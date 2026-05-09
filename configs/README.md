# Polis Configs — Reference templates

Reference templates for the substrate primitives. These are **fully-seeded examples** that contributors learn from and fork when authoring their own.

## Layout

```
configs/
├── sources.yaml                    Provenance + license tracking for all
│                                   ingested public-domain corpora —
│                                   legal-defensibility audit trail
├── countries/
│   └── england-on-polis/           V0 country template: ~50 files spanning
│                                   constitution, parliament, government,
│                                   geography, laws (civil / criminal /
│                                   commercial / labour / tax / immigration /
│                                   press / sport), regulators, treaties,
│                                   public services, economy
├── industries/
│   ├── football-modern-earth/      4-tier football pyramid with promotion-relegation,
│   │                               6 professions with growth-curve skills,
│   │                               soft-skill weights, overall-rating formula,
│   │                               5-corpora cognition pointers
│   ├── basketball/                 Second industry — proves substrate
│   │                               generality. Backed by an executable
│   │                               round-trip test fixture in cli/tests/
│   └── governance/                 Substrate-level industry hosting
│                                   government, judiciary, civil service,
│                                   cross-cutting regulators
└── (institutions and worlds live in seeds/, not here — see seeds/README.md)
```

## What's in here vs in seeds/

`configs/` holds **templates** — the schema-conforming definition of what a country, industry, or world *is*. Templates are forkable starting points for contributors.

`seeds/` holds **system seeds** — the concrete instances that populate a specific world (Modern Earth 2026's actual cabinet, the actual 12 football clubs in the Hartshire Combination, the actual 20-odd seeded characters, etc.).

A new country template lands in `configs/countries/<name>/`; the people who staff it land in `seeds/<world>/<country>/`.

## Status

V0 closed alpha. England-on-Polis country template, football-modern-earth and basketball industry templates, governance industry template are authored. Additional countries / industries land via [Tier 2 contribution PR per `../CONTRIBUTING.md`](../CONTRIBUTING.md).

## Authoring approach

Most country / industry content is **adapted from public-domain or open-license sources** (per `sources.yaml`). The substrate's own LLM stack drafts; founder reviews + edits for voice.

Voice / framing bar: see [`../CONTRIBUTING.md §4`](../CONTRIBUTING.md#4-voice-and-framing-bar).

## License

CC-BY 4.0 with attribution per [`../LICENSE-CONTENT`](../LICENSE-CONTENT).

Some content adapts from upstream public-domain or open-license sources. Per-source license tracking in [`sources.yaml`](sources.yaml).
