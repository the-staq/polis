# Polis Seeds — staq-curated launch instance data

> **What this is.** The specific instance data that makes the substrate **operational from minute one**. Government incumbents fill country roles so ConflictWorkflow can adjudicate. Regulator institutions populate industry oversight slots. NPCs fill labor markets so player-characters apply against a populated workforce. Reference institutions (Hartwell FC, the 12 Hartshire clubs) give the world texture. Reference characters carry the first stories. First-period press archive gives the world historical depth.
>
> **What this is not.** Schemas (those are the API in `../schemas/`). Templates (those are *shape* definitions in `../configs/`). User-founded content (that's V1+ engine-private in `polis-internal`). Operational state (running balances, in-flight contracts — substrate-tracked, not authored).
>
> **Per PRD §5.2 + §8.6 + §9.4 + OPEN-SOURCE.md Tier 2:** seeds are reference content (CC-BY 4.0), public-repo, contributor-visible, fork-and-adapt-able. Anyone curating a new world / country / industry can study these as worked examples.

## The four-layer mental model

```
SCHEMAS (API)              ← polis/schemas/*.schema.json (Apache 2)
   ↓ defines
TEMPLATES (shapes)         ← polis/configs/{worlds,countries,industries}/ (CC-BY)
   ↓ instantiated by
SYSTEM SEEDS (launch state) ← THIS DIRECTORY (CC-BY)
   ↓ runs alongside
INSTANCES (V1+ user data)  ← polis-internal (private; user-owned per Tier 3 CLA)
```

Seeds and instances have the same shape (both validate against the same schemas). The distinction is **who curates them and when**:

| | Seeds (here) | Instances (polis-internal at V1+) |
|---|---|---|
| Curator | the staq | User-founders (Tier 3) |
| Visibility | Public, CC-BY | Private; selectively surfaced via UI |
| Lifecycle | Frozen launch state | Living; saga-tracked operational state |
| Licensing | CC-BY 4.0 | Creator-owned with license-to-host grant |
| Royalty | None (bundled with platform) | Perpetual per PRD §6.3-6.4 |

## Layout

Per world, per country, per industry:

```
seeds/<world>/<country>/
├── government/                  (always seeded — substrate enforcement
│   ├── prime-minister.yaml      depends on filled gov roles)
│   ├── cabinet/
│   ├── judiciary/
│   └── civil-service/
├── regulators/                  (per-country; filled regulators per
│                                 country.regulators[] foreign keys)
├── npcs/                        (bootstrap labor pool — engine-spawned
│                                 character_role: npc, lower LLM tier)
├── <industry>/                  (per industry the country hosts)
│   ├── institutions/            (12 football clubs at V0)
│   ├── characters/              (60 footballers + 14 officers + 12 managers)
│   └── press-archive/           (Cattlemarket Echo Vol I issues 1-8)
└── ... (additional industries when V0.5 / V1+ ship)
```

V0 alpha ships seeds for `modern-earth-2026/england-on-polis/` only. V0.5 adds basketball under the same country. V1+ may open user-created countries — those instances live in `polis-internal`, not here.

## Why seeds are CC-BY (not creator-owned)

System seeds are **reference content** in the sense of OPEN-SOURCE.md Tier 2 (paid bounty). The staq pays contributors to author them as bundled platform content. Authors get bounty + named credit. They do NOT get perpetual royalty — that mechanism is reserved for Tier 3 originals (user-founded countries / industries / institutions) where the creator is the substrate principal earning the royalty stream.

Seeds = reference; not Tier 3 royalty-bearing originals.

## How seeds and templates relate

A common confusion is "isn't `england-on-polis/` a template (because it's a country) AND a seed (because it has specific incumbents)?" Resolution:

- **`polis/configs/countries/england-on-polis/`** is the *template* — the constitution, the law definitions, the parliamentary structure-as-data. *What England-on-Polis is structurally.* If a V1+ user wants to fork England-on-Polis to create the Republic of Westonia, this is what they fork.
- **`polis/seeds/modern-earth-2026/england-on-polis/`** is the *seed* — Eleanor Pell-Whitcombe is the current PM, Adaeze Okoye is at Hartwell FC, Hartwell are 4th in the league at gameweek 9. *What England-on-Polis is in V0 launch state.*

Both validate against the same schemas. Different layers of the same substrate.

## Authoring seeds

Per OPEN-SOURCE.md Tier 2 (b): bountied work, founder-edited for voice. Most reference-character + reference-institution content already exists in `design/data.js` (the V2 design's seeded football data). Foundation-work week 5-7 translates that content into seed YAMLs against the schemas — translation, not invention. New work (government incumbents, regulators, NPCs) adapts from public-domain sources per `../configs/sources.yaml`.

## License

CC-BY 4.0 per [`../LICENSE-CONTENT`](../LICENSE-CONTENT). Adapt and remix; attribute "the staq and contributors."
