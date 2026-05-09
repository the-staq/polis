# Basketball — industry template

> **What this is.** The canonical Basketball industry template for Polis. Defines professions, institution types, events, competition hierarchy, calendar, regulator role, licensing regime, economic model, founder royalty cap, and the five-sub-corpora cognition slots (event / commentary / decision / governance / tactical) per V0-PLAN §3.10.
>
> **What this is not.** Specific basketball clubs, leagues, agents, or players. Those are **instances**, created by users via the industry's web-app form flow at V1+. Instances live in `polis-internal` (or are user-private at V1+); only the **template** lives here in the public repo.
>
> **Substrate principle:** *industries are templates (in the open repo); institutions are instances (user-created via the industry config).*

## What's here

```
basketball/
├── README.md                ← this file
├── industry.yaml            ← the industry config (validates against
│                              ../../schemas/industry.schema.json)
└── cognition/               ← corpora pointers + provenance for the
                               5 sub-corpora (event/commentary/decision/
                               governance/tactical) — TBD as ingestion
                               lands per FOUNDATION-PLAN.md
```

## How users instantiate against this template

At V1+, when a user wants to found a basketball club via the web app, the form is **codegen'd from `../../schemas/institution.schema.json`** filtered against this industry's `institution_types[]` (which says `club` is `creation_open: true`, `min_capital_pol: 50000`, etc). The user fills the form, signs the Tier 3 CLA, locks 50K POL, passes cooling-off, and goes live. The resulting institution config is engine-private (in `polis-internal`).

Same for an agency (`agency` type, `creation_open: true`, `min_capital_pol: 5000`). Different gates per type.

What the user **cannot** instantiate from here:
- A new league (`creation_open: false` — only one league/country at V0; world-curator decision at V1+)
- A new federation (`creation_open: false`)

These gates live in `industry.yaml` and the engine enforces.

## Round-trip test

The schema-dogfood-fixture (institutions + characters + contracts + match) for V0-PLAN §5.1 rule 3 (executable second-industry round-trip) lives at:

```
polis/cli/tests/fixtures/basketball-roundtrip/
```

That fixture validates the substrate accommodates basketball without schema changes. It is **test data**, not substrate content. CI runs `polis-cli validate` over it; if a schema PR breaks the fixture, the schema PR is wrong.

## License

CC-BY 4.0 per [`../../../LICENSE-CONTENT`](../../../LICENSE-CONTENT). Adapt and remix; attribute "the staq and contributors."
