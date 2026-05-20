# polis/sim — substrate simulation kernel

Generic discrete-event simulation primitive. Open-source under Apache 2.0.
The kernel that runs every sim across the Polis substrate: football matches,
basketball games, court cases, hostile takeovers, elections, steel production,
boxing matches, music recording sessions. Industry configs declare the rules;
this kernel orchestrates time, RNG, and LLM decision callbacks.

See `../../DECISION-SIM-ENGINE.md` for the architectural decision and rationale.

## What's here

```
polis/sim/
├── kernel.py        # asyncio event loop, heapq scheduler, ~150 LOC
├── contract.py      # Simulator Protocol, Observation, FinalState (Gymnasium-shaped)
├── events.py        # Event dataclass + EventLog (append-only)
├── rng.py           # SeededRandom — deterministic + replayable
├── llm_hook.py      # LLMHook Protocol + StubLLMHook + RandomLLMHook
├── config.py        # SimConfig Pydantic model — what configs declare
├── patterns/        # (planned) reusable event/tick/turn drivers
└── tests/           # kernel smoke + determinism + basketball integration
```

## Run the toy basketball sim

```python
import asyncio, yaml
from polis.sim import SimConfig, SeededRandom, StubLLMHook, run_sim

with open("polis/configs/industries/basketball/sim/rules.yaml") as f:
    cfg = SimConfig(**yaml.safe_load(f))

rng = SeededRandom(seed=42)
hook = StubLLMHook(
    rng=rng,
    policies={"shot_choice": lambda ctx, r: r.choice(ctx.legal_actions)},
)

final = asyncio.run(run_sim(cfg, seed=42, llm_hook=hook))
print(f"Final: {final.outcome['score']}, events: {len(final.event_log)}")
```

## Author a new industry sim

Three pieces in `polis/configs/industries/{industry}/sim/`:

1. **`rules.yaml`** — `SimConfig` declaring driver type, end condition, event
   vocabulary, role expectations, initial state.
2. **`handlers.py`** — async Python handlers each event references via dotted
   path. Signature: `async def handler(sim: Sim, ctx: Action | None) -> None`.
   Mutate `sim.state`, `sim.emit()` events, `sim.schedule()` follow-ups, call
   `sim.end()` when the sim should stop.
3. **`README.md`** — purpose, run instructions, calibration data sources.

See `polis/configs/industries/basketball/sim/` for a worked example.

## Substrate-discipline guarantees

- Kernel code contains zero industry-specific terms (verified by V0-PLAN §5.1
  rule 7 lint). All domain vocabulary lives in configs.
- Deterministic under stub LLM hook + fixed seed — required for calibration
  (V0-PLAN §7 gap 1). See `tests/test_kernel.py::test_kernel_is_deterministic_under_same_seed`.
- Event log order is sim-time monotonic + sequence-counter tie-broken — no
  ordering ambiguity across runs.
- LLM hook is async-native — production hooks can await Temporal activities,
  retrieval calls, multi-second LLM responses inline without contortion.
- `Simulator` Protocol matches Gymnasium shape (`reset` / `step` / `run`) so
  RL toolchains can plug in later for free, without depending on Gymnasium.

## Determinism + LLM nondeterminism

The kernel + seeded RNG + `StubLLMHook` is fully deterministic. Production
runs with cloud LLM hooks (Claude / GPT / Ollama) are not — LLM responses vary
even at `temperature=0` due to model serving infrastructure. Calibration suites
use the stub hook; alpha/prod runs accept LLM nondeterminism as a feature.

To replay a real LLM-driven run: record LLM responses in the EventLog payload
during the live run, then replay via a `RecordingLLMHook` that returns the
recorded responses. (Recording hook is V0.5+ work; not shipped yet.)

## Integration with the closed runtime

This kernel ships in the open repo. The closed runtime (`polis-internal/`)
provides:

- Production `LLMHook` implementations (LiteLLM router + Langfuse + retrieval-
  augmented context per V0-PLAN §3.10)
- Workflow orchestration that triggers sims (`MatchWorkflow`, `ConflictWorkflow`)
- Settlement of sim outcomes to the Coin ledger (`DECISION-LEDGER.md`)
- Persistence of EventLog to Postgres with substrate-scoped indexing

The contract between open kernel and closed runtime is the `Simulator` +
`LLMHook` Protocols in this package. The closed runtime imports `polis.sim`
just like any other consumer.

## Pending

- ~~`polis/schemas/sim_config.schema.json` — JSON Schema equivalent of `SimConfig`~~ — **shipped** (round-trip enforced by `tests/test_sim_config_schema.py`; Pydantic source in `config.py` stays manual mirror until codegen pipeline per V0-PLAN §5 ships)
- ~~`polis/schemas/sim_result.schema.json` — JSON Schema for `FinalState.outcome` shape; referenced by `SimConfig.output_schema_ref`~~ — **shipped** (basketball-fixture round-trip enforced by `tests/test_sim_result_schema.py`; Pydantic `SimResult` model + `FinalState.to_sim_result()` helper to follow when orchestration in `polis-internal` wires this in)
- `patterns/event.py`, `patterns/tick.py`, `patterns/turn.py` — reusable drivers
  for common sim shapes
- Calibration harness scaffolding (`polis/sim/calibration/`) — Monte Carlo runner,
  per-industry target-distribution comparison
- TypeScript + Rust SDK additions (`polis/sdk/ts/sim/`, `polis/sdk/rs/sim/`) so
  non-Python consumers can author and run sims

## License

Apache 2.0. See `../LICENSE`.
