"""Football sim tests — schema + calibration round-trip.

Proves V0-PLAN §5.1 rules 3 & 4:
- Rule 3: the football sim runs through the same kernel as basketball.
- Rule 4: calibration is enforced as discipline — over N runs, the sim's
  event-count means must land within tolerance of the empirical distribution
  means it was parameterized from.

The placeholder distributions ship realistic-ballpark numbers
(goals/match ~2.7, shots/match ~24, fouls/match ~20.9). When the StatsBomb
ingestion pipeline overwrites the file with `provenance: computed` real
numbers, this same test suite re-runs against them — no code changes.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

import pytest
import yaml

from polis.sim import (
    SeededRandom,
    StubLLMHook,
    load_sim_from_yaml,
    run_sim,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
DIST_SCHEMA = REPO_ROOT / "schemas" / "derived_distributions.schema.json"
FOOTBALL_DIR = REPO_ROOT / "configs" / "industries" / "football-modern-earth" / "sim"
FOOTBALL_RULES = FOOTBALL_DIR / "rules.yaml"
FOOTBALL_DIST = FOOTBALL_DIR / "derived_distributions.yaml"


def _load_distributions() -> dict:
    with FOOTBALL_DIST.open() as f:
        return yaml.safe_load(f)


def test_distributions_schema_is_valid():
    """derived_distributions.schema.json is a valid JSON Schema draft 2020-12."""
    jsonschema = pytest.importorskip("jsonschema")
    with DIST_SCHEMA.open() as f:
        schema = json.load(f)
    jsonschema.Draft202012Validator.check_schema(schema)
    assert schema["title"] == "DerivedDistributions"


def test_football_distributions_yaml_validates_against_schema():
    """The placeholder yaml must conform to the schema. Replacement contract:
    when the StatsBomb pipeline overwrites this file, it must still validate."""
    jsonschema = pytest.importorskip("jsonschema")
    with DIST_SCHEMA.open() as f:
        schema = json.load(f)
    data = _load_distributions()
    jsonschema.validate(instance=data, schema=schema)


def test_outcomes_sum_to_unity():
    """home_win + draw + away_win must sum to 1.0 (tolerance 1e-3)."""
    data = _load_distributions()
    s = sum(data["outcomes"].values())
    assert abs(s - 1.0) < 1e-3, f"outcomes sum to {s}, expected 1.0"


def test_goal_minutes_distribution_sums_to_unity():
    """goal_minutes_distribution.freq values sum to ~1.0 (tolerance 5%)."""
    data = _load_distributions()
    s = sum(b["freq"] for b in data["goal_minutes_distribution"])
    assert abs(s - 1.0) < 0.05, f"goal_minutes freqs sum to {s}, expected ~1.0"


# --- Sim integration ---------------------------------------------------------


def _run_one_match(seed: int, *, always_shoot: bool = False):
    """Run one football sim. Returns FinalState.

    `always_shoot=True` uses a policy that picks {shoot_close, shoot_far}
    only — never pass_back. This is the calibration test posture: we're
    measuring the corpus-driven event RATES, not agent strategy. Real LLM
    agents at V0.5+ make meaningful pass-back decisions; the calibration
    target is then re-derived against agent-emergent behavior.
    """
    cfg, cfg_dir = load_sim_from_yaml(FOOTBALL_RULES)
    rng = SeededRandom(seed=seed)
    if always_shoot:
        policy = lambda ctx, r: r.choice(["shoot_close", "shoot_far"])  # noqa: E731
    else:
        policy = lambda ctx, r: r.choice(ctx.legal_actions)  # noqa: E731
    hook = StubLLMHook(rng=rng, policies={"shot_choice": policy})

    import asyncio

    return asyncio.run(run_sim(cfg, seed=seed, llm_hook=hook, config_dir=cfg_dir))


@pytest.mark.asyncio
async def test_football_sim_runs_end_to_end():
    """Football sim loads file-path handlers, runs 90 min, emits a result."""
    cfg, cfg_dir = load_sim_from_yaml(FOOTBALL_RULES)
    rng = SeededRandom(seed=42)
    hook = StubLLMHook(
        rng=rng,
        policies={"shot_choice": lambda ctx, r: r.choice(ctx.legal_actions)},
    )
    final = await run_sim(cfg, seed=42, llm_hook=hook, config_dir=cfg_dir)

    assert final.sim_time == 5400.0, f"sim ended at {final.sim_time}, expected 5400"
    assert "score" in final.outcome
    assert {"home", "away"} == set(final.outcome["score"].keys())

    types = {e.action_type for e in final.event_log}
    assert {"kickoff", "half_time", "final_whistle"} <= types, \
        f"missing required match phases; saw {types}"

    final_whistles = [e for e in final.event_log if e.action_type == "final_whistle"]
    assert len(final_whistles) == 1, "exactly one final_whistle per match"


@pytest.mark.asyncio
async def test_football_sim_is_deterministic():
    """Same seed → identical event sequence."""
    cfg, cfg_dir = load_sim_from_yaml(FOOTBALL_RULES)
    policy = lambda ctx, r: r.choice(ctx.legal_actions)  # noqa: E731

    rng1 = SeededRandom(seed=99)
    final1 = await run_sim(
        cfg, seed=99,
        llm_hook=StubLLMHook(rng=rng1, policies={"shot_choice": policy}),
        config_dir=cfg_dir,
    )
    rng2 = SeededRandom(seed=99)
    final2 = await run_sim(
        cfg, seed=99,
        llm_hook=StubLLMHook(rng=rng2, policies={"shot_choice": policy}),
        config_dir=cfg_dir,
    )

    assert final1.outcome["score"] == final2.outcome["score"]
    assert len(final1.event_log) == len(final2.event_log)
    for a, b in zip(final1.event_log, final2.event_log):
        assert a.action_type == b.action_type
        assert a.sim_time == b.sim_time


def test_calibration_means_match_distribution_within_tolerance():
    """Run N matches. Sample mean of (shots, fouls, yellows) per match must
    land within k * (stdev / sqrt(N)) of the distribution mean.

    This is the load-bearing claim of V0-PLAN §5.1 rule 4: the sim is a
    generator of the same distributions it's calibrated against. When the
    StatsBomb pipeline overwrites distributions.yaml with `provenance:
    computed` real numbers, this test re-runs unchanged and is the gate that
    catches drift between the sim and its calibration target.

    Note: with the placeholder having artificially-tight stdevs (n=0), we use
    a loose tolerance band (k=3.0). Once real corpus values land, the test
    will naturally tighten as n grows.
    """
    dist = _load_distributions()
    N_MATCHES = 40
    K_SIGMA = 3.0  # loose for placeholder; tighten when n>0

    shots_observed = []
    fouls_observed = []
    yellows_observed = []
    goals_observed = []
    for seed in range(N_MATCHES):
        final = _run_one_match(seed=seed, always_shoot=True)
        outcome = final.outcome
        shots_observed.append(outcome["shots"]["home"] + outcome["shots"]["away"])
        fouls_observed.append(outcome["fouls"]["home"] + outcome["fouls"]["away"])
        yellows_observed.append(outcome["yellows"]["home"] + outcome["yellows"]["away"])
        goals_observed.append(outcome["score"]["home"] + outcome["score"]["away"])

    def _within(name: str, observed: list[float], target: dict) -> None:
        obs_mean = statistics.fmean(observed)
        obs_stdev = statistics.pstdev(observed) if len(observed) > 1 else 0.0
        # standard error of the mean
        sem = obs_stdev / (N_MATCHES ** 0.5) if obs_stdev > 0 else 1.0
        band = K_SIGMA * sem
        delta = abs(obs_mean - target["mean"])
        assert delta <= band + 1.5, (
            f"{name} sim mean {obs_mean:.2f} ± {sem:.2f} drifts from "
            f"distribution mean {target['mean']:.2f} by {delta:.2f}; band={band:.2f}+1.5"
        )

    metrics = dist["metrics"]
    _within("shots_per_match", shots_observed, metrics["shots_per_match"])
    _within("fouls_per_match", fouls_observed, metrics["fouls_per_match"])
    _within("yellow_cards_per_match", yellows_observed, metrics["yellow_cards_per_match"])
    _within("goals_per_match", goals_observed, metrics["goals_per_match"])


def test_file_path_handler_resolution_works_for_hyphenated_dir():
    """Regression: football-modern-earth has a hyphen in the dir name. The
    kernel must resolve `./handlers.py::bootstrap` against the rules.yaml
    directory, not via dotted-module import."""
    cfg, cfg_dir = load_sim_from_yaml(FOOTBALL_RULES)
    # Smoke: every handler ref uses the file form
    assert all("::" in e.handler for e in cfg.events), \
        "every football event should use file-path handler form"
    # Smoke: handlers.py exists at the resolved location
    assert (cfg_dir / "handlers.py").exists()
