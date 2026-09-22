#!/usr/bin/env python3
"""Generate minimal Natural Earth GeoJSON files for the attack map.

The site lazily fetches two ~40MB Natural Earth datasets (see DETAILS_URL
and PLACES_URL in index.html) but only ever uses features belonging to
countries that have attacks filed in attacks.json. This script downloads
both datasets, drops every feature for countries with zero attacks, trims
unused properties, and writes minified JSON files next to this script:

    tools/ne_10m_admin_1_states_provinces.min.json
    tools/ne_10m_populated_places_simple.min.json

Country matching uses the exact same keys as index.html:
  * admin-1 features: properties.admin / properties.geonunit vs the world
    geojson country name (with a " S.A.R." suffix also accepted)
  * places are kept if their point falls inside any kept admin-1 polygon
    (after a bbox pre-filter), same as the frontend

Usage: python3 generateMinimalGeoJSON.py
"""

import json
import math
import os
import urllib.request

TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(TOOLS_DIR)
ATTACKS_PATH = os.path.join(REPO_ROOT, "attacks.json")

DETAILS_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_admin_1_states_provinces.geojson"
PLACES_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_populated_places_simple.geojson"
WORLD_URL = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"

DETAILS_OUT = os.path.join(TOOLS_DIR, "ne_10m_admin_1_states_provinces.min.json")
PLACES_OUT = os.path.join(TOOLS_DIR, "ne_10m_populated_places_simple.min.json")

# --- mirrors ISO2_TO_3 in index.html (extend there if attacks are added
# for new countries) ---
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

# Properties used by index.html for admin-1 features:
#   admin/geonunit -> country matching & names, name -> region labels.
ADMIN1_KEEP_PROPS = {"admin", "geonunit", "name"}


def fetch_json(url):
    print(f"downloading {url} ...", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    print(f"  -> {len(data.get('features', []))} features")
    return data


def country_names():
    """Names of countries with attacks, mirroring index.html countryName()."""
    with open(ATTACKS_PATH) as f:
        attacks = json.load(f)
    iso3s = {ISO2_TO_3.get(a["country_code"]) for a in attacks}
    iso3s.discard(None)
    world = fetch_json(WORLD_URL)
    by_id = {f.get("id"): f["properties"]["name"] for f in world["features"]}
    names = {by_id[iso3] for iso3 in iso3s if iso3 in by_id}
    missing = iso3s - set(by_id)
    if missing:
        print(f"warning: no world.geo.json feature for: {sorted(missing)}")
    print(f"attack countries: {len(iso3s)} ({len(names)} world features)")
    return names


def geom_bbox(geom):
    min_lat, max_lat, min_lng, max_lng = math.inf, -math.inf, math.inf, -math.inf
    polys = ([geom["coordinates"]] if geom["type"] == "Polygon"
             else geom["coordinates"] if geom["type"] == "MultiPolygon" else [])
    for poly in polys:
        for ring in poly:
            for lng, lat, *_ in ring:
                min_lat, max_lat = min(min_lat, lat), max(max_lat, lat)
                min_lng, max_lng = min(min_lng, lng), max(max_lng, lng)
    if min_lat is math.inf:
        return None
    return (min_lat, max_lat, min_lng, max_lng)


def point_in_ring(lat, lng, ring):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if (yi > lat) != (yj > lat):
            xint = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lng < xint:
                inside = not inside
        j = i
    return inside


def point_in_geometry(lat, lng, geom):
    polys = ([geom["coordinates"]] if geom["type"] == "Polygon"
             else geom["coordinates"] if geom["type"] == "MultiPolygon" else [])
    for poly in polys:
        if point_in_ring(lat, lng, poly[0]):
            if not any(point_in_ring(lat, lng, hole) for hole in poly[1:]):
                return True
    return False


def trim_admin1(features, names):
    kept = []
    for f in features:
        p = f.get("properties") or {}
        if any(p.get(k) == name or p.get(k) == name + " S.A.R."
               for name in names for k in ("admin", "geonunit")):
            kept.append({
                "type": "Feature",
                "properties": {k: v for k, v in p.items() if k in ADMIN1_KEEP_PROPS},
                "geometry": f["geometry"],
            })
    return kept


def trim_places(features, kept_admin1):
    bboxes = [geom_bbox(f["geometry"]) for f in kept_admin1]
    kept = []
    for f in features:
        geom = f.get("geometry")
        coords = geom and geom.get("coordinates")
        if not coords:
            continue
        lng, lat = coords[0], coords[1]
        for bf, bb in zip(kept_admin1, bboxes):
            if bb is None:
                continue
            min_lat, max_lat, min_lng, max_lng = bb
            if min_lat <= lat <= max_lat and min_lng <= lng <= max_lng:
                if point_in_geometry(lat, lng, bf["geometry"]):
                    kept.append({
                        "type": "Feature",
                        "properties": {"pop_max": (f.get("properties") or {}).get("pop_max", 0)},
                        "geometry": {"type": "Point", "coordinates": coords},
                    })
                    break
    return kept


def write_min(path, features):
    fc = {"type": "FeatureCollection", "features": features}
    with open(path, "w") as f:
        json.dump(fc, f, separators=(",", ":"), ensure_ascii=False)
    size = os.path.getsize(path)
    print(f"wrote {os.path.basename(path)}: {len(features)} features, "
          f"{size / 1048576:.1f} MB ({size} bytes)")


def main():
    names = country_names()

    admin1 = fetch_json(DETAILS_URL)
    kept_admin1 = trim_admin1(admin1["features"], names)
    print(f"admin-1: kept {len(kept_admin1)} of {len(admin1['features'])}")
    write_min(DETAILS_OUT, kept_admin1)

    places = fetch_json(PLACES_URL)
    kept_places = trim_places(places["features"], kept_admin1)
    print(f"places: kept {len(kept_places)} of {len(places['features'])}")
    write_min(PLACES_OUT, kept_places)


if __name__ == "__main__":
    main()
