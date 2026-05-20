# Polis Schemas

Canonical JSON Schema definitions for the substrate primitives.

These schemas are the **public API of Polis**. Pydantic / SQLAlchemy / TypeScript / docs are all codegen'd from here.

## Schemas

| Schema | Version | Description |
|---|---|---|
| `world.schema.json`        | 0.1.2 | Curated world (e.g. Modern Earth 2026) — geography, calendar, physics, mortality calibration, asset pack. v0.1.2 amends `calendar`: `in_world_day_per_real_day` default 1.0 → 12.0 (one canonical clock per world at 12× wall-clock); adds `heartbeat_world_seconds` (default 3600) per [`../../DECISION-TIME-MODEL.md`](../../DECISION-TIME-MODEL.md) |
| `country.schema.json`      | 0.1.2 | Country template — jurisdictions, government, laws, taxation, citizenship, regulators, foreign policy, actuarial life expectancy, plus bound constraints encoding substrate guardrails. v0.1.2 adds `currency.realm` enum (coin V0 / on-chain V1+) per [`../../DECISION-CURRENCY-MODEL.md`](../../DECISION-CURRENCY-MODEL.md) |
| `industry.schema.json`     | 0.1.2 | Industry template — professions with growth-curve-aware skills, institution types, events, economics, competition hierarchy, regulator, season calendar, 5-corpora cognition pointers, soft-skill weights, overall-rating formula |
| `institution.schema.json`  | 0.1.1 | Institution — staff hierarchy with reporting lines, governance, capital, operations, reputation, smart contracts. v0.1.1 renames `initial_treasury_pol`/`current_treasury_pol`/`principal_pol`/`share_capital_pol` to their `_coin` counterparts (V0 primary); pol-suffix fields recast as V0.5+ real-money rail per [`../../DECISION-CURRENCY-MODEL.md`](../../DECISION-CURRENCY-MODEL.md) |
| `character.schema.json`    | 0.1.4 | AI agent — identity, personality, cognition, professions, soft skills (9-attribute), vital status, finances, relationships, **affinities**, principal-agent governance. v0.1.3 = Coin/POL finances per `DECISION-CURRENCY-MODEL.md`. v0.1.4 amends cognition per [`../../DECISION-TIME-MODEL.md`](../../DECISION-TIME-MODEL.md) (renames `decision_frequency` → `decision_frequency_wall`, adds `event_subscriptions[]`) AND adds `affinities[]` per [`../../DECISION-AFFINITY-PRIMITIVE.md`](../../DECISION-AFFINITY-PRIMITIVE.md) (typed/weighted/factor-attributed emotional investments — fans, supporters, anti-rivals) |
| `contract.schema.json`     | 0.1.0 | Tradeable agreement — type, parties, terms, performance modifiers, termination clauses |
| `conflict.schema.json`     | 0.1.0 | Adversarial action — wars, lawsuits, hostile takeovers, foreclosures with deterministic resolution |
| `lot.schema.json`          | 0.1.0 | Smallest land unit — coordinates, zoning, ownership, rental, endowments |
| `soft_skills.schema.json`  | 0.1.0 | Canonical 9-attribute soft-skill taxonomy (composure, charisma, resilience, integrity, decisiveness, empathy, ambition, ego, work_ethic) |
| `mortality.schema.json`    | 0.1.0 | Cause-of-death catalogue (16 entries), death-event record, vital_status, needs_calibration, actuarial_life_expectancy. Suicide is engine-gated |
| `sim_config.schema.json`   | 0.1.0 | Per-industry simulation config consumed by the `polis/sim/` substrate kernel — driver (event/tick/turn), end conditions, actor roles, event vocabulary with optional LLM decision points, output schema ref. Per [`../../DECISION-SIM-ENGINE.md`](../../DECISION-SIM-ENGINE.md) |
| `sim_result.schema.json`   | 0.1.1 | Persisted, replayable record of one sim run — wraps the kernel's FinalState with sim_id, kernel/config version, seed, wall-clock + world-clock timing, terminated_by enum, full event_log, industry-specific outcome payload, llm_hook metadata, optional replay_hash. Closes the loop on `sim_config.schema.json.output_schema_ref`. v0.1.1 adds `world_time_at_start` + `world_time_at_end` per [`../../DECISION-TIME-MODEL.md`](../../DECISION-TIME-MODEL.md) (kernel emits events at world-time pace; wall-clock and world-clock tracked separately) |

## Discipline

- **Wide** — generic across industries; no domain-specific columns. Skills, soft-skills, professions all stored as JSON maps keyed by industry-defined IDs.
- **Deep** — fully expresses real-world dependencies (jurisdictions, laws, hierarchies, regulators, mortality, principal-agent governance, contractual remedies).
- **Bounded** — constraints encode guardrails (max tax 65%, max inflation 20%, mandatory `must_include` law floors, suicide engine-gating).

Schema changes go through RFC at V1+. See [`../GOVERNANCE.md`](../GOVERNANCE.md).

## Validation

```bash
# Validate a config locally
polis-cli validate ../configs/countries/england-on-polis/

# Generate Pydantic / TS / SQLAlchemy bindings from schema
polis-cli codegen --target python --output ../sdk/polis-sdk-py/
```

CLI tooling lands with the foundation sprint. Until then, validation can be run manually via `python3 -m jsonschema` or any Draft 2020-12 validator.

## Doctrine

Two design docs at the repo root expand on the schema:
- [`../SKILLS-DESIGN.md`](../SKILLS-DESIGN.md) — how hard-skill growth curves + soft-skill weights + per-profession `overall_rating_formula` compose into ranking
- [`../MORTALITY-DESIGN.md`](../MORTALITY-DESIGN.md) — needs-calibration → death-event flow, the 4 paths to mortality, the suicide safeguarding policy
