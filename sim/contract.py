"""Simulator Protocol — Gymnasium-shaped outer API.

We adopt the shape of `gymnasium.Env` (reset / step / observation / info) without
depending on the package. RL toolchains can plug in later for free; the kernel
stays independent.

Implementations: `polis.sim.kernel.Sim` is the reference. Other implementations
can satisfy the same Protocol (e.g., a recorded-replay simulator that re-emits
an EventLog without running the kernel).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .events import EventLog


SimTime = float
"""Seconds since sim start. Each driver maps its native time unit to this."""


@dataclass(slots=True)
class Observation:
    """Current state of the sim, observable by an LLM hook or external watcher.

    Industry-agnostic shape. `state` carries the industry-specific detail.
    """

    sim_time: SimTime
    state: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FinalState:
    """End-of-sim summary returned by `run()`."""

    sim_time: SimTime
    outcome: dict[str, Any] = field(default_factory=dict)
    event_log: EventLog = field(default_factory=EventLog)
    seed: int = 0
    """The RNG seed used — required for replay."""


class Simulator(Protocol):
    """The contract every sim implementation satisfies.

    `reset` initializes from a config + seed and returns the starting observation.
    `step` advances the sim by one event (driver-specific definition of "one event")
    and returns (observation, events emitted this step, done).
    `run` is the convenience method: reset implied, advance until `until` or end
    condition, return FinalState.
    """

    async def reset(self, config: Any, seed: int) -> Observation: ...

    async def step(self) -> tuple[Observation, list, bool]:
        """Returns (observation, events_emitted_this_step, done)."""
        ...

    async def run(self, until: SimTime | None = None) -> FinalState: ...
