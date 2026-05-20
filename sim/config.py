"""SimConfig — declarative shape every industry's sim config must declare.

Pydantic v2. Loaded from per-industry YAML in `polis/configs/industries/{industry}/sim/`.
Validated at sim startup; never trust an unvalidated config.

Authoring: contributors write YAML against this shape. The kernel reads the
parsed model. Industry-specific event probabilities live in callable handler
modules pointed to by `events[].handler` — see `polis/configs/industries/basketball/sim/`
for a worked example.

NOTE: A JSON Schema equivalent (`polis/schemas/sim_config.schema.json`) should
land alongside the other 8 substrate schemas per V0-PLAN §5. Pending in the
substrate-schemas pass.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class DriverType(str, Enum):
    """Which time-stepping pattern the sim uses."""

    EVENT = "event"
    """Event-driven — schedule next event from current state. Match-shaped (football)."""

    TICK = "tick"
    """Fixed-cadence — every N seconds, process all active actors. Production-shaped (steel)."""

    TURN = "turn"
    """Turn-based — one actor acts per turn, round-robin. Legal-shaped (court case)."""


class EndConditionType(str, Enum):
    DURATION = "duration"
    """End at sim_time >= sim_seconds."""

    TARGET_STATE = "target_state"
    """End when state matches a predicate (e.g., one side wins)."""

    EVENT_COUNT = "event_count"
    """End after N events of a specific type (e.g., 12 rounds of boxing)."""


class EndCondition(BaseModel):
    type: EndConditionType
    sim_seconds: float | None = None
    target_state: dict | None = None
    event_type: str | None = None
    count: int | None = None


class EventSpec(BaseModel):
    """One kind of thing that can happen during the sim."""

    id: str
    """Industry-defined verb. e.g., "pass", "shot", "objection"."""

    handler: str
    """Dotted Python path to the handler function.
    Signature: `async def handler(sim, ctx) -> list[Event]`.
    Loaded via importlib at sim startup."""

    decision_point: bool = False
    """If true, kernel calls LLMHook.decide() before invoking the handler."""

    decision_type: str | None = None
    """Required if decision_point=true. Passed to the LLM hook."""

    legal_actions: list[str] = Field(default_factory=list)
    """Industry-defined action vocabulary the LLM hook can return."""


class ActorRoleSpec(BaseModel):
    """A role one or more actors fill in the sim (goalkeeper, judge, factory_foreman)."""

    role: str
    schema_ref: str = "polis/schemas/character.schema.json"
    """Which schema this role validates against."""

    min_count: int = 1
    max_count: int | None = None


class SimConfig(BaseModel):
    """Top-level sim config. One per industry-sim per world."""

    industry_id: str
    """Matches the industry config id (e.g., "football-modern-earth")."""

    driver: DriverType

    end_condition: EndCondition

    roles: list[ActorRoleSpec] = Field(default_factory=list)
    """What actor roles this sim expects."""

    initial_state: dict = Field(default_factory=dict)
    """Starting state. Industry-specific. Kernel does not introspect."""

    events: list[EventSpec]
    """Event vocabulary for this sim."""

    output_schema_ref: str = "polis/schemas/sim_result.schema.json"
    """Where the FinalState.outcome conforms to."""

    metadata: dict = Field(default_factory=dict)
    """Free-form: version, author, calibration target ref, etc."""
