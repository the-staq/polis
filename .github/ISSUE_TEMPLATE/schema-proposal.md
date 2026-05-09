---
name: Schema proposal
about: Propose a change to a substrate schema (V0-PLAN §5 schema-driven discipline)
labels: ['schema', 'discussion']
---

## Schema affected

<!-- e.g. country.schema.json, industry.schema.json -->

## Proposed change

<!-- Describe the field / constraint / structural change. Include before/after if applicable. -->

## Motivation

<!-- Why is this needed? What can't existing schemas express? -->

## Depth check (V0-PLAN §5.0)

<!-- Does this proposal increase schema DEPTH or just shape? Concretely: does it let
substrate primitives express real-world dependencies that were previously implicit? -->

## Generality check (V0-PLAN §5.1)

<!-- Does this proposal stay generic across industries, or is it domain-shaped? -->

## Existing config impact

<!-- Which existing configs (worlds / countries / industries / institutions) need to
be updated to satisfy the new schema? Will the toy-basketball CI fixture still pass? -->

## Bounds / guardrails (country / institution / industry only)

<!-- If this affects a country schema, does it touch any constraint in GUARDRAILS.md?
Does it require a new bound (min/max), enum, or must-include floor? -->

## Migration path

<!-- If this is a breaking change to an existing field, what's the migration story
for already-deployed configs? -->

## Alternatives considered

<!-- What other shapes did you consider? Why this one? -->
