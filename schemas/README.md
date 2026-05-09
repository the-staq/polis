# Polis Schemas

Canonical JSON Schema definitions for the substrate primitives.

These schemas are the **public API of Polis**. Pydantic / SQLAlchemy / TypeScript / docs are all codegen'd from here.

## Schemas

| Schema | Version | Description |
|---|---|---|
| `world.schema.json`        | 0.1.1 | Curated world (e.g. Modern Earth 2026) — geography, calendar, physics, mortality calibration, asset pack |
| `country.schema.json`      | 0.1.1 | Country template — jurisdictions, government, laws, taxation, citizenship, regulators, foreign policy, actuarial life expectancy, plus bound constraints encoding substrate guardrails |
| `industry.schema.json`     | 0.1.2 | Industry template — professions with growth-curve-aware skills, institution types, events, economics, competition hierarchy, regulator, season calendar, 5-corpora cognition pointers, soft-skill weights, overall-rating formula |
| `institution.schema.json`  | 0.1.0 | Institution — staff hierarchy with reporting lines, governance, capital, operations, reputation, smart contracts |
| `character.schema.json`    | 0.1.2 | AI agent — identity, personality, cognition, professions, soft skills (9-attribute), vital status (life expectancy + mortality), finances, relationships, principal-agent governance |
| `contract.schema.json`     | 0.1.0 | Tradeable agreement — type, parties, terms, performance modifiers, termination clauses |
| `conflict.schema.json`     | 0.1.0 | Adversarial action — wars, lawsuits, hostile takeovers, foreclosures with deterministic resolution |
| `lot.schema.json`          | 0.1.0 | Smallest land unit — coordinates, zoning, ownership, rental, endowments |
| `soft_skills.schema.json`  | 0.1.0 | Canonical 9-attribute soft-skill taxonomy (composure, charisma, resilience, integrity, decisiveness, empathy, ambition, ego, work_ethic) |
| `mortality.schema.json`    | 0.1.0 | Cause-of-death catalogue (16 entries), death-event record, vital_status, needs_calibration, actuarial_life_expectancy. Suicide is engine-gated |

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
