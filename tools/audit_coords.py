#!/usr/bin/env python3
"""Audit attacks.json geo-coordinates against country polygons.

For each attack, verify that (lat, lng) falls inside the polygon of its
assigned country. Points within TOL_KM of the border also count as correct:
Natural Earth's coastlines are vertex-snapped, so genuine coastal and border
cities (Miami, Lagos, Florianopolis, ...) routinely sit a few km seaward of
the outline.

For points that fail, try simple corrective transforms (swapped lat/lng,
dropped negative signs) and keep the first one that lands inside the right
country.

IMPORTANT: attacks.json is a *build artifact* — CI regenerates it from
README.md via geocode.py on every push. Patching attacks.json would be
silently reverted, so --fix instead repairs the authoritative GEO table in
geocode.py and then re-runs the generator. That makes the repair survive
regeneration and show up in review.

Usage:
    python3 tools/audit_coords.py           # dry run, report only (exit 0)
    python3 tools/audit_coords.py --gate    # exit 1 if anything is misplaced
    python3 tools/audit_coords.py --fix     # repair geocode.py, then regenerate
"""
import json
import math
import re
import sys
import urllib.request
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ATTACKS = "attacks.json"
GEOCODE = TOOLS / "geocode.py"

# High-resolution country polygons (Natural Earth 10m). The coarse 110m
# johan polygons used by the dashboard misclassify coastal/island cities.
# Vendored locally so the CI gate is offline and deterministic; falls back to
# the upstream URL only if the vendored copy is absent.
LOCAL_WORLD = TOOLS / "ne_10m_admin_0_countries.min.json"
WORLD = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
         "master/geojson/ne_10m_admin_0_countries.geojson")


def load_world():
    """Return the list of country features, preferring the vendored copy."""
    if LOCAL_WORLD.exists():
        with LOCAL_WORLD.open(encoding="utf-8") as fh:
            return json.load(fh)["features"]
    print(f"Vendored polygons missing, downloading from {WORLD} ...")
    with urllib.request.urlopen(WORLD) as r:
        return json.load(r)["features"]

# A point this close to (or inside) the country outline counts as correct.
# Coastal cities are frequently a few km seaward of the vertex-snapped
# Natural Earth coastline, so a strict inside/outside test flags good data.
TOL_KM = 10.0
KM_PER_DEG = 111.0                                   # rough, fine at this scale

ISO2_TO_3 = {
    "AE": "ARE", "AR": "ARG", "AT": "AUT", "AU": "AUS", "BE": "BEL",
    "BD": "BGD", "BG": "BGR", "BR": "BRA", "CA": "CAN", "CN": "CHN", "CO": "COL",
    "CR": "CRI", "CY": "CYP", "DE": "DEU", "EE": "EST", "ES": "ESP",
    "FR": "FRA", "GB": "GBR", "GE": "GEO", "GH": "GHA", "HK": "HKG",
    "ID": "IDN", "IL": "ISR", "IN": "IND", "IS": "ISL", "IT": "ITA",
    "JP": "JPN", "KR": "KOR", "LK": "LKA", "LT": "LTU", "LV": "LVA",
    "MT": "MLT", "ME": "MNE", "MX": "MEX", "MY": "MYS", "NG": "NGA",
    "NL": "NLD", "NO": "NOR", "NZ": "NZL", "PH": "PHL", "PK": "PAK",
    "PL": "POL", "PY": "PRY", "RO": "ROU", "RU": "RUS", "SE": "SWE",
    "SG": "SGP", "TH": "THA", "TR": "TUR", "TT": "TTO", "TW": "TWN",
    "UA": "UKR", "UG": "UGA", "US": "USA", "VN": "VNM", "ZA": "ZAF",
}


def point_in_ring(lat, lng, ring):
    """Ray casting; ring is list of [lng, lat] (GeoJSON order)."""
    x, y = lng, lat
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > y) != (yj > y):
            xint = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < xint:
                inside = not inside
        j = i
    return inside


def point_in_geometry(lat, lng, geom):
    """True if point inside any polygon of the geometry (holes respected)."""
    polys = ([geom["coordinates"]] if geom["type"] == "Polygon"
             else geom["coordinates"] if geom["type"] == "MultiPolygon"
             else [])
    for poly in polys:
        if point_in_ring(lat, lng, poly[0]):          # inside outer ring
            if not any(point_in_ring(lat, lng, hole) for hole in poly[1:]):
                return True
    return False


def _rings(geom):
    """Yield every ring (outer + holes) of a Polygon/MultiPolygon geometry."""
    polys = ([geom["coordinates"]] if geom["type"] == "Polygon"
             else geom["coordinates"] if geom["type"] == "MultiPolygon"
             else [])
    for poly in polys:
        for ring in poly:
            yield ring


def _seg_dist_deg(px, py, ax, ay, bx, by):
    """Distance in degrees from point (px, py) to segment (ax, ay)-(bx, by)."""
    dx, dy = bx - ax, by - ay
    if dx == 0.0 and dy == 0.0:
        return math.hypot(px - ax, py - ay)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def point_to_geometry_dist_deg(lat, lng, geom):
    """Distance in degrees from a point to the nearest polygon edge.

    Planar approximation, which is plenty accurate over the few-km scale
    this is used at. Segment-based (not vertex-based) so a point near the
    middle of a long straight coastline still measures as close.
    """
    best = float("inf")
    for ring in _rings(geom):
        n = len(ring)
        for i in range(n):
            ax, ay = ring[i - 1]                      # i-1 wraps to n-1
            bx, by = ring[i]
            d = _seg_dist_deg(lng, lat, ax, ay, bx, by)
            if d < best:
                best = d
    return best


def near_geometry(lat, lng, geom, tol_km=TOL_KM):
    """True if the point is inside the geometry or within tol_km of its edge."""
    if point_in_geometry(lat, lng, geom):
        return True
    return point_to_geometry_dist_deg(lat, lng, geom) * KM_PER_DEG <= tol_km


def which_country(lat, lng, features):
    for f in features:
        # Natural Earth 10m features have no top-level "id"; the ISO code
        # lives in properties (ADM0_A3), so fall back to that.
        if point_in_geometry(lat, lng, f["geometry"]):
            return f["properties"].get("ADM0_A3") or f.get("id")
    return None


def transforms(lat, lng):
    """Candidate fixes for a misplaced point, in preference order."""
    yield lat, lng                                    # as-is (no-op)
    yield -lat, lng                                   # dropped S. hemisphere sign
    yield lat, -lng                                   # dropped W. hemisphere sign
    yield -lat, -lng                                  # both signs dropped
    yield lng, lat                                    # swapped lat/lng
    yield -lng, lat                                   # swapped + sign fix
    yield lng, -lat                                   # swapped + sign fix
    yield -lng, -lat                                  # swapped + both signs


def geo_entry_re(location):
    """Regex matching a GEO dict line for exactly this location key."""
    return re.compile(
        r"^(?P<indent>[ \t]*)(?P<key>" + re.escape(repr(location)) +
        r'|"' + re.escape(location) + r'")(?P<mid>\s*:\s*)(?P<val>\([^)]*\))(?P<tail>.*)$',
        re.MULTILINE)


def patch_geocode(location, city, region, country, iso2, lat, lng):
    """Rewrite one GEO tuple in geocode.py. Returns True if the line changed.

    This is the durable repair point: geocode.py is the source of truth that
    CI feeds through to attacks.json, so fixing it here survives regeneration.
    Existing quote style is preserved so repairs don't create cosmetic churn.
    """
    text = GEOCODE.read_text(encoding="utf-8")
    m = geo_entry_re(location).search(text)
    if m is None:
        return False
    q = "'" if m.group("val").lstrip("(").startswith("'") else '"'
    parts = [city, region, country, iso2]
    new_val = "(" + ", ".join(q + str(p) + q for p in parts) + f", {lat}, {lng})"
    if m.group("val") == new_val:
        return False
    GEOCODE.write_text(text[:m.start("val")] + new_val + text[m.end("val"):],
                       encoding="utf-8")
    return True


def main():
    gate = "--gate" in sys.argv
    fix_mode = "--fix" in sys.argv
    with open(ATTACKS) as fh:
        attacks = json.load(fh)

    features = load_world()

    def geom_for(iso3):
        for f in features:
            p = f["properties"]
            if (p.get("ADM0_A3") == iso3 or p.get("adm0_a3") == iso3
                    or f.get("id") == iso3):
                return f["geometry"]
        return None

    if fix_mode:
        # Import lazily so dry runs don't require importing the GEO table.
        sys.path.insert(0, str(TOOLS))
        import geocode as geocode_mod
        GEO = geocode_mod.GEO
    else:
        GEO = {}

    misplaced, fixed, unfixable, no_geo_entry = [], [], [], []
    for a in attacks:
        iso3 = ISO2_TO_3.get(a.get("country_code"))
        lat, lng = a.get("lat"), a.get("lng")
        if not iso3 or lat is None or lng is None:
            continue                                  # no geo data to check
        g = geom_for(iso3)
        if g is None:
            print(f"  !! no polygon for {iso3}")
            continue
        if near_geometry(lat, lng, g):
            continue                                  # inside, or on the coast
        loc = a.get("location")
        misp = (a.get("country_code"), a.get("city"), lat, lng, loc)
        misplaced.append(misp)
        if not fix_mode:
            continue
        # try transforms that land inside (or within tolerance of) the country
        best = None
        for tlat, tlng in list(transforms(lat, lng))[1:]:
            if near_geometry(tlat, tlng, g):
                best = (tlat, tlng)
                break
        if not best:
            unfixable.append(misp)
            continue
        # Repair the SOURCE (geocode.py), not the generated attacks.json.
        cur = GEO.get(loc)
        if cur is None:
            no_geo_entry.append(misp)
            continue
        city, region, country, iso2 = cur[0], cur[1], cur[2], cur[3]
        if patch_geocode(loc, city, region, country, iso2, best[0], best[1]):
            GEO[loc] = (city, region, country, iso2, best[0], best[1])
            fixed.append(misp + (best[0], best[1]))

    if fix_mode and fixed:
        # Regenerate so attacks.json reflects the repaired GEO table.
        import subprocess
        subprocess.run([sys.executable, str(TOOLS / "geocode.py")], check=True,
                       cwd=str(TOOLS.parent))

    print(f"\n{len(misplaced)} misplaced coordinate(s) found.")
    if fix_mode:
        print(f"Repaired {len(fixed)} GEO entr"
              f"{'y' if len(fixed) == 1 else 'ies'} in {GEOCODE.name}:")
        for cc, city, ol, og, _loc, nl, ng in fixed:
            print(f"  {cc} {city}: ({ol}, {og}) -> ({nl}, {ng})")
        if no_geo_entry:
            print(f"\nNo GEO entry for {len(no_geo_entry)} location(s) — add them manually:")
            for cc, city, lat, lng, loc in no_geo_entry:
                print(f"  {cc} {city}: {loc!r} ({lat}, {lng})")
        if unfixable:
            print(f"\nStill outside their country borders ({len(unfixable)}) — "
                  "manual review needed:")
            for cc, city, lat, lng, _loc in unfixable:
                g = geom_for(ISO2_TO_3.get(cc))
                off = point_to_geometry_dist_deg(lat, lng, g) * KM_PER_DEG
                print(f"  {cc} {city}: ({lat}, {lng})  [{off:.1f} km from border]")
        if not fixed and not unfixable and not no_geo_entry:
            print("All misplaced coordinates now fixed.")
    else:
        source = "vendored" if LOCAL_WORLD.exists() else WORLD
        print(f"(dry run — tolerance {TOL_KM:g} km, polygons: {source}; "
              "re-run with --fix to repair geocode.py)")
        for cc, city, lat, lng, loc in misplaced:
            g = geom_for(ISO2_TO_3.get(cc))
            off = point_to_geometry_dist_deg(lat, lng, g) * KM_PER_DEG
            print(f"  {cc} {city}: ({lat}, {lng})  [{off:.1f} km from border]")

    remaining = len(misplaced) - len(fixed)
    if gate and remaining:
        print(f"\nFAILED: {remaining} coordinate(s) outside their country. "
              "Run tools/audit_coords.py --fix and commit geocode.py.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
