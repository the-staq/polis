"""Toy basketball sim handlers.

Demonstrates the kernel contract: handlers receive a `Sim` instance, mutate
state, emit events, and schedule follow-up events. Configs reference these
via dotted Python paths in `events[].handler`.

This is NOT a real basketball sim — probabilities are deliberately uniform
and the play model is trivially simple. The point is to prove the kernel
runs end-to-end with a non-football industry.
"""

from __future__ import annotations

from polis.sim import Action, DecisionContext, Sim


# Handler signature: async def handler(sim: Sim, ctx: Action | None) -> None
# - `sim` is the kernel instance — read sim.state, sim.rng, sim.now; mutate via
#   sim.emit(), sim.schedule(), sim.end()
# - `ctx` is the Action returned by the LLM hook for decision_point events,
#   or None for non-decision events. The handler decides what to do with it.


async def bootstrap(sim: Sim, _ctx: Action | None) -> None:
    """Kick off the game. Scheduled once at sim start by run_sim()."""
    sim.emit(actor_id=None, action_type="tipoff", payload={"won_by": sim.state["possession"]})
    sim.schedule(0.0, possession_change)


async def possession_change(sim: Sim, _ctx: Action | None) -> None:
    """A team gets the ball. Schedule a shot attempt 15s later (toy timing)."""
    if sim.now >= sim.config.end_condition.sim_seconds:
        sim.end()
        return
    sim.emit(
        actor_id=None,
        action_type="possession_change",
        payload={"team": sim.state["possession"]},
    )
    sim.schedule(15.0, shot_attempt)


async def shot_attempt(sim: Sim, _ctx: Action | None) -> None:
    """Decision point: the offensive player chooses what to do."""
    team = sim.state["possession"]
    decision = await sim.llm_hook.decide(
        DecisionContext(
            sim_time=sim.now,
            character_id=f"{team}_player_1",  # toy: always player 1
            decision_type="shot_choice",
            legal_actions=["two_point", "three_point", "pass_instead"],
            state=dict(sim.state),
        )
    )

    if decision.action_type == "pass_instead":
        sim.emit(actor_id=f"{team}_player_1", action_type="pass", payload={})
        sim.schedule(5.0, shot_attempt)
        return

    sim.emit(actor_id=f"{team}_player_1", action_type="shot", payload={"kind": decision.action_type})

    # Toy probabilities: 2pt makes 50%, 3pt makes 33%
    p_make = 0.50 if decision.action_type == "two_point" else 0.33
    if sim.rng.bernoulli(p_make):
        await score(sim, decision)
    else:
        await _flip_possession(sim)


async def score(sim: Sim, ctx: Action | None) -> None:
    """A shot went in. Update score, flip possession."""
    assert ctx is not None
    team = sim.state["possession"]
    points = 3 if ctx.action_type == "three_point" else 2
    sim.state["score"][team] += points
    sim.emit(actor_id=f"{team}_player_1", action_type="score", payload={"points": points, "team": team})
    await _flip_possession(sim)


async def _flip_possession(sim: Sim) -> None:
    """Internal helper — swap possession and schedule the next possession_change."""
    sim.state["possession"] = "away" if sim.state["possession"] == "home" else "home"
    sim.schedule(2.0, possession_change)
