"""Sim kernel — asyncio-native discrete-event loop.

The substrate primitive. ~150 LOC. Per `DECISION-SIM-ENGINE.md`:
- heapq event queue with sequence-counter tie-break (deterministic ordering)
- seeded RNG injected at reset
- async/await native — LLM hooks await inline
- driver-agnostic — config picks event / tick / turn time-stepping
- Gymnasium-shaped outer API (reset / step / run)

This is where every sim across the substrate runs: football match, basketball
game, court case, hostile takeover, election, steel production, music recording.
The kernel never knows what any of these are — it only schedules callbacks and
records what happens.
"""

from __future__ import annotations

import asyncio
import heapq
import importlib
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field

from polis.sim.contract import FinalState, Observation, SimTime
from polis.sim.events import Event, EventLog
from polis.sim.llm_hook import LLMHook
from polis.sim.rng import SeededRandom


@dataclass(order=True)
class _ScheduledEvent:
    """Internal queue entry. heapq orders by (time, sequence)."""

    time: SimTime
    sequence: int
    callback: Callable[["Sim"], Awaitable[None]] = field(compare=False)


class Sim:
    """The kernel. One instance per sim run.

    Lifecycle:
        sim = Sim(config, llm_hook=StubLLMHook(rng=SeededRandom(42)))
        await sim.reset(config, seed=42)
        await sim.run(until=5400)  # 90 minutes
        # sim.event_log contains everything that happened
    """

    def __init__(self, config, llm_hook: LLMHook) -> None:
        self.config = config
        self.llm_hook = llm_hook
        self.now: SimTime = 0.0
        self.state: dict = {}
        self.rng: SeededRandom | None = None
        self.event_log = EventLog()

        self._queue: list[_ScheduledEvent] = []
        self._sequence: int = 0
        self._handlers: dict[str, Callable] = {}
        self._done: bool = False

    async def reset(self, config, seed: int) -> Observation:
        """Initialize from config + seed. Returns starting observation."""
        self.config = config
        self.now = 0.0
        self.state = dict(config.initial_state)
        self.rng = SeededRandom(seed)
        self.event_log = EventLog()
        self._queue = []
        self._sequence = 0
        self._done = False
        self._load_handlers()
        return Observation(sim_time=self.now, state=dict(self.state))

    def _load_handlers(self) -> None:
        """Import each event handler from its dotted path. Done once at reset."""
        self._handlers = {}
        for event_spec in self.config.events:
            module_path, _, func_name = event_spec.handler.rpartition(".")
            if not module_path:
                raise ValueError(f"event handler must be dotted path, got {event_spec.handler!r}")
            module = importlib.import_module(module_path)
            handler = getattr(module, func_name)
            self._handlers[event_spec.id] = handler

    def schedule(self, delay: SimTime, callback: Callable[["Sim"], Awaitable[None]]) -> None:
        """Schedule a callback to run after `delay` sim seconds.

        Sequence counter breaks ties for callbacks scheduled at the same sim_time —
        guarantees deterministic event ordering across runs with the same seed.
        """
        if delay < 0:
            raise ValueError(f"schedule delay must be >= 0, got {delay}")
        self._sequence += 1
        heapq.heappush(
            self._queue,
            _ScheduledEvent(time=self.now + delay, sequence=self._sequence, callback=callback),
        )

    def emit(self, *, actor_id: str | None, action_type: str, payload: dict | None = None) -> Event:
        """Record an Event at the current sim_time. Returns the persisted Event."""
        self._sequence += 1
        event = Event(
            sim_time=self.now,
            actor_id=actor_id,
            action_type=action_type,
            payload=payload or {},
            sequence=self._sequence,
        )
        self.event_log.append(event)
        return event

    def end(self, outcome: dict | None = None) -> None:
        """Signal the sim should stop. The current `run` call will return."""
        self._done = True
        if outcome:
            self.state.update(outcome)

    async def step(self) -> tuple[Observation, list[Event], bool]:
        """Advance one event from the queue. Returns (obs, events_emitted, done)."""
        if self._done or not self._queue:
            return Observation(sim_time=self.now, state=dict(self.state)), [], True

        scheduled = heapq.heappop(self._queue)
        self.now = scheduled.time
        events_before = len(self.event_log.events)
        await scheduled.callback(self)
        new_events = self.event_log.events[events_before:]

        done = self._done or self._check_end_condition()
        return Observation(sim_time=self.now, state=dict(self.state)), new_events, done

    def _check_end_condition(self) -> bool:
        """Driver-agnostic end-condition check."""
        ec = self.config.end_condition
        if ec.type.value == "duration":
            return self.now >= (ec.sim_seconds or float("inf"))
        if ec.type.value == "event_count":
            target = ec.count or 0
            type_count = sum(1 for e in self.event_log if e.action_type == ec.event_type)
            return type_count >= target
        if ec.type.value == "target_state":
            target = ec.target_state or {}
            return all(self.state.get(k) == v for k, v in target.items())
        return False

    async def run(self, until: SimTime | None = None) -> FinalState:
        """Run until end condition, queue empty, or `until` sim seconds reached."""
        while not self._done:
            if until is not None and self.now >= until:
                break
            if not self._queue:
                break
            _, _, done = await self.step()
            if done:
                break
        return FinalState(
            sim_time=self.now,
            outcome=dict(self.state),
            event_log=self.event_log,
            seed=self.rng.seed if self.rng else 0,
        )

    def handler_for(self, event_id: str) -> Callable:
        """Look up the loaded handler for an event id. Used by drivers / configs."""
        return self._handlers[event_id]


async def run_sim(config, *, seed: int, llm_hook: LLMHook, until: SimTime | None = None) -> FinalState:
    """Convenience: create + reset + run a sim in one call."""
    sim = Sim(config=config, llm_hook=llm_hook)
    await sim.reset(config, seed=seed)
    # Driver-specific bootstrap: schedule the first event(s). Configs typically
    # provide a `bootstrap` handler that does this; if not, the run is a no-op.
    if config.events and config.events[0].id == "bootstrap":
        bootstrap = sim.handler_for("bootstrap")
        await bootstrap(sim, None)
    return await sim.run(until=until)
