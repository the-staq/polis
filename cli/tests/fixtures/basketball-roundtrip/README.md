# Basketball round-trip fixture — schema-dogfood test data

> **Purpose.** Per V0-PLAN §5.1 rule 3: schemas validate ahead of content via an *executable second-industry round-trip*. This fixture is the test data the polis-cli validator runs against to prove the 8 substrate schemas accommodate a non-football industry without modification.
>
> **This is test data, not substrate content.** The actual basketball industry **template** lives at `polis/configs/industries/basketball/`. The instance data here (institutions, characters, contracts, match) demonstrates instantiation against the template — same shape users will produce at V1+ via the web-app founding flow, but staged here as deterministic test fixtures.

## Layout

```
basketball-roundtrip/
├── README.md                       ← this file
├── institutions/
│   ├── league.yaml                 ← Hartshire Basketball Combination
│   ├── foxbridge-titans.yaml       ← team 1 (staq-curated test data,
│   │                                  founder_principal_id: principal_the-staq)
│   ├── ravensby-fishers.yaml       ← team 2 (staq-curated)
│   └── lambeth-sports-agency.yaml  ← USER-FOUNDED via Tier 3 flow
│                                     (founder_principal_id: principal_user_renata_marquez)
│                                     — demonstrates user-founder substrate distinction
├── characters/
│   └── c_b001.yaml ... c_b010.yaml ← 5 Foxbridge Titans + 5 Ravensby Fishers starters
├── contracts/
│   ├── contract_b001.yaml          ← player employment (Hollencourt → Titans)
│   ├── contract_b002.yaml          ← player employment + agent (Ostmark → Fishers,
│   │                                  represented by lambeth-sports-agency)
│   └── contract_b003.yaml          ← inter-team transfer (sale type with
│                                      sell_on_clause_percent)
└── match-stub/                     ← deterministic match simulator stub
                                       (rng_seed → replayable outcome)
```

## What this fixture proves

| Substrate claim | What this validates |
|---|---|
| Schema **generality** (V0-PLAN §5.1 rule 1) | Basketball uses different professions / skills / competition formats than football, against the same `industry.schema.json` and `institution.schema.json`. No football-shaped fields leaked into the schema. |
| Schema **depth** (V0-PLAN §5.0) | Staff hierarchy with `reports_to_role_id` accommodates basketball's coaching tree as cleanly as football's. Contract `terms.sale.sell_on_clause_percent` shapes basketball transfer the same way it shapes football transfer. |
| **Country hosts multiple industries** | Same `england-on-polis` hosts football AND basketball cleanly; characters can hold professions across both at V1+ multi-profession activation. |
| **Same town, multiple industries** | Ravensby has Ravensby Athletic (football) AND Ravensby Fishers (basketball). Lot / town / district are substrate primitives, industry-agnostic. |
| **5-corpora cognition slot** (V0-PLAN §3.10) | Basketball declares its own event / commentary / decision / governance / tactical corpora pointers; engine retrieval composes them per V0-PLAN §3.10 5-layer pattern. |
| **User-founded vs staq-curated** | `lambeth-sports-agency.yaml` carries a user `founder_principal_id` and a `founder_royalty: 0.005`; the others carry `principal_the-staq` and `founder_royalty: 0.0`. The substrate enforces NO asymmetry between them beyond the founder-requirement gates. Tier 3 economics path validated. |
| **Determinism** | The match stub uses an `rng_seed`; given identical inputs, the simulator produces identical outputs. Substrate guarantee for replay + audit. |

## Running the round-trip test

```bash
# Validate every YAML in this fixture against the public schemas
polis-cli validate polis/cli/tests/fixtures/basketball-roundtrip/

# Run the deterministic match simulator
python polis/cli/tests/fixtures/basketball-roundtrip/match-stub/simulator.py

# CI gate: this fixture must validate AND the simulator must produce stable
# output before any schema PR can land.
```

## Where this differs from V1+ user-creation

Same shape, different lifecycle:

| Aspect | This fixture | V1+ user-creation |
|---|---|---|
| Authoring | Hand-written YAML for tests | Web-app form codegen'd from schemas |
| Storage | Public CLI test fixtures | Engine-private (polis-internal) per institution config |
| Founder verification | None (test data) | KYC tier check, capital lock, cooling-off |
| Smart contract | None | Factory-deployed via Polis approved factory |
| Royalty payments | Inert | Real POL flows per `founder_royalty` |
| Public visibility | This file is in the public repo (it's a test) | Institution data is engine-private; only aggregate / consented fields surface publicly |

## License

The schemas this fixture validates against are Apache 2 (in `polis/schemas/`). The fixture YAMLs themselves are CC-BY 4.0 — substrate-fictional content, attribution to "the staq and contributors."
