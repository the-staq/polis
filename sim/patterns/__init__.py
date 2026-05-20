"""Reusable sim driver patterns.

Optional. Industry configs can either author handlers directly against the
`Sim` kernel, or use one of these patterns as a starting point.

- `event` (planned) — event-driven scheduler with probabilistic next-event selection
- `tick` (planned) — fixed-cadence tick driver for production sims
- `turn` (planned) — turn-based driver for legal / electoral sims

Pattern modules will land alongside the first industry sim configs that need
them. For V0, the basketball toy fixture authors handlers directly against
the kernel (no pattern required).
"""
