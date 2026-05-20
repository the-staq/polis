"""LLM callback hook — how character decisions happen inside a sim.

The kernel calls `await hook.decide(...)` whenever a sim config event is flagged
as `decision_point: true`. The hook decides what the character does and returns
an Action.

Two reference implementations ship here:
- `StubLLMHook` — deterministic policy from config rules. Use for tests + calibration.
- `RandomLLMHook` — picks uniformly from legal actions. Use for chaos testing.

Production hooks (Ollama-routed, Claude/GPT via LiteLLM, Temporal-wrapped) live in
the closed runtime (`polis-internal/app/cognition/`) and inject 5-layer retrieval
context per V0-PLAN §3.10.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from .rng import SeededRandom


@dataclass(frozen=True, slots=True)
class Action:
    """What a character decided to do at a decision point.

    Industry-specific. Football: "shoot" / "pass" / "dribble". Court: "object" /
    "concede" / "rest". The kernel passes this back to the sim config's event
    handler, which applies it.
    """

    action_type: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class DecisionContext:
    """What the hook sees when deciding.

    Industry-agnostic shape. The orchestration layer (closed) extends this by
    injecting retrieval-augmented context, character memory, etc., before
    calling `decide`. Kernel-side hooks see this minimal shape only.
    """

    sim_time: float
    character_id: str
    decision_type: str
    legal_actions: Sequence[str]
    state: dict[str, Any]


@runtime_checkable
class LLMHook(Protocol):
    """The contract every decision-source must satisfy.

    Async by design — production hooks await Temporal activities, LiteLLM calls,
    retrieval lookups. Stub hooks return synchronously but match the signature
    so the kernel never branches on hook type.
    """

    async def decide(self, ctx: DecisionContext) -> Action: ...


class StubLLMHook:
    """Deterministic policy hook. Picks the first legal action by default.

    Override per-decision behavior via the `policies` dict, keyed by
    `decision_type`. Each policy is a callable `(ctx) -> action_type`.

    Use this for calibration runs (10K Monte Carlo) and tests. Behavior is
    reproducible given the same RNG seed.
    """

    def __init__(
        self,
        rng: SeededRandom,
        policies: dict[str, Any] | None = None,
    ) -> None:
        self._rng = rng
        self._policies: dict[str, Any] = policies or {}

    async def decide(self, ctx: DecisionContext) -> Action:
        if ctx.decision_type in self._policies:
            chosen = self._policies[ctx.decision_type](ctx, self._rng)
        else:
            chosen = ctx.legal_actions[0] if ctx.legal_actions else "noop"
        return Action(action_type=chosen)


class RandomLLMHook:
    """Picks uniformly from legal actions. Useful for chaos-testing sim configs."""

    def __init__(self, rng: SeededRandom) -> None:
        self._rng = rng

    async def decide(self, ctx: DecisionContext) -> Action:
        if not ctx.legal_actions:
            return Action(action_type="noop")
        return Action(action_type=self._rng.choice(ctx.legal_actions))
