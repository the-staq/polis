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
import importlib.util
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from pathlib import Path

from .contract import FinalState, Observation, SimTime
from .events import Event, EventLog
from .llm_hook import LLMHook
from .rng import SeededRandom


@dataclass(order=True)
class _ScheduledEvent:
    """Internal queue entry. heapq orders by (time, sequence)."""

    time: SimTime
    sequence: int
    callback: Callable[["Sim", object | None], Awaitable[None]] = field(compare=False)


class Sim:
    """The kernel. One instance per sim run.

    Lifecycle:
        sim = Sim(config, llm_hook=StubLLMHook(rng=SeededRandom(42)))
        await sim.reset(config, seed=42)
        await sim.run(until=5400)  # 90 minutes
        # sim.event_log contains everything that happened
    """

    def __init__(
        self,
        config,
        llm_hook: LLMHook,
        config_dir: Path | str | None = None,
    ) -> None:
        self.config = config
        self.llm_hook = llm_hook
        self.config_dir: Path | None = Path(config_dir) if config_dir else None
        """Source directory of the parsed sim_config YAML. Used to resolve
        file-path handler refs (e.g., `./handlers.py::bootstrap`). Populated by
        `load_sim_from_yaml()`; remains `None` for dotted-module-only configs
        (e.g., basketball)."""
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
        """Resolve each event handler ref into a callable. Done once at reset.

        Two ref formats supported:
          - `pkg.module.func` (dotted-module, legacy) — `importlib.import_module`
          - `./relative_path.py::func` (file-path) — resolved against `config_dir`

        File-path form unblocks hyphenated industry directories (e.g.,
        `football-modern-earth/`) that can't be Python package names.
        """
        self._handlers = {}
        for event_spec in self.config.events:
            self._handlers[event_spec.id] = self._resolve_handler(event_spec.handler)

    def _resolve_handler(self, ref: str) -> Callable:
        if "::" in ref:
            return self._resolve_file_handler(ref)
        module_path, _, func_name = ref.rpartition(".")
        if not module_path:
            raise ValueError(
                f"handler ref must be dotted path (`pkg.module.func`) or "
                f"file form (`./file.py::func`), got {ref!r}"
            )
        module = importlib.import_module(module_path)
        return getattr(module, func_name)

    def _resolve_file_handler(self, ref: str) -> Callable:
        path_part, _, func_name = ref.partition("::")
        if not func_name:
            raise ValueError(f"file-form handler ref missing function: {ref!r}")
        if self.config_dir is None:
            raise ValueError(
                f"file-path handler ref {ref!r} requires Sim(config_dir=...). "
                f"Pass config_dir or use `load_sim_from_yaml()` which sets it."
            )
        file_path = (self.config_dir / path_part).resolve()
        if not file_path.exists():
            raise FileNotFoundError(
                f"handler module not found: {file_path} (from ref {ref!r}, "
                f"config_dir={self.config_dir})"
            )
        module_name = f"_polis_sim_handler_{file_path.stem}_{id(self):x}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot build module spec for handler file: {file_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, func_name)

    def schedule(
        self,
        delay: SimTime,
        callback: Callable[["Sim", object | None], Awaitable[None]],
    ) -> None:
        """Schedule a callback to run after `delay` sim seconds.

        Sequence counter breaks ties for callbacks scheduled at the same sim_time —
        guarantees deterministic event ordering across runs with the same seed.

        Callback signature: `async def handler(sim, ctx) -> None`. The kernel
        passes `ctx=None` for scheduled callbacks; decision-point dispatch
        happens inside handlers (via `sim.llm_hook.decide(...)`).
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
        await scheduled.callback(self, None)
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


async def run_sim(
    config,
    *,
    seed: int,
    llm_hook: LLMHook,
    until: SimTime | None = None,
    config_dir: Path | str | None = None,
) -> FinalState:
    """Convenience: create + reset + run a sim in one call.

    Pass `config_dir` when any handler ref uses file-path form
    (`./handlers.py::func`). For dotted-module-only configs, omit.
    """
    sim = Sim(config=config, llm_hook=llm_hook, config_dir=config_dir)
    await sim.reset(config, seed=seed)
    # Driver-specific bootstrap: schedule the first event(s). Configs typically
    # provide a `bootstrap` handler that does this; if not, the run is a no-op.
    if config.events and config.events[0].id == "bootstrap":
        bootstrap = sim.handler_for("bootstrap")
        await bootstrap(sim, None)
    return await sim.run(until=until)
