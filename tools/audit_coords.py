#!/usr/bin/env python3
"""Audit attacks.json geo-coordinates against country polygons.

For each attack, verify that (lat, lng) falls inside the polygon of its
assigned country (from the same johan/world.geo.json the dashboard uses).
For points that fail, try simple corrective transforms (swapped lat/lng,
dropped negative signs) and keep the first one that lands inside the right
country. Writes a fixed attacks.json and prints a report.
"""
import json
import urllib.request

ATTACKS = "attacks.json"
# High-resolution country polygons (Natural Earth 10m). The coarse 110m
# johan polygons used by the dashboard misclassify coastal/island cities.
WORLD = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
         "master/geojson/ne_10m_admin_0_countries.geojson")

ISO2_TO_3 = {
    "AE": "ARE", "AR": "ARG", "AT": "AUT", "AU": "AUS", "BE": "BEL",
    "BG": "BGR", "BR": "BRA", "CA": "CAN", "CN": "CHN", "CO": "COL",
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


def which_country(lat, lng, features):
    for f in features:
        if point_in_geometry(lat, lng, f["geometry"]):
            return f["id"]
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


def main():
    import sys
    fix_mode = "--fix" in sys.argv
    with open(ATTACKS) as fh:
        attacks = json.load(fh)
    print(f"Fetching world polygons from {WORLD} ...")
    with urllib.request.urlopen(WORLD) as r:
        world = json.load(r)
    features = world["features"]

    def geom_for(iso3):
        for f in features:
            p = f["properties"]
            if (p.get("ADM0_A3") == iso3 or p.get("adm0_a3") == iso3
                    or f.get("id") == iso3):
                return f["geometry"]
        return None

    misplaced, fixed, unfixable = [], [], []
    for a in attacks:
        iso3 = ISO2_TO_3.get(a.get("country_code"))
        lat, lng = a.get("lat"), a.get("lng")
        if not iso3 or lat is None or lng is None:
            continue                                  # no geo data to check
        g = geom_for(iso3)
        if g is None:
            print(f"  !! no polygon for {iso3}")
            continue
        if point_in_geometry(lat, lng, g):
            continue                                  # already correct
        misp = (a.get("country_code"), a.get("city"), lat, lng)
        misplaced.append(misp)
        if not fix_mode:
            continue
        # try transforms that land inside the right country
        best = None
        for tlat, tlng in list(transforms(lat, lng))[1:]:
            if point_in_geometry(tlat, tlng, g):
                best = (tlat, tlng)
                break
        if best:
            a["lat"], a["lng"] = best
            fixed.append(misp + (best[0], best[1]))
        else:
            unfixable.append(misp)

    if fix_mode:
        with open(ATTACKS, "w") as fh:
            json.dump(attacks, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

    print(f"\n{len(misplaced)} misplaced coordinate(s) found.")
    if fix_mode:
        print(f"Fixed {len(fixed)}:")
        for cc, city, ol, og, nl, ng in fixed:
            print(f"  {cc} {city}: ({ol}, {og}) -> ({nl}, {ng})")
        if unfixable:
            print(f"\nStill outside their country borders ({len(unfixable)}) — "
                  "manual review needed:")
            for cc, city, lat, lng in unfixable:
                print(f"  {cc} {city}: ({lat}, {lng})")
        else:
            print("All misplaced coordinates now fixed.")
    else:
        print("(dry run — re-run with --fix to apply corrections)")
        for cc, city, lat, lng in misplaced:
            print(f"  {cc} {city}: ({lat}, {lng})")


if __name__ == "__main__":
    main()
