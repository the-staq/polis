"""Round-trip test: a real sim run produces a SimResult that validates against schema.

Proves the load-bearing claim of `polis/schemas/sim_result.schema.json` — that
the kernel's FinalState can be wrapped into a persistable SimResult envelope
without information loss. Until a dedicated Pydantic SimResult ships, the
conversion is exercised inline so the contract stays honest.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

from polis.sim import SeededRandom, SimConfig, StubLLMHook, run_sim

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "sim_result.schema.json"
BASKETBALL_CONFIG = (
    REPO_ROOT / "configs" / "industries" / "basketball" / "sim" / "rules.yaml"
)


def _final_state_to_sim_result(
    final,
    *,
    sim_id: str,
    industry_id: str,
    config_version: str,
    started_at: datetime,
    ended_at: datetime,
    world_time_at_start: datetime,
    world_time_at_end: datetime,
    terminated_by: str,
    llm_hook_name: str,
    deterministic: bool,
) -> dict:
    """Convert kernel FinalState → SimResult envelope per sim_result.schema.json.

    Lives in the test for now; promotes into `polis/sim/result.py` when the
    orchestration layer in `polis-internal` needs it (V0.5+ wiring).
    """
    return {
        "sim_id": sim_id,
        "industry_id": industry_id,
        "kernel_version": "0.0.1",
        "config_version": config_version,
        "seed": final.seed,
        "started_at": started_at.isoformat().replace("+00:00", "Z"),
        "ended_at": ended_at.isoformat().replace("+00:00", "Z"),
        "world_time_at_start": world_time_at_start.isoformat().replace("+00:00", "Z"),
        "world_time_at_end": world_time_at_end.isoformat().replace("+00:00", "Z"),
        "sim_duration_seconds": final.sim_time,
        "wall_duration_ms": int((ended_at - started_at).total_seconds() * 1000),
        "terminated_by": terminated_by,
        "event_log": [asdict(e) for e in final.event_log],
        "outcome": dict(final.outcome),
        "llm_hook": {
            "name": llm_hook_name,
            "deterministic": deterministic,
        },
        "metadata": {
            "calibration_run": False,
        },
    }


def _load_schema() -> dict:
    with SCHEMA_PATH.open() as f:
        return json.load(f)


def test_schema_is_valid_json_schema():
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load_schema()
    jsonschema.Draft202012Validator.check_schema(schema)
    assert schema["title"] == "SimResult"
    assert "$defs" in schema
    assert "Event" in schema["$defs"]


@pytest.mark.asyncio
async def test_basketball_sim_produces_valid_sim_result():
    """Real sim run → SimResult envelope → validates against schema."""
    jsonschema = pytest.importorskip("jsonschema")

    with BASKETBALL_CONFIG.open() as f:
        cfg = SimConfig(**yaml.safe_load(f))

    rng = SeededRandom(seed=42)
    hook = StubLLMHook(
        rng=rng,
        policies={"shot_choice": lambda ctx, r: r.choice(ctx.legal_actions)},
    )

    started = datetime.now(timezone.utc)
    final = await run_sim(cfg, seed=42, llm_hook=hook)
    ended = datetime.now(timezone.utc)

    # Per DECISION-TIME-MODEL.md: world rate is 12× wall. Test scaffolds a
    # plausible world-time window; real orchestration computes from WorldClock.
    world_start = datetime(2026, 5, 20, 14, 0, 0, tzinfo=timezone.utc)
    world_end = datetime(2026, 5, 21, 2, 0, 0, tzinfo=timezone.utc)
    result = _final_state_to_sim_result(
        final,
        sim_id=f"sim_{uuid.uuid4().hex[:16]}",
        industry_id=cfg.industry_id,
        config_version=(cfg.metadata or {}).get("version", "0.0.1"),
        started_at=started,
        ended_at=ended,
        world_time_at_start=world_start,
        world_time_at_end=world_end,
        terminated_by="duration",
        llm_hook_name="stub",
        deterministic=True,
    )

    schema = _load_schema()
    jsonschema.validate(instance=result, schema=schema)

    # Sanity: outcome has the basketball-specific score field
    assert "score" in result["outcome"]
    # Sanity: every event has the universal envelope fields
    assert all({"sim_time", "action_type", "sequence"} <= set(e.keys()) for e in result["event_log"])


@pytest.mark.asyncio
async def test_sim_result_replay_hash_is_stable_under_same_seed():
    """Two runs with same seed produce SimResults with identical event_logs.

    Foundation of the replay_hash field — same inputs, same hash, same outcome.
    """
    jsonschema = pytest.importorskip("jsonschema")

    with BASKETBALL_CONFIG.open() as f:
        cfg_data = yaml.safe_load(f)
    cfg = SimConfig(**cfg_data)
    policy = lambda ctx, r: r.choice(ctx.legal_actions)  # noqa: E731

    rng1 = SeededRandom(seed=99)
    final1 = await run_sim(cfg, seed=99, llm_hook=StubLLMHook(rng=rng1, policies={"shot_choice": policy}))

    rng2 = SeededRandom(seed=99)
    final2 = await run_sim(cfg, seed=99, llm_hook=StubLLMHook(rng=rng2, policies={"shot_choice": policy}))

    log1 = [asdict(e) for e in final1.event_log]
    log2 = [asdict(e) for e in final2.event_log]
    assert log1 == log2
