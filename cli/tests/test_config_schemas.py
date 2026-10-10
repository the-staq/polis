"""Validate every YAML under configs/ and seeds/ against the JSON Schema that applies.

`polis-cli validate` is planned but not built yet (see cli/README.md). Until it
ships, this module is the schema check that CI runs. It follows the pattern of
sim/tests/test_sim_config_schema.py: PyYAML `yaml.safe_load` + `jsonschema`.

How files are matched
---------------------
* SCHEMA_MAP lists (glob, schema file, optional JSON pointer) entries. A file
  that matches one is validated against that schema, or against the sub-schema
  at the pointer.
* NO_SCHEMA lists (glob, reason) entries for YAML that no schema in schemas/
  describes.
* test_every_yaml_is_classified fails if a .yaml/.yml file under configs/ or
  seeds/ matches no entry, or matches more than one. New files therefore
  cannot skip validation silently: add them to one of the two tables.

Validation details
------------------
* Each schema is used with the validator class for its declared `$schema`
  (Draft 2020-12 for all of them today), via
  `jsonschema.validators.validator_for`.
* Cross-schema `$ref`s (for example character -> mortality#/$defs/vital_status)
  resolve through a local `referencing.Registry` keyed by each schema's `$id`.
  Nothing is fetched over the network.
* `format` is an annotation only (the Draft 2020-12 default). This matches the
  existing tests, which call `jsonschema.validate` without a format checker.
* YAML is loaded with `yaml.safe_load`, the loader that polis-internal and the
  existing tests use. A scalar that YAML turns into a non-JSON type, such as an
  unquoted date, is reported as an error.
* Every error for a file is reported (`iter_errors`), not only the first one.

Known failures
--------------
KNOWN_FAILURES lists files that fail today because of a tracked data or schema
problem. known_schema_errors.json records each one's exact errors, as
(instance path, keyword) pairs. Such a file counts as xfail(strict=True) only
while its errors match that record exactly:
* a new or different error fails the run, so known-bad files are still checked;
* a fixed file XPASSes, which fails the run until its entry is removed.
After a deliberate partial fix, regenerate the record with
`POLIS_UPDATE_KNOWN_SCHEMA_ERRORS=1 python -m pytest cli/tests/test_config_schemas.py`.

Run from the repo root (this module does not import `polis.sim`):

    python -m pytest cli/tests/test_config_schemas.py
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from urllib.parse import urljoin

import pytest
import yaml
from jsonschema.validators import validator_for
from referencing import Registry, Resource

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schemas"
SCANNED_DIRS = ("configs", "seeds")
YAML_SUFFIXES = (".yaml", ".yml")


@dataclass(frozen=True)
class SchemaRule:
    glob: str
    """Glob relative to the repo root."""
    schema: str
    """File name under schemas/."""
    pointer: str = ""
    """Optional JSON pointer into the schema, e.g. "/$defs/vital_status"."""


@dataclass(frozen=True)
class NoSchemaRule:
    glob: str
    reason: str


# --------------------------------------------------------------------------
# Which schema applies to which files.
# --------------------------------------------------------------------------

SCHEMA_MAP: tuple[SchemaRule, ...] = (
    # configs/ (templates)
    SchemaRule("configs/countries/*/country.yaml", "country.schema.json"),
    # parliament.yaml declares "Schema: country.schema.json (parliament block)".
    # It is the long form of country.yaml's government.branches.legislative.
    SchemaRule(
        "configs/countries/*/government/parliament.yaml",
        "country.schema.json",
        "/properties/government/properties/branches/properties/legislative",
    ),
    SchemaRule("configs/industries/*/industry.yaml", "industry.schema.json"),
    SchemaRule("configs/industries/*/sim/rules.yaml", "sim_config.schema.json"),
    SchemaRule(
        "configs/industries/*/sim/derived_distributions.yaml",
        "derived_distributions.schema.json",
    ),
    SchemaRule("configs/institutions/*.yaml", "institution.schema.json"),
    SchemaRule("configs/professions/*.yaml", "profession.schema.json"),
    SchemaRule("configs/worlds/*/world.config.yaml", "world.schema.json"),
    # seeds/ (instances; seeds/README.md: "both validate against the same schemas")
    SchemaRule("seeds/*/world.yaml", "world.schema.json"),
    SchemaRule("seeds/*/lots/**/*.yaml", "lot.schema.json"),
    # Gameplay venues (CC BY). OSM names and points live in odbl/, which is not
    # scanned here; cli/tests/test_odbl_dataset.py checks that layer.
    SchemaRule("seeds/*/venues/*.yaml", "venue.schema.json"),
    SchemaRule("seeds/*/*/geography/lots/**/*.yaml", "lot.schema.json"),
    SchemaRule("seeds/*/*/*/characters/**/*.yaml", "character.schema.json"),
    SchemaRule("seeds/*/*/*/contracts/*.yaml", "contract.schema.json"),
    SchemaRule("seeds/*/*/*/institutions/*.yaml", "institution.schema.json"),
    SchemaRule("seeds/*/*/regulators/*.yaml", "institution.schema.json"),
    SchemaRule("seeds/*/*/government/prime-minister.yaml", "character.schema.json"),
    SchemaRule("seeds/*/*/government/cabinet/*.yaml", "character.schema.json"),
    SchemaRule("seeds/*/*/government/civil-service/*.yaml", "character.schema.json"),
    SchemaRule("seeds/*/*/government/judiciary/*.yaml", "character.schema.json"),
    SchemaRule("seeds/*/*/government/hm-government-foxbridge.yaml", "institution.schema.json"),
    SchemaRule("seeds/*/*/government/supreme-court-of-foxbridge.yaml", "institution.schema.json"),
    SchemaRule("seeds/*/*/government/cabinet-office-foxbridge.yaml", "institution.schema.json"),
)

_COUNTRY_SUBDOC = (
    "Country-template supporting document. country.yaml references it by path "
    "or carries a short summary of it. country.schema.json has no $defs for it, "
    "and its summary blocks have a different shape"
)

NO_SCHEMA: tuple[NoSchemaRule, ...] = (
    NoSchemaRule(
        "configs/sources.yaml",
        "Provenance and licence ledger for ingested corpora (configs/README.md). "
        "No schema in schemas/ describes it.",
    ),
    NoSchemaRule(
        "configs/countries/*/economy/*.yaml",
        f"{_COUNTRY_SUBDOC}: country.schema.json only has currency.{{enabled, realm, "
        "monetary_policy}}. It has no budget or currency-policy document.",
    ),
    NoSchemaRule(
        "configs/countries/*/geography/counties/*.yaml",
        f"{_COUNTRY_SUBDOC}: territory.subdivisions[] requires level/id/name. "
        "County sketches use type + identity.name and many more fields.",
    ),
    NoSchemaRule(
        "configs/countries/*/government/cabinet-positions/*.yaml",
        f"{_COUNTRY_SUBDOC}: government.branches.executive.cabinet_positions[] "
        "requires title + portfolio (a string). Slot files use position_id and "
        "an object portfolio.",
    ),
    NoSchemaRule(
        "configs/countries/*/government/civil-service/*.yaml",
        f"{_COUNTRY_SUBDOC}: government.civil_service expects "
        "permanent_secretaries[]. The slot file uses permanent_secretary_corps + "
        "positions[].",
    ),
    NoSchemaRule(
        "configs/countries/*/laws/**/*.yaml",
        f"{_COUNTRY_SUBDOC}: laws.* are path strings, and taxation.* holds only "
        "summary rates. Tax schedules and immigration rules have their own shape "
        "(e.g. brackets[].income_above_pol rather than income_above).",
    ),
    NoSchemaRule(
        "configs/countries/*/public-services/*.yaml",
        f"{_COUNTRY_SUBDOC}: country.schema.json does not model public services.",
    ),
    NoSchemaRule(
        "configs/countries/*/regulators/*.yaml",
        f"{_COUNTRY_SUBDOC}: country.schema.json regulators.* holds only "
        "institution ids. The slot map has per-role objects.",
    ),
    NoSchemaRule(
        "configs/countries/*/treaties.yaml",
        f"{_COUNTRY_SUBDOC}: foreign_policy requires recognized_countries/allies/"
        "sanctions/treaties. This file holds treaties + posture only.",
    ),
    NoSchemaRule(
        "configs/industries/*/sim/examples/**/*.yaml",
        "Few-shot cognition examples. Their shape is polis.sim.llm_hook.Example, "
        "loaded by sim/ and polis-internal cognition/examples_loader.py. No JSON "
        "Schema exists for them.",
    ),
    NoSchemaRule(
        "seeds/*/districts/*.yaml",
        "Starter districts read by polis-internal scripts/seed_world.py. schemas/ "
        "has no district schema; lot.schema.json only references districts by id.",
    ),
)

# --------------------------------------------------------------------------
# Known failures: xfail(strict=True) until the referenced issue is fixed.
# --------------------------------------------------------------------------

_CHARACTER_NEEDS_SCALE = (
    "the-staq/polis#2: state.needs still uses the "
    "pre-v0.2.0 0-1 float axes. character.schema.json v0.2.0 requires integers "
    "from 0 to 100, where HIGH means more in need"
)
_INSTITUTION_VACANT_BOARD = (
    "the-staq/polis#3: governance.board[] seats "
    "have character_id: null, but institution.schema.json requires a string"
)
_WORLD_CONFIG_SHAPE = (
    "the-staq/polis#4: world.config.yaml claims "
    "world.schema.json v0.1.3 but is missing required blocks and uses "
    "non-schema values"
)
_STARTER_LOT_SHAPE = (
    "the-staq/polis#5: starter lots use the flat "
    "seed_world.py shape (world_id/lat/lon/district/canonical_name) instead of "
    "lot.schema.json (world/coordinates/parent_district_id, lot_ id prefix, "
    "*_price_pol)"
)
_COMMERCE_INSTITUTION_SHAPE = (
    "the-staq/polis#6: commerce institution "
    "configs lack the 10 fields that institution.schema.json requires and add "
    "name/description/district/goods"
)
_INSTITUTION_KIND_TRANSIT = (
    "the-staq/polis#7: kind 'transit' (used by the "
    "engine and by profession transit-operator) is not in the "
    "institution.schema.json kind enum, which has 'transit-operator'"
)

KNOWN_FAILURES: dict[str, str] = {
    "seeds/modern-earth-2026/england-on-polis/football/characters/footballers/adaeze-okoye.yaml": _CHARACTER_NEEDS_SCALE,
    "seeds/modern-earth-2026/england-on-polis/football/characters/managers/marquez.yaml": _CHARACTER_NEEDS_SCALE,
    "seeds/modern-earth-2026/england-on-polis/government/prime-minister.yaml": _CHARACTER_NEEDS_SCALE,
    "seeds/modern-earth-2026/england-on-polis/regulators/federation-of-hartshire.yaml": _INSTITUTION_VACANT_BOARD,
    "configs/worlds/modern-earth-2026/world.config.yaml": _WORLD_CONFIG_SHAPE,
    "seeds/modern-earth-2026/lots/camden/flat-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/camden/flat-02.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/camden/house-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/camden/studio-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/hackney/flat-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/hackney/house-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/hackney/loft-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/hackney/studio-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/stratford/flat-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/stratford/house-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/stratford/new-01.yaml": _STARTER_LOT_SHAPE,
    "seeds/modern-earth-2026/lots/stratford/studio-01.yaml": _STARTER_LOT_SHAPE,
    "configs/institutions/camden-arms-cafe.yaml": _COMMERCE_INSTITUTION_SHAPE,
    "configs/institutions/fitlab-gym-hackney.yaml": _COMMERCE_INSTITUTION_SHAPE,
    "configs/institutions/hackney-corner-grocery.yaml": _COMMERCE_INSTITUTION_SHAPE,
    "configs/institutions/hackney-kitchen.yaml": _COMMERCE_INSTITUTION_SHAPE,
    "configs/institutions/hackney-transit-authority.yaml": (
        f"{_COMMERCE_INSTITUTION_SHAPE}; {_INSTITUTION_KIND_TRANSIT}"
    ),
    "configs/institutions/the-red-lion-pub.yaml": _COMMERCE_INSTITUTION_SHAPE,
}


KNOWN_ERRORS_FILE = Path(__file__).with_name("known_schema_errors.json")


class KnownSchemaErrors(AssertionError):
    """A KNOWN_FAILURES file failed with exactly its recorded errors."""


def _known_errors() -> dict[str, list[str]]:
    if not KNOWN_ERRORS_FILE.exists():
        return {}
    return json.loads(KNOWN_ERRORS_FILE.read_text(encoding="utf-8"))


def _signature(err) -> str:
    return "/" + "/".join(str(p) for p in err.absolute_path) + " " + str(err.validator)


# --------------------------------------------------------------------------
# Discovery
# --------------------------------------------------------------------------


def _rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def _is_yaml(path: Path) -> bool:
    return path.is_file() and path.suffix in YAML_SUFFIXES


def _discover_yaml() -> list[str]:
    return sorted(
        _rel(p) for d in SCANNED_DIRS for p in (REPO_ROOT / d).rglob("*") if _is_yaml(p)
    )


def _expand(glob: str) -> set[str]:
    return {_rel(p) for p in REPO_ROOT.glob(glob) if _is_yaml(p)}


def _classify() -> dict[str, list[SchemaRule | NoSchemaRule]]:
    """Map every scanned YAML file to the table entries whose glob matches it."""
    matches: dict[str, list[SchemaRule | NoSchemaRule]] = {p: [] for p in _discover_yaml()}
    for rule in (*SCHEMA_MAP, *NO_SCHEMA):
        for path in _expand(rule.glob):
            if path in matches:  # globs may only classify files under SCANNED_DIRS
                matches[path].append(rule)
    return matches


def _validation_cases() -> list:
    """One case per file that matches exactly one SchemaRule (and nothing else)."""
    cases = []
    for path, rules in sorted(_classify().items()):
        if len(rules) != 1 or not isinstance(rules[0], SchemaRule):
            continue  # unmapped/ambiguous files are reported by test_every_yaml_is_classified
        marks = ()
        if path in KNOWN_FAILURES:
            marks = (
                pytest.mark.xfail(
                    strict=True, raises=KnownSchemaErrors, reason=KNOWN_FAILURES[path]
                ),
            )
        cases.append(pytest.param(path, rules[0], id=path, marks=marks))
    return cases


# --------------------------------------------------------------------------
# Schemas
# --------------------------------------------------------------------------


@lru_cache(maxsize=None)
def _schemas() -> dict[str, dict]:
    return {
        p.name: json.loads(p.read_text(encoding="utf-8"))
        for p in sorted(SCHEMA_DIR.glob("*.schema.json"))
    }


@lru_cache(maxsize=None)
def _registry() -> Registry:
    """All schemas, keyed by `$id`, so cross-schema `$ref`s resolve offline."""
    return Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in _schemas().values()
    ).crawl()


def _validator(rule: SchemaRule):
    schema = _schemas()[rule.schema]
    cls = validator_for(schema)
    target = {"$ref": f"{schema['$id']}#{rule.pointer}"} if rule.pointer else schema
    return cls(target, registry=_registry())


def _format_error(err) -> str:
    where = "/" + "/".join(str(p) for p in err.absolute_path) if err.absolute_path else "(root)"
    schema_where = "/".join(str(p) for p in err.absolute_schema_path)
    message = err.message if len(err.message) <= 500 else err.message[:500] + " ..."
    if isinstance(err.instance, (date, datetime)):
        message += " (YAML read an unquoted date/time; quote it to keep it a string)"
    return f"  - at {where}: {message}  [schema: {schema_where}]"


# --------------------------------------------------------------------------
# Tests: the YAML files
# --------------------------------------------------------------------------


@pytest.mark.parametrize(("path", "rule"), _validation_cases())
def test_yaml_validates_against_schema(path: str, rule: SchemaRule) -> None:
    with (REPO_ROOT / path).open(encoding="utf-8") as f:
        instance = yaml.safe_load(f)
    errors = sorted(
        _validator(rule).iter_errors(instance),
        key=lambda e: ([str(p) for p in e.absolute_path], e.message),
    )
    if path in KNOWN_FAILURES and os.environ.get("POLIS_UPDATE_KNOWN_SCHEMA_ERRORS") == "1":
        known = _known_errors()
        known[path] = sorted({_signature(e) for e in errors})
        KNOWN_ERRORS_FILE.write_text(json.dumps(known, indent=2, sort_keys=True) + "\n")
    if not errors:
        return
    target = f"schemas/{rule.schema}" + (f"#{rule.pointer}" if rule.pointer else "")
    report = (
        f"{path} does not validate against {target} ({len(errors)} error(s)):\n"
        + "\n".join(_format_error(e) for e in errors)
    )
    if path in KNOWN_FAILURES:
        expected = set(_known_errors().get(path, []))
        actual = {_signature(e) for e in errors}
        if actual == expected:
            raise KnownSchemaErrors(report)
        pytest.fail(
            f"{report}\n\nErrors differ from the known_schema_errors.json record "
            f"(new: {sorted(actual - expected)}, gone: {sorted(expected - actual)}).",
            pytrace=False,
        )
    pytest.fail(report, pytrace=False)


def test_every_yaml_is_classified() -> None:
    """Each YAML under configs/ and seeds/ matches exactly one SCHEMA_MAP or NO_SCHEMA entry."""
    problems = []
    for path, rules in sorted(_classify().items()):
        if not rules:
            problems.append(f"  - {path}: matches no SCHEMA_MAP or NO_SCHEMA entry")
        elif len(rules) > 1:
            globs = ", ".join(r.glob for r in rules)
            problems.append(f"  - {path}: matches several entries ({globs})")
    assert not problems, (
        "Add each file to SCHEMA_MAP (the schema that applies) or NO_SCHEMA (why none "
        "does) in cli/tests/test_config_schemas.py:\n" + "\n".join(problems)
    )


def test_every_table_glob_matches_files() -> None:
    """Stale globs (renamed or removed files) must be removed from the tables."""
    stale = [r.glob for r in (*SCHEMA_MAP, *NO_SCHEMA) if not _expand(r.glob)]
    assert not stale, f"Globs that match no YAML file: {stale}"


def test_known_failures_are_validation_cases() -> None:
    """Every KNOWN_FAILURES entry names a file that is actually validated."""
    validated = {p for p, rules in _classify().items() if len(rules) == 1 and isinstance(rules[0], SchemaRule)}
    stale = sorted(set(KNOWN_FAILURES) - validated)
    assert not stale, f"KNOWN_FAILURES entries that are not validated files: {stale}"
    assert set(_known_errors()) == set(KNOWN_FAILURES), (
        "known_schema_errors.json and KNOWN_FAILURES must list the same files"
    )


_HEADER_SCHEMA_RE = re.compile(r"([a-z_]+\.schema\.json)")


def _declared_schemas(path: str) -> set[str]:
    """Schema file names mentioned in the file's leading comment block."""
    declared: set[str] = set()
    with (REPO_ROOT / path).open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped in ("", "---"):
                continue
            if not stripped.startswith("#"):
                break
            declared.update(_HEADER_SCHEMA_RE.findall(stripped))
    return declared


def test_mapping_agrees_with_schema_declared_in_file_header() -> None:
    """A file whose header names a schema ("# Schema: .../x.schema.json") is validated against it."""
    problems = []
    for path, rules in sorted(_classify().items()):
        declared = _declared_schemas(path)
        if not declared or len(rules) != 1:
            continue
        rule = rules[0]
        if isinstance(rule, NoSchemaRule):
            problems.append(f"  - {path}: header names {sorted(declared)} but it is in NO_SCHEMA")
        elif rule.schema not in declared:
            problems.append(f"  - {path}: header names {sorted(declared)} but it is mapped to {rule.schema}")
    assert not problems, "\n".join(problems)


# --------------------------------------------------------------------------
# Tests: the schemas themselves
# --------------------------------------------------------------------------


@pytest.mark.parametrize("schema_file", sorted(_schemas()))
def test_schema_is_valid(schema_file: str) -> None:
    schema = _schemas()[schema_file]
    assert "$schema" in schema, f"{schema_file} does not declare $schema"
    assert schema.get("$id", "").endswith("/" + schema_file), (
        f"{schema_file}: $id {schema.get('$id')!r} should end with /{schema_file}"
    )
    validator_for(schema).check_schema(schema)


def test_schema_ids_are_unique() -> None:
    ids = [s.get("$id") for s in _schemas().values()]
    assert len(ids) == len(set(ids)), f"duplicate $id values: {ids}"


def _iter_refs(node, base: str):
    if isinstance(node, dict):
        if isinstance(node.get("$id"), str):
            base = urljoin(base, node["$id"])
        if isinstance(node.get("$ref"), str):
            yield base, node["$ref"]
        for value in node.values():
            yield from _iter_refs(value, base)
    elif isinstance(node, list):
        for value in node:
            yield from _iter_refs(value, base)


@pytest.mark.parametrize("schema_file", sorted(_schemas()))
def test_schema_refs_resolve_locally(schema_file: str) -> None:
    """Every $ref resolves through the local registry (no network, no dangling refs)."""
    unresolved = []
    for base, ref in _iter_refs(_schemas()[schema_file], ""):
        try:
            _registry().resolver(base_uri=base).lookup(ref)
        except Exception as exc:  # referencing raises several Unresolvable subclasses
            unresolved.append(f"{ref} (from {base}): {type(exc).__name__}")
    assert not unresolved, "\n".join(unresolved)


def test_schema_map_targets_exist() -> None:
    """Each SCHEMA_MAP entry names a schema file in schemas/ and, if set, a pointer that resolves."""
    problems = []
    for rule in SCHEMA_MAP:
        schema = _schemas().get(rule.schema)
        if schema is None:
            problems.append(f"{rule.glob}: schemas/{rule.schema} does not exist")
            continue
        if rule.pointer:
            try:
                _registry().resolver().lookup(f"{schema['$id']}#{rule.pointer}")
            except Exception as exc:
                problems.append(
                    f"{rule.glob}: pointer {rule.pointer} does not resolve: {type(exc).__name__}"
                )
    assert not problems, "\n".join(problems)
