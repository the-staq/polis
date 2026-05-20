"""Football match sim handlers — examples + LLM-as-environment driven.

Per DECISION-CALIBRATION-SOURCE.md: realistic sim behavior comes from
community-authored few-shot example YAMLs in `./examples/` rather than
commercial statistical corpora. The placeholder `./derived_distributions.yaml`
stays as the deterministic CI / fast-path fallback (stub LLM hooks use Poisson
rates from it; real LLM hooks use the examples).

The dual-path architecture:
  - StubLLMHook (CI, deterministic) → Poisson sampling against placeholder rates
  - Real LLM hook (V0.5+, polis-internal) → LLM-as-environment with few-shot
    examples filtered by event type, era, region

Both paths share the same handler code. The handler loads BOTH examples and
rates at bootstrap; the LLMHook implementation decides which to consume via
the `examples` field on DecisionContext (stubs ignore it; real LLM hooks
format it into prompts).

This file plugs into the substrate sim kernel via file-path handler refs in
`./rules.yaml` (e.g., `./handlers.py::bootstrap`). The kernel runs everything
else: heapq event queue, deterministic seeding, LLM-hook decision dispatch.

Per V0-PLAN §5.1 rules:
- Rule 1 (kernel never knows football): all football-specific logic lives here
- Rule 3 (substrate is not football-shaped): basketball + football share the kernel
- Rule 4 (calibration as discipline): stub-hook tests verify event-count means
  within tolerance of placeholder distribution means; real-LLM-hook calibration
  is a separate V0.5+ test (judge-LLM rates the narrative quality)
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from polis.sim import Action, DecisionContext, Example, Sim


MATCH_DURATION_SECONDS = 5400.0  # 90 minutes
HALF_TIME_AT_SECONDS = 2700.0    # 45 minutes


@lru_cache(maxsize=8)
def _load_examples(config_dir_str: str) -> dict[str, tuple[Example, ...]]:
    """Walk ./examples/ subdirs and load all YAMLs, indexed by event_type.

    Returns a dict mapping event_type → tuple of Example objects sorted by
    filename (so 01-xxx comes before 02-yyy).

    lru_cached by config_dir path. Examples are versioned in git; treat as
    immutable per-process. Restart to pick up changes.

    Per DECISION-CALIBRATION-SOURCE.md: contributors can add new example
    YAMLs in any event-type subdirectory and they're picked up on next sim
    run — no engine code changes, no schema migration.
    """
    examples_dir = Path(config_dir_str) / "examples"
    if not examples_dir.exists():
        return {}

    by_event_type: dict[str, list[Example]] = {}
    for event_dir in sorted(p for p in examples_dir.iterdir() if p.is_dir()):
        event_type = event_dir.name
        examples_for_type: list[Example] = []
        for yaml_file in sorted(event_dir.glob("*.yaml")):
            try:
                with yaml_file.open() as f:
                    doc = yaml.safe_load(f) or {}
                examples_for_type.append(
                    Example(
                        id=doc.get("id", yaml_file.stem),
                        event_type=event_type,
                        name=doc.get("name", ""),
                        category=doc.get("category", ""),
                        difficulty=doc.get("difficulty", ""),
                        mechanics=tuple(doc.get("mechanics", []) or []),
                        typical_outcomes=tuple(doc.get("typical_outcomes", []) or []),
                        narrative_examples=tuple(doc.get("narrative_examples", []) or []),
                        metadata=dict(doc.get("metadata", {}) or {}),
                    )
                )
            except Exception as e:  # noqa: BLE001 — bad example shouldn't kill bootstrap
                print(f"skipping malformed example {yaml_file}: {e}")
        if examples_for_type:
            by_event_type[event_type] = tuple(examples_for_type)
    return by_event_type


def _examples_for(
    examples_by_type: dict[str, tuple[Example, ...]],
    event_type: str,
    *,
    max_n: int = 5,
) -> tuple[Example, ...]:
    """Return up to N examples for the given event type. V0: first N by filename.

    V0.5+ enhancement: filter by current match state (era, region, score
    state, time-of-game), select diverse examples to fit prompt budget.
    """
    pool = examples_by_type.get(event_type, ())
    return pool[:max_n]


@lru_cache(maxsize=8)
def _load_rates(config_dir_str: str) -> dict[str, Any]:
    """Load + memoize derived_distributions.yaml from the sim_config directory.

    Cached by config_dir path so concurrent / repeated sim runs don't re-read
    the file. Cache key is the resolved path string; if the file changes on
    disk between cached reads, restart the process (intentional — file is
    treated as immutable per-version, like a compiled artifact).
    """
    dist_path = Path(config_dir_str) / "derived_distributions.yaml"
    if not dist_path.exists():
        raise FileNotFoundError(
            f"football sim requires derived_distributions.yaml next to rules.yaml; "
            f"expected at {dist_path}. Hand-authored placeholder ships at "
            f"polis/configs/industries/football-modern-earth/sim/; "
            f"real values come from polis-internal/app/retrieval/ingestion/football/."
        )
    with dist_path.open() as f:
        doc = yaml.safe_load(f)

    metrics = doc["metrics"]
    goals = metrics["goals_per_match"]["mean"]
    shots = metrics["shots_per_match"]["mean"]
    fouls = metrics["fouls_per_match"]["mean"]
    yellows = metrics["yellow_cards_per_match"]["mean"]
    reds = metrics["red_cards_per_match"]["mean"]
    sot = metrics["shots_on_target_per_match"]["mean"]

    # Per-second arrival rate for the combined match-event Poisson process.
    # `match_events` = shots + fouls treated as the universe of "something
    # noteworthy happens" arrivals across 90 min.
    match_events_rate = (shots + fouls) / MATCH_DURATION_SECONDS
    p_shot_given_event = shots / max(1.0, shots + fouls)

    # Per-shot conversion (goal | shot). xG mean is a finer-grained alternative
    # but per-shot conversion is what calibration tests check.
    p_goal_given_shot = goals / max(1.0, shots)
    p_on_target_given_shot = sot / max(1.0, shots)

    # Per-foul card probabilities. Yellow + red are stochastically independent
    # per the placeholder (real corpus would have a joint distribution).
    p_yellow_given_foul = yellows / max(1.0, fouls)
    p_red_given_foul = reds / max(1.0, fouls)

    return {
        "match_events_per_second": match_events_rate,
        "p_shot_given_event": p_shot_given_event,
        "p_goal_given_shot": p_goal_given_shot,
        "p_on_target_given_shot": p_on_target_given_shot,
        "p_yellow_given_foul": p_yellow_given_foul,
        "p_red_given_foul": p_red_given_foul,
        "source_id": doc["source_id"],
        "provenance": doc["provenance"],
    }


def _sample_inter_arrival(sim: Sim, rate_per_second: float) -> float:
    """Sample exponential inter-arrival time from a Poisson process. Returns
    seconds until the next event. Uses sim.rng for determinism."""
    if rate_per_second <= 0:
        return float("inf")
    u = sim.rng.uniform(1e-9, 1.0)  # avoid log(0); 1e-9 sentinel
    return -math.log(u) / rate_per_second


def _other_team(team: str) -> str:
    return "away" if team == "home" else "home"


async def bootstrap(sim: Sim, _ctx: Action | None) -> None:
    """Kick the match off. Loads rates + examples, emits kickoff, schedules first event."""
    rates = _load_rates(str(sim.config_dir))
    examples = _load_examples(str(sim.config_dir))
    sim.state["__rates"] = rates  # handlers read this; calibration tests ignore _-prefixed
    sim.state["__examples"] = examples
    sim.state["__example_counts"] = {k: len(v) for k, v in examples.items()}
    sim.state["score"] = {"home": 0, "away": 0}
    sim.state["yellows"] = {"home": 0, "away": 0}
    sim.state["reds"] = {"home": 0, "away": 0}
    sim.state["shots"] = {"home": 0, "away": 0}
    sim.state["shots_on_target"] = {"home": 0, "away": 0}
    sim.state["fouls"] = {"home": 0, "away": 0}
    sim.state["half"] = 1
    sim.state["possession"] = "home"

    sim.emit(
        actor_id=None,
        action_type="kickoff",
        payload={"team": "home", "source_id": rates["source_id"], "provenance": rates["provenance"]},
    )
    sim.schedule(HALF_TIME_AT_SECONDS, half_time)
    sim.schedule(MATCH_DURATION_SECONDS, final_whistle)
    _schedule_next_match_event(sim)


def _schedule_next_match_event(sim: Sim) -> None:
    """Schedule the next match event from the Poisson arrival distribution."""
    rates = sim.state["__rates"]
    delta = _sample_inter_arrival(sim, rates["match_events_per_second"])
    if sim.now + delta >= MATCH_DURATION_SECONDS:
        # No more events this match; final_whistle is already scheduled.
        return
    sim.schedule(delta, match_event)


async def match_event(sim: Sim, _ctx: Action | None) -> None:
    """A noteworthy match event happens. Pick shot vs foul, dispatch."""
    rates = sim.state["__rates"]
    sim.state["possession"] = _other_team(sim.state["possession"]) if sim.rng.bernoulli(0.4) else sim.state["possession"]
    if sim.rng.bernoulli(rates["p_shot_given_event"]):
        await shot_attempt(sim, None)
    else:
        await foul(sim, None)


async def shot_attempt(sim: Sim, _ctx: Action | None) -> None:
    """A shot is taken. Decision point: shot kind chosen via LLM hook.

    Real LLM hooks (V0.5+) receive few-shot examples from ./examples/shot/
    via the DecisionContext.examples field — used as anchors for narrative
    generation. Stub hooks ignore examples and pick from legal_actions.
    """
    team = sim.state["possession"]
    rates = sim.state["__rates"]
    examples_by_type = sim.state.get("__examples", {})

    decision = await sim.llm_hook.decide(
        DecisionContext(
            sim_time=sim.now,
            character_id=f"{team}_striker",
            decision_type="shot_choice",
            legal_actions=["shoot_close", "shoot_far", "pass_back"],
            state={"score": dict(sim.state["score"]), "team": team, "minute": int(sim.now / 60)},
            examples=_examples_for(examples_by_type, "shot"),
        )
    )

    if decision.action_type == "pass_back":
        sim.emit(actor_id=f"{team}_striker", action_type="pass", payload={"team": team})
        _schedule_next_match_event(sim)
        return

    sim.state["shots"][team] += 1
    sim.emit(
        actor_id=f"{team}_striker",
        action_type="shot",
        payload={"team": team, "kind": decision.action_type, "minute": int(sim.now / 60)},
    )

    # Distance multipliers — close-range shots more likely to be on-target AND
    # convert. Multipliers are heuristic; the BASE rates still come from the
    # corpus. Calibration sees aggregate rates; individual-shot bias is
    # operator-tunable later. (Real V0.5+ enhancement: per-shot xG model.)
    is_close = decision.action_type == "shoot_close"
    on_target_p = min(0.99, rates["p_on_target_given_shot"] * (1.4 if is_close else 0.7))
    goal_p = min(0.99, rates["p_goal_given_shot"] * (1.7 if is_close else 0.5))

    if sim.rng.bernoulli(on_target_p):
        sim.state["shots_on_target"][team] += 1
        if sim.rng.bernoulli(goal_p / max(on_target_p, 1e-6)):
            await _score(sim, team, decision.action_type)
        else:
            sim.emit(actor_id=f"{team}_goalkeeper", action_type="save",
                     payload={"team": _other_team(team), "shot_kind": decision.action_type})
    else:
        sim.emit(actor_id=f"{team}_striker", action_type="shot_miss",
                 payload={"team": team, "shot_kind": decision.action_type})

    _schedule_next_match_event(sim)


async def _score(sim: Sim, team: str, shot_kind: str) -> None:
    sim.state["score"][team] += 1
    sim.emit(
        actor_id=f"{team}_striker",
        action_type="goal",
        payload={
            "team": team,
            "shot_kind": shot_kind,
            "minute": int(sim.now / 60),
            "new_score": dict(sim.state["score"]),
        },
    )


async def foul(sim: Sim, _ctx: Action | None) -> None:
    """A foul occurs. Roll for cards using corpus-derived rates."""
    rates = sim.state["__rates"]
    perpetrator = _other_team(sim.state["possession"])  # the defender commits
    sim.state["fouls"][perpetrator] += 1
    sim.emit(
        actor_id=f"{perpetrator}_defender",
        action_type="foul",
        payload={"team": perpetrator, "minute": int(sim.now / 60)},
    )

    if sim.rng.bernoulli(rates["p_red_given_foul"]):
        sim.state["reds"][perpetrator] += 1
        sim.emit(
            actor_id=f"{perpetrator}_defender",
            action_type="card",
            payload={"team": perpetrator, "color": "red", "minute": int(sim.now / 60)},
        )
    elif sim.rng.bernoulli(rates["p_yellow_given_foul"]):
        sim.state["yellows"][perpetrator] += 1
        sim.emit(
            actor_id=f"{perpetrator}_defender",
            action_type="card",
            payload={"team": perpetrator, "color": "yellow", "minute": int(sim.now / 60)},
        )

    _schedule_next_match_event(sim)


async def half_time(sim: Sim, _ctx: Action | None) -> None:
    """At minute 45 — emit half_time event, transition state."""
    sim.state["half"] = 2
    sim.emit(
        actor_id=None,
        action_type="half_time",
        payload={"score_at_break": dict(sim.state["score"])},
    )


async def final_whistle(sim: Sim, _ctx: Action | None) -> None:
    """At minute 90 — emit final_whistle, end sim with result."""
    home = sim.state["score"]["home"]
    away = sim.state["score"]["away"]
    if home > away:
        outcome = "home_win"
    elif away > home:
        outcome = "away_win"
    else:
        outcome = "draw"
    sim.emit(
        actor_id=None,
        action_type="final_whistle",
        payload={
            "final_score": dict(sim.state["score"]),
            "outcome": outcome,
        },
    )
    sim.end(outcome={"outcome": outcome})
