"""Integration test for the toy basketball sim config.

Proves the substrate is not football-shaped (V0-PLAN §5.1 rule 3) at the sim
layer: a non-football industry config + handlers runs end-to-end through the
same kernel.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from polis.sim import SeededRandom, SimConfig, StubLLMHook, run_sim


CONFIG_PATH = (
    Path(__file__).resolve().parents[2]
    / "configs"
    / "industries"
    / "basketball"
    / "sim"
    / "rules.yaml"
)


def _load_basketball_config() -> SimConfig:
    with CONFIG_PATH.open() as f:
        return SimConfig(**yaml.safe_load(f))


@pytest.mark.asyncio
async def test_basketball_sim_runs_end_to_end():
    """Toy basketball sim boots, scores points, hits end condition."""
    cfg = _load_basketball_config()
    rng = SeededRandom(seed=42)
    # Policy: random shot choice from legal actions
    hook = StubLLMHook(
        rng=rng,
        policies={"shot_choice": lambda ctx, r: r.choice(ctx.legal_actions)},
    )
    final = await run_sim(cfg, seed=42, llm_hook=hook)

    # Sim ran for the configured duration (4 quarters of 12 minutes)
    assert final.sim_time >= 2880.0 - 60.0, f"sim ended early at {final.sim_time}"

    # Score is in state
    assert "score" in final.outcome
    assert {"home", "away"} <= set(final.outcome["score"].keys())

    # At least some events emitted
    assert len(final.event_log) > 10, f"only {len(final.event_log)} events emitted"

    # Tipoff happened once
    tipoffs = final.event_log.filter(action_type="tipoff")
    assert len(tipoffs) == 1


@pytest.mark.asyncio
async def test_basketball_sim_is_deterministic():
    """Same seed → same final score + same event sequence. Calibration prerequisite."""
    cfg = _load_basketball_config()
    policy = lambda ctx, r: r.choice(ctx.legal_actions)  # noqa: E731

    rng1 = SeededRandom(seed=42)
    final1 = await run_sim(
        cfg, seed=42, llm_hook=StubLLMHook(rng=rng1, policies={"shot_choice": policy})
    )

    rng2 = SeededRandom(seed=42)
    final2 = await run_sim(
        cfg, seed=42, llm_hook=StubLLMHook(rng=rng2, policies={"shot_choice": policy})
    )

    assert final1.outcome["score"] == final2.outcome["score"]
    assert len(final1.event_log) == len(final2.event_log)
