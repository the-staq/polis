"""Smoke + determinism tests for the sim kernel.

Determinism is the load-bearing property — calibration suites (V0-PLAN §7 gap 1)
depend on bit-identical EventLogs across runs with the same seed + stub hook.
"""

from __future__ import annotations

import pytest

from polis.sim import (
    DriverType,
    EndCondition,
    EndConditionType,
    EventSpec,
    SeededRandom,
    Sim,
    SimConfig,
    StubLLMHook,
    run_sim,
)


# --- Minimal noop handler so configs validate -------------------------------


async def _noop_bootstrap(sim: Sim, _ctx) -> None:
    sim.emit(actor_id=None, action_type="started", payload={})
    sim.schedule(1.0, _tick)


async def _tick(sim: Sim, _ctx) -> None:
    sim.emit(actor_id="ticker", action_type="tick", payload={"n": sim.rng.integer(1, 100)})
    if sim.now < 5.0:
        sim.schedule(1.0, _tick)


@pytest.fixture
def minimal_config():
    return SimConfig(
        industry_id="test-noop",
        driver=DriverType.EVENT,
        end_condition=EndCondition(type=EndConditionType.DURATION, sim_seconds=10.0),
        roles=[],
        initial_state={"counter": 0},
        events=[
            EventSpec(id="bootstrap", handler="polis.sim.tests.test_kernel._noop_bootstrap"),
            EventSpec(id="tick", handler="polis.sim.tests.test_kernel._tick"),
        ],
    )


# --- Tests ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_kernel_boots_and_runs(minimal_config):
    """Sim resets, runs, returns a FinalState."""
    rng = SeededRandom(seed=42)
    hook = StubLLMHook(rng=rng)
    final = await run_sim(minimal_config, seed=42, llm_hook=hook)
    assert final.sim_time >= 5.0
    assert final.seed == 42
    assert len(final.event_log) >= 1


@pytest.mark.asyncio
async def test_kernel_emits_events_in_order(minimal_config):
    """Events come out in monotonically non-decreasing sim_time order."""
    rng = SeededRandom(seed=42)
    hook = StubLLMHook(rng=rng)
    final = await run_sim(minimal_config, seed=42, llm_hook=hook)
    times = [e.sim_time for e in final.event_log]
    assert times == sorted(times), f"events out of order: {times}"


@pytest.mark.asyncio
async def test_kernel_is_deterministic_under_same_seed(minimal_config):
    """Two runs with the same seed + stub hook produce identical event logs.

    This is the load-bearing property — calibration suites depend on it.
    """
    rng1 = SeededRandom(seed=42)
    hook1 = StubLLMHook(rng=rng1)
    final1 = await run_sim(minimal_config, seed=42, llm_hook=hook1)

    rng2 = SeededRandom(seed=42)
    hook2 = StubLLMHook(rng=rng2)
    final2 = await run_sim(minimal_config, seed=42, llm_hook=hook2)

    assert len(final1.event_log) == len(final2.event_log)
    for e1, e2 in zip(final1.event_log, final2.event_log, strict=True):
        assert e1.sim_time == e2.sim_time
        assert e1.action_type == e2.action_type
        assert e1.actor_id == e2.actor_id
        assert e1.payload == e2.payload


@pytest.mark.asyncio
async def test_kernel_diverges_under_different_seed(minimal_config):
    """Different seeds produce different RNG-driven payloads."""
    rng1 = SeededRandom(seed=42)
    rng2 = SeededRandom(seed=99)
    final1 = await run_sim(minimal_config, seed=42, llm_hook=StubLLMHook(rng=rng1))
    final2 = await run_sim(minimal_config, seed=99, llm_hook=StubLLMHook(rng=rng2))

    payloads1 = [e.payload.get("n") for e in final1.event_log if e.action_type == "tick"]
    payloads2 = [e.payload.get("n") for e in final2.event_log if e.action_type == "tick"]
    assert payloads1 != payloads2, "different seeds should produce different rng payloads"


@pytest.mark.asyncio
async def test_kernel_respects_end_condition(minimal_config):
    """Duration end condition stops the sim at or after sim_seconds."""
    rng = SeededRandom(seed=42)
    final = await run_sim(minimal_config, seed=42, llm_hook=StubLLMHook(rng=rng))
    assert final.sim_time <= 11.0, f"ran past end condition: {final.sim_time}"


@pytest.mark.asyncio
async def test_event_log_filter_and_last(minimal_config):
    """EventLog helpers work for inspection."""
    rng = SeededRandom(seed=42)
    final = await run_sim(minimal_config, seed=42, llm_hook=StubLLMHook(rng=rng))
    ticks = final.event_log.filter(action_type="tick")
    assert len(ticks) >= 1
    last_tick = final.event_log.last(action_type="tick")
    assert last_tick is not None
    assert last_tick.action_type == "tick"
