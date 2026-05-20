# Toy basketball sim config

Kernel-validation fixture per **V0-PLAN §5.1 rule 3**: proves the `polis/sim/`
substrate kernel is industry-agnostic by running a non-football sim end-to-end.

This is **not** a production basketball simulator. Probabilities are uniform,
the play model is two-line, calibration data is absent. Real basketball is
V0.5+ work.

## What it exercises

- `polis.sim.Sim` kernel boots, resets, runs an event-driven sim
- Configs declare event handlers via dotted Python paths
- Event handlers schedule follow-up events (event-driven driver)
- `StubLLMHook` makes decisions at `decision_point: true` events
- `SeededRandom` produces deterministic outcomes with a fixed seed
- `EventLog` accumulates the full play-by-play
- End condition (`duration: 2880 sim_seconds` = 48 min) stops the sim

## Files

- `rules.yaml` — the SimConfig (events, end condition, roles, initial state)
- `handlers.py` — the Python handlers each event references
- `README.md` — this file

## Run it

From a Python environment with `polis` installed:

```python
import asyncio, yaml
from polis.sim import SimConfig, SeededRandom, StubLLMHook, run_sim

cfg = SimConfig(**yaml.safe_load(open("polis/configs/industries/basketball/sim/rules.yaml")))
rng = SeededRandom(seed=42)
hook = StubLLMHook(rng=rng, policies={"shot_choice": lambda ctx, r: r.choice(ctx.legal_actions)})

final = asyncio.run(run_sim(cfg, seed=42, llm_hook=hook))
print(final.outcome["score"], len(final.event_log.events))
```

Output: a final score (deterministic given seed=42) and the count of events
emitted (tipoffs, possessions, shots, scores).

## Substrate-discipline check

The kernel code in `polis/sim/` contains zero references to "basketball",
"shot", "possession", or any other basketball-specific term. All such logic
lives here in the config + handlers. Same kernel, different config, different
game — exactly what V0-PLAN §5.1 rule 1 requires.
