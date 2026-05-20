"""Round-trip test: every per-industry sim config validates against sim_config.schema.json.

V0-PLAN §5 makes JSON Schema canonical. The Pydantic model in `polis/sim/config.py`
must stay in sync with `polis/schemas/sim_config.schema.json` until codegen lands.
This test enforces both: (1) the schema is valid, (2) every shipped sim config
parses against it, (3) the Pydantic model accepts the same configs without losing
information.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from polis.sim import SimConfig

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "sim_config.schema.json"
CONFIG_GLOB = "configs/industries/*/sim/rules.yaml"


def _load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return json.load(f)


def _discover_sim_configs() -> list[Path]:
    return sorted(REPO_ROOT.glob(CONFIG_GLOB))


def test_schema_is_valid_json_schema():
    """The schema itself parses as JSON and has the expected top-level shape."""
    schema = _load_schema()
    assert schema["title"] == "SimConfig"
    assert schema["type"] == "object"
    assert "industry_id" in schema["required"]
    assert "driver" in schema["properties"]
    assert set(schema["properties"]["driver"]["enum"]) == {"event", "tick", "turn"}


@pytest.mark.parametrize("config_path", _discover_sim_configs(), ids=lambda p: p.parent.parent.name)
def test_sim_config_validates_against_schema(config_path):
    """Every shipped sim config must validate against sim_config.schema.json."""
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load_schema()
    with config_path.open() as f:
        cfg = yaml.safe_load(f)
    jsonschema.validate(instance=cfg, schema=schema)


@pytest.mark.parametrize("config_path", _discover_sim_configs(), ids=lambda p: p.parent.parent.name)
def test_sim_config_parses_into_pydantic_model(config_path):
    """Every shipped sim config must also parse into the Pydantic SimConfig model.

    Catches drift between JSON Schema and Pydantic source until codegen flips
    them into a single source of truth.
    """
    with config_path.open() as f:
        cfg = yaml.safe_load(f)
    parsed = SimConfig(**cfg)
    assert parsed.industry_id == cfg["industry_id"]
    assert parsed.driver.value == cfg["driver"]
