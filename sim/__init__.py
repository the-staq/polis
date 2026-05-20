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

from .config import (
    ActorRoleSpec,
    DriverType,
    EndCondition,
    EndConditionType,
    EventSpec,
    SimConfig,
    load_sim_from_yaml,
)
from .contract import FinalState, Observation, SimTime, Simulator
from .events import Event, EventLog
from .kernel import Sim, run_sim
from .llm_hook import Action, DecisionContext, Example, LLMHook, RandomLLMHook, StubLLMHook
from .rng import SeededRandom

__all__ = [
    # config
    "ActorRoleSpec",
    "DriverType",
    "EndCondition",
    "EndConditionType",
    "EventSpec",
    "SimConfig",
    "load_sim_from_yaml",
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
    "Example",
    "LLMHook",
    "RandomLLMHook",
    "StubLLMHook",
    # rng
    "SeededRandom",
]

__version__ = "0.0.1"
