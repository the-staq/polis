"""Event + EventLog — what a sim produces.

Substrate primitive. Industry-agnostic. The kernel emits Events; the orchestration
layer (closed) consumes them to drive narrative surfaces, settle the ledger, and
feed press recap. The same Event schema serves football, basketball, court cases,
production sims, elections — every industry per `DECISION-SIM-ENGINE.md`.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class Event:
    """A single thing that happened in a sim, at a moment in sim time.

    Fields are deliberately minimal. Industry-specific detail lives in `payload`,
    keyed by the industry's sim config schema. The kernel never reads `payload`.
    """

    sim_time: float
    """Seconds since sim start. Driver-defined (1 tick = 1 second, or per-shift, or per-turn)."""

    actor_id: str | None
    """Which actor caused this event. None for environmental events (kickoff, weather)."""

    action_type: str
    """Industry-defined verb: "shot", "pass", "objection", "produce", "vote_cast"."""

    payload: dict[str, Any] = field(default_factory=dict)
    """Industry-specific detail. The kernel does not introspect this."""

    sequence: int = 0
    """Tie-break for same-sim_time events. Set by the kernel on emit."""


@dataclass(slots=True)
class EventLog:
    """Append-only log. Source of truth for what a sim run did.

    Determinism guarantee: with identical SimConfig + seed + stub LLM hook,
    `EventLog.events` is bit-identical across runs.
    """

    events: list[Event] = field(default_factory=list)

    def append(self, event: Event) -> None:
        self.events.append(event)

    def __iter__(self) -> Iterator[Event]:
        return iter(self.events)

    def __len__(self) -> int:
        return len(self.events)

    def filter(self, *, action_type: str | None = None, actor_id: str | None = None) -> list[Event]:
        return [
            e
            for e in self.events
            if (action_type is None or e.action_type == action_type)
            and (actor_id is None or e.actor_id == actor_id)
        ]

    def last(self, action_type: str | None = None) -> Event | None:
        for e in reversed(self.events):
            if action_type is None or e.action_type == action_type:
                return e
        return None
