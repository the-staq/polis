"""Polis sim — generic discrete-event simulation kernel.

Substrate primitive. Open-source under Apache 2.0. See `DECISION-SIM-ENGINE.md`.

The kernel runs every sim across the substrate: football match, basketball
game, court case, hostile takeover, election, steel production. Industry
configs declare the rules; the kernel orchestrates time, RNG, and LLM
decision callbacks.

Public surface:
    from polis.sim import Sim, SimConfig, Event, EventLog, LLMHook, StubLLMHook
    from polis.sim import run_sim, SeededRandom

Production runtime (LLM-hook wiring, retrieval injection, ledger settlement)
lives in `polis-internal` and consumes the same primitives.
"""

from polis.sim.config import (
    ActorRoleSpec,
    DriverType,
    EndCondition,
    EndConditionType,
    EventSpec,
    SimConfig,
)
from polis.sim.contract import FinalState, Observation, SimTime, Simulator
from polis.sim.events import Event, EventLog
from polis.sim.kernel import Sim, run_sim
from polis.sim.llm_hook import Action, DecisionContext, LLMHook, RandomLLMHook, StubLLMHook
from polis.sim.rng import SeededRandom

__all__ = [
    # config
    "ActorRoleSpec",
    "DriverType",
    "EndCondition",
    "EndConditionType",
    "EventSpec",
    "SimConfig",
    # contract
    "FinalState",
    "Observation",
    "SimTime",
    "Simulator",
    # events
    "Event",
    "EventLog",
    # kernel
    "Sim",
    "run_sim",
    # llm_hook
    "Action",
    "DecisionContext",
    "LLMHook",
    "RandomLLMHook",
    "StubLLMHook",
    # rng
    "SeededRandom",
]

__version__ = "0.0.1"
