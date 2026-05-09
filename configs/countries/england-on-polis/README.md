# England-on-Polis — country template

> **What this is.** The canonical V0 reference country template, authored by the staq as Tier 2 open-source contribution per `OPEN-SOURCE.md`. Defines constitutional structure (parliamentary supremacy, common law), government branches as data, jurisdictional hierarchy (1 country → 11 counties → towns → districts → lots), filed laws (civil / criminal / commercial / labour / tax / immigration / press / sport), regulator slots, foreign policy posture, public services, economic baseline.
>
> **What this is not.** Specific incumbents (Eleanor Pell-Whitcombe is PM; the cabinet is Treasury / Justice / Foreign / Sport / Labour / Home / Health) — those are *seeds* in `polis/seeds/modern-earth-2026/england-on-polis/`. The template defines the *slot*; the seed fills it.
>
> **At V1+:** users can fork this template to create their own countries (the Republic of Westonia, etc.) via PR per `OPEN-SOURCE.md` Tier 2 (a). This is the canonical reference.

## Layout

```
england-on-polis/
├── README.md                            ← this file
├── country.yaml                         ← top-level country.schema.json instance
├── constitution.md                      ← Westminster-template adaptation; parliamentary
│                                          supremacy, common law, declared rights
├── government/
│   ├── parliament.yaml                  ← chambers, parties, current seat distribution
│   ├── cabinet-positions/               ← 7 cabinet position SLOTS (filled by seeds)
│   │   ├── prime-minister.yaml
│   │   ├── treasury-minister.yaml
│   │   ├── justice-minister.yaml
│   │   ├── foreign-secretary.yaml
│   │   ├── sport-minister.yaml
│   │   ├── labour-minister.yaml
│   │   ├── home-secretary.yaml
│   │   └── health-secretary.yaml
│   └── civil-service/
│       └── permanent-secretaries.yaml   ← positions, not incumbents
├── geography/
│   ├── boundaries.geojson               ← OSM-derived (TBD)
│   ├── counties/
│   │   ├── hartshire.yaml               ← V0 fully-seeded county
│   │   ├── foxbridge.yaml               ← capital region (sketched)
│   │   └── ... (9 more, named-only)
│   └── towns/
│       └── ... (towns within Hartshire — seeded as needed)
├── laws/
│   ├── civil/
│   │   ├── contract-act.md              ← contract-law foundation
│   │   ├── property-act.md
│   │   └── tort-act.md                  ← defamation lives here
│   ├── criminal/
│   │   ├── code.md
│   │   └── procedure.md
│   ├── commercial/
│   │   ├── corporations-act.md
│   │   ├── bankruptcy-act.md
│   │   └── securities-regulation.md
│   ├── labour/
│   │   ├── employment-act.md            ← used by ConflictWorkflow on contract disputes
│   │   ├── union-act.md
│   │   └── pensions-act.md
│   ├── tax/
│   │   ├── income-tax-brackets.yaml     ← machine-readable rates
│   │   ├── corporate-tax.yaml
│   │   ├── capital-gains.yaml
│   │   ├── property-tax.yaml
│   │   └── transfer-tax.yaml            ← matters for football transfer fees
│   ├── immigration/
│   │   ├── visa-categories.yaml
│   │   └── sanctions-and-bars.yaml
│   ├── press/
│   │   └── defamation-and-libel.md      ← Foxbridge Defamation Act; press complaints standard
│   └── sport/
│       └── football-act.md              ← gambling, broadcasting, club licensing
├── regulators/
│   └── index.yaml                       ← which institutions hold which regulator roles
├── public-services/
│   ├── health-system.yaml
│   ├── education.yaml
│   ├── police.yaml
│   └── transport.yaml
├── treaties.yaml                        ← V0: empty (only one country in world)
└── economy/
    ├── currency-policy.yaml
    └── budget.yaml
```

## Authoring approach

LLM-drafts-founder-edits. Public-domain sources adapted with name-substitution per `polis/configs/sources.yaml` provenance rules:

- Constitution → adapted from Constituteproject.org Westminster template (CC-BY 4.0)
- Civil / criminal / commercial / labour / tax law → adapted from `legislation.gov.uk` (Open Government Licence v3.0); names substrate-fictionalised
- Defamation Act → UK Defamation Act 2013 with substrate-fictional name "Foxbridge Defamation Act"
- Football Act → adapted from FA Rules + EFL handbook (publicly available)

Founder editorial review on every file.

## License

CC-BY 4.0 per `../../../LICENSE-CONTENT`. Adapt and remix; attribute "the staq and contributors."

## Status

V0.1 — scaffold landed; key files (country.yaml, constitution.md, hartshire county, defamation act, employment act, income tax brackets, currency policy) authored. ~30 files remain for V0 completeness.
