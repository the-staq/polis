"""Checks for the OSM venue layer in odbl/ and its join to the CC BY venues.

Real public places (L and P tiers) are named and placed from OpenStreetMap.
That data lives only in odbl/ (ODbL 1.0, published as a derivative database)
and is joined to the CC BY gameplay rows in seeds/<world>/venues/ by venue id.
test_config_schemas.py scans only configs/ and seeds/, so this module covers
odbl/ and the rules that cross the two layers:

* every odbl/<city>/venues-osm.geojson validates against venue-osm.schema.json;
* venue ids and OSM elements are unique, and the picks, the GeoJSON and the
  latest EXTRACT-LOG.yaml entry name the same elements;
* each OSM feature has exactly one venue row with name_source osm and tier
  L or P, and each such row has a feature;
* the licence, attribution, NOTICE and configs/sources.yaml entry exist;
* no YAML under configs/ or seeds/ stores an OSM id or a maps provider ref,
  except the legacy lot.schema.json maps_provider_ref block;
* every institution venue_id, parent_venue_id and host_venue_id resolves;
* fictional venues are not named after, or placed on, an OSM feature.

Standard library, PyYAML and jsonschema only. No network.

    python -m pytest cli/tests/test_odbl_dataset.py
"""

from __future__ import annotations

import json
import math
from collections import Counter
from fnmatch import fnmatch
from functools import lru_cache
from pathlib import Path

import pytest
import yaml
from jsonschema.validators import validator_for

REPO_ROOT = Path(__file__).resolve().parents[2]
ODBL_DIR = REPO_ROOT / "odbl"
SCHEMA_DIR = REPO_ROOT / "schemas"
OSM_ATTRIBUTION = "© OpenStreetMap contributors"
OSM_KEYS = frozenset({"osm_id", "osm_type", "maps_provider_ref"})
# lot.schema.json still carries maps_provider_ref {osm_type, osm_id} (legacy,
# retires in P2.10). Only lot files may use it, and only there.
LOT_GLOBS = ("seeds/*/lots/**/*.yaml", "seeds/*/*/geography/lots/**/*.yaml")
# A hand-placed fictional venue must sit at least this far from any OSM point.
MIN_DISTANCE_M = 75.0


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------


def _load_yaml(path: Path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _schema(name: str):
    schema = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
    return validator_for(schema)(schema)


def _geojson_files() -> list[Path]:
    return sorted(ODBL_DIR.glob("*/venues-osm.geojson"))


@lru_cache(maxsize=None)
def _features() -> tuple[dict, ...]:
    out = []
    for path in _geojson_files():
        out.extend(json.loads(path.read_text(encoding="utf-8"))["features"])
    return tuple(out)


@lru_cache(maxsize=None)
def _picks() -> tuple[dict, ...]:
    out = []
    for path in sorted((ODBL_DIR / "picks").glob("*.yaml")):
        out.extend(_load_yaml(path)["picks"])
    return tuple(out)


def _venue_files() -> list[Path]:
    return sorted(REPO_ROOT.glob("seeds/*/venues/*.yaml"))


@lru_cache(maxsize=None)
def _venues() -> tuple[dict, ...]:
    out = []
    for path in _venue_files():
        out.extend(_load_yaml(path)["venues"])
    return tuple(out)


def _venues_by_id() -> dict[str, dict]:
    return {v["id"]: v for v in _venues()}


def _osm_ref(props: dict) -> str:
    return f"{props['osm_type']}/{props['osm_id']}"


def _distance_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine distance in metres."""
    r = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


# --------------------------------------------------------------------------
# The ODbL layer itself
# --------------------------------------------------------------------------


def test_layer_exists() -> None:
    assert _geojson_files(), "no odbl/<city>/venues-osm.geojson files"
    assert _features(), "the OSM venue layer has no features"


@pytest.mark.parametrize("path", _geojson_files(), ids=lambda p: p.relative_to(REPO_ROOT).as_posix())
def test_geojson_validates(path: Path) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    errors = sorted(_schema("venue-osm.schema.json").iter_errors(doc), key=lambda e: list(e.absolute_path))
    assert not errors, "\n".join(f"/{'/'.join(map(str, e.absolute_path))}: {e.message}" for e in errors)


def test_feature_ids_and_elements_are_unique() -> None:
    ids = Counter(f["properties"]["venue_id"] for f in _features())
    refs = Counter(_osm_ref(f["properties"]) for f in _features())
    assert not [k for k, n in ids.items() if n > 1], f"duplicate venue_id: {ids.most_common(3)}"
    assert not [k for k, n in refs.items() if n > 1], f"OSM element used twice: {refs.most_common(3)}"


def test_osm_version_all_or_none() -> None:
    """A live extract has a version on every feature; a file extract on none."""
    for path in _geojson_files():
        doc = json.loads(path.read_text(encoding="utf-8"))
        flags = {"osm_version" in f["properties"] for f in doc["features"]}
        assert len(flags) <= 1, f"{path.name}: osm_version on some features only"


def test_every_pick_resolves_to_one_feature() -> None:
    """picks/*.yaml and the GeoJSON name the same venues and elements."""
    picks = {p["venue_id"]: f"{p['osm_type']}/{p['osm_id']}" for p in _picks()}
    features = {f["properties"]["venue_id"]: _osm_ref(f["properties"]) for f in _features()}
    assert len(picks) == len(_picks()), "duplicate venue_id in picks"
    assert picks == features, (
        f"picks without a feature: {sorted(set(picks) - set(features))}; "
        f"features without a pick: {sorted(set(features) - set(picks))}; "
        f"element mismatch: {sorted(k for k in picks.keys() & features.keys() if picks[k] != features[k])}"
    )
    assert all(p["tier"] in ("L", "P") for p in _picks()), "picks may only be tier L or P"


def test_extract_log_matches_layer() -> None:
    """The latest EXTRACT-LOG.yaml entry records the URL, base timestamp and every element."""
    log = _load_yaml(ODBL_DIR / "EXTRACT-LOG.yaml")
    assert isinstance(log, list) and log, "EXTRACT-LOG.yaml must be a non-empty list"
    for entry in log:
        missing = {"date", "script_version", "overpass_url", "osm_base_timestamp", "osm_ids"} - set(entry)
        assert not missing, f"log entry {entry.get('date')} lacks {sorted(missing)}"
        assert str(entry["overpass_url"]).startswith("https://"), entry["overpass_url"]
    latest = log[-1]
    assert sorted(latest["osm_ids"]) == sorted(_osm_ref(f["properties"]) for f in _features())
    assert {f["properties"]["retrieved_at"] for f in _features()} == {latest["osm_base_timestamp"]}


# --------------------------------------------------------------------------
# Licence and attribution
# --------------------------------------------------------------------------


def test_licence_and_attribution_present() -> None:
    licence = (ODBL_DIR / "LICENSE").read_text(encoding="utf-8")
    assert "Open Database License" in licence and "Database Contents License" in licence
    assert OSM_ATTRIBUTION in (ODBL_DIR / "README.md").read_text(encoding="utf-8")
    for path in _geojson_files():
        doc = json.loads(path.read_text(encoding="utf-8"))
        assert doc["license"] == "ODbL-1.0" and OSM_ATTRIBUTION in doc["attribution"], path.name

    notice = (REPO_ROOT / "NOTICE").read_text(encoding="utf-8")
    assert OSM_ATTRIBUTION in notice and "odbl/" in notice and "ODbL" in notice
    assert "odbl/" in (REPO_ROOT / "LICENSE-CONTENT").read_text(encoding="utf-8")
    assert "odbl/" in (REPO_ROOT / "README.md").read_text(encoding="utf-8")


def test_sources_yaml_has_openstreetmap() -> None:
    sources = _load_yaml(REPO_ROOT / "configs" / "sources.yaml")["sources"]
    osm = [s for s in sources if s.get("id") == "openstreetmap"]
    assert len(osm) == 1, "configs/sources.yaml needs exactly one openstreetmap entry"
    entry = osm[0]
    assert entry["license"] == "ODbL-1.0"
    assert OSM_ATTRIBUTION in entry["attribution"]
    assert "odbl/**" in entry["used_in"]


# --------------------------------------------------------------------------
# The join to the CC BY venue rows
# --------------------------------------------------------------------------


def test_venue_ids_are_unique_and_match_their_file() -> None:
    ids = Counter(v["id"] for v in _venues())
    assert not [k for k, n in ids.items() if n > 1], f"duplicate venue ids: {ids.most_common(3)}"
    for path in _venue_files():
        doc = _load_yaml(path)
        assert path.stem == doc["district"], f"{path.name}: district {doc['district']!r}"
        assert (path.parents[1] / "districts" / f"{doc['district']}.yaml").exists(), path.name
        assert all(v["district"] == doc["district"] for v in doc["venues"]), path.name


def test_each_feature_has_exactly_one_osm_row_and_back() -> None:
    feature_ids = {f["properties"]["venue_id"] for f in _features()}
    osm_rows = [v for v in _venues() if v["name_source"] == "osm"]
    assert all(v["tier"] in ("L", "P") for v in osm_rows), "name_source osm rows must be tier L or P"
    rows = Counter(v["id"] for v in osm_rows)
    assert all(rows[i] == 1 for i in feature_ids), (
        f"features without exactly one osm row: {sorted(i for i in feature_ids if rows[i] != 1)}"
    )
    assert set(rows) <= feature_ids, f"osm rows without a feature: {sorted(set(rows) - feature_ids)}"


def test_osm_rows_agree_with_picks() -> None:
    """Tier, kind and district in the CC BY row match the pick that sourced it."""
    venues = _venues_by_id()
    for pick in _picks():
        row = venues[pick["venue_id"]]
        for key in ("tier", "kind", "district"):
            assert row[key] == pick[key], f"{pick['venue_id']}: {key} {row[key]!r} != pick {pick[key]!r}"


def test_venue_links_resolve() -> None:
    venues = _venues_by_id()
    for v in _venues():
        if "parent_venue_id" in v:
            parent = venues.get(v["parent_venue_id"])
            assert parent is not None, f"{v['id']}: parent {v['parent_venue_id']} not found"
            assert parent["tier"] in ("L", "P"), f"{v['id']}: parent must be a public place"
        if "host_venue_id" in v:
            host = venues.get(v["host_venue_id"])
            assert host is not None, f"{v['id']}: host {v['host_venue_id']} not found"
            assert host["tier"] in ("L", "P") and host["district"] == v["district"], v["id"]


def test_every_institution_venue_id_resolves() -> None:
    venues = _venues_by_id()
    paths = sorted(REPO_ROOT.glob("configs/institutions/*.yaml")) + sorted(
        REPO_ROOT.glob("seeds/*/*/*/institutions/*.yaml")
    )
    for path in paths:
        doc = _load_yaml(path)
        venue_id = doc.get("venue_id")
        if venue_id is None:
            continue
        venue = venues.get(venue_id)
        assert venue is not None, f"{path.name}: venue_id {venue_id} not found"
        assert venue["tier"] in ("V", "B"), f"{path.name}: institutions trade from V/B venue rows"
        district = doc.get("district")
        if isinstance(district, str):
            assert district.lower() == venue["district"], f"{path.name}: district {district} != {venue['district']}"


def test_fictional_names_and_points_stay_off_osm() -> None:
    """polis and licensed rows never reuse an OSM name, and hand-placed points
    sit near, not on, the OSM places."""
    osm_names = {f["properties"]["name"].casefold() for f in _features() if f["properties"]["name"]}
    points = [
        (f["geometry"]["coordinates"][1], f["geometry"]["coordinates"][0], f["properties"]["venue_id"])
        for f in _features()
    ]
    for v in _venues():
        if v["name_source"] not in ("polis", "licensed"):
            continue
        assert v["name"].casefold() not in osm_names, f"{v['id']}: name copies an OSM name"
        if "lat" in v:
            near = min(points, key=lambda p: _distance_m(v["lat"], v["lon"], p[0], p[1]))
            d = _distance_m(v["lat"], v["lon"], near[0], near[1])
            assert d >= MIN_DISTANCE_M, f"{v['id']} is {d:.0f} m from {near[2]}; place it off the OSM point"


# --------------------------------------------------------------------------
# No OSM data outside odbl/
# --------------------------------------------------------------------------


def _key_paths(node, prefix: tuple = ()):
    if isinstance(node, dict):
        for key, value in node.items():
            yield (*prefix, key)
            yield from _key_paths(value, (*prefix, key))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from _key_paths(value, (*prefix, i))


def test_no_osm_keys_in_configs_or_seeds() -> None:
    problems = []
    for base in ("configs", "seeds"):
        for path in sorted((REPO_ROOT / base).rglob("*.y*ml")):
            rel = path.relative_to(REPO_ROOT).as_posix()
            is_lot = any(fnmatch(rel, g) for g in LOT_GLOBS)
            for doc in yaml.safe_load_all(path.read_text(encoding="utf-8")):
                for key_path in _key_paths(doc):
                    key = key_path[-1]
                    if key not in OSM_KEYS:
                        continue
                    if is_lot and key_path[0] == "maps_provider_ref" and len(key_path) <= 2:
                        continue  # legacy lot.schema.json block
                    problems.append(f"{rel}: {'/'.join(map(str, key_path))}")
    assert not problems, "OSM ids belong only in odbl/ (join by venue_id):\n" + "\n".join(problems)


# --------------------------------------------------------------------------
# The venue.schema.json source rules
# --------------------------------------------------------------------------

_BASE = {"world": "modern-earth-2026", "district": "hackney"}


def _row_errors(row: dict) -> list[str]:
    doc = {**_BASE, "venues": [{"district": "hackney", **row}]}
    return [e.message for e in _schema("venue.schema.json").iter_errors(doc)]


@pytest.mark.parametrize(
    "row",
    [
        {"id": "x-park", "tier": "P", "kind": "park", "name_source": "osm"},
        {"id": "x-slot", "tier": "P", "kind": "pitch", "name_source": "generic", "slot_label": "Pitch 1", "parent_venue_id": "x-park"},
        {"id": "x-cafe", "tier": "B", "kind": "cafe", "name_source": "polis", "name": "Some Cafe", "lat": 51.5, "lon": -0.1},
        {"id": "x-stall", "tier": "B", "kind": "stall", "name_source": "polis", "name": "Some Stall", "host_venue_id": "x-park"},
        {"id": "x-shop", "tier": "B", "kind": "cafe", "name_source": "licensed", "name": "Real Cafe", "lat": 51.5, "lon": -0.1},
    ],
    ids=["osm", "generic", "polis-point", "polis-hosted", "licensed"],
)
def test_venue_schema_accepts(row: dict) -> None:
    assert _row_errors(row) == []


@pytest.mark.parametrize(
    "row",
    [
        {"id": "x-park", "tier": "P", "kind": "park", "name_source": "osm", "name": "Copied Name"},
        {"id": "x-park", "tier": "P", "kind": "park", "name_source": "osm", "lat": 51.5, "lon": -0.1},
        {"id": "x-pub", "tier": "B", "kind": "pub", "name_source": "osm"},
        {"id": "x-court", "tier": "V", "kind": "other", "name_source": "osm"},
        {"id": "x-cafe", "tier": "B", "kind": "cafe", "name_source": "generic", "slot_label": "A", "parent_venue_id": "x-park"},
        {"id": "x-slot", "tier": "P", "kind": "pitch", "name_source": "generic", "slot_label": "Pitch 1", "parent_venue_id": "x-park", "lat": 51.5, "lon": -0.1},
        {"id": "x-cafe", "tier": "B", "kind": "cafe", "name_source": "polis", "name": "Some Cafe"},
        {"id": "x-park", "tier": "P", "kind": "park", "name_source": "licensed", "name": "Sold Park", "lat": 51.5, "lon": -0.1},
    ],
    ids=["osm-name", "osm-point", "osm-B", "osm-V", "generic-B", "generic-point", "polis-no-point", "licensed-P"],
)
def test_venue_schema_rejects(row: dict) -> None:
    assert _row_errors(row), f"venue.schema.json accepted {row}"
