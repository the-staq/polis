# Polis

> **A substrate for civilizations.** Open schemas, open SDK, open reference configs. Closed engine that runs them.

Polis is a hosted platform substrate where users build persistent virtual civilizations populated by autonomous AI characters. This repository is the **public surface** — the schemas that contributors author against, the SDK that consumes them, reference configs that show what's possible, and the CLI that validates work locally.

The engine that runs the substrate (`polis-internal`) is closed-source. Contributions to this repository land as **declarative configs + assets, never executable code in the runtime path**.

---

## Status

- **Phase:** v0 closed alpha — foundation work in progress (schemas + reference content + corpora)
- **License:** Apache 2.0 (code, SDK, schemas) · CC-BY 4.0 (content configs)
- **Governance:** founder-only review at v0; reviewer pool at v1; RFC process at v2+. See [`GOVERNANCE.md`](GOVERNANCE.md).
- **Contribution agreement:** [Developer Certificate of Origin](https://developercertificate.org/) for Tier 1 + Tier 2 contributions; explicit license-to-host CLA for Tier 3 (royalty-bearing original creations). See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Repository layout

```
polis/
├── schemas/         JSON Schemas — the substrate's public API
│                    (world / country / industry / institution / character /
│                     contract / conflict / lot / soft_skills / mortality)
├── configs/         Reference instances (templates, slot definitions)
│   ├── countries/      Country templates with full depth (laws / government /
│   │                   regulators / public services)
│   ├── industries/     Industry templates (football, basketball, governance)
│   └── sources.yaml    Provenance + license tracking for ingested corpora
├── seeds/           System seeds — concrete instances of the templates
│   └── modern-earth-2026/
│       ├── world.yaml      The curated V0 world
│       └── england-on-polis/   Government, regulators, football clubs,
│                               characters, contracts, lots
├── sdk/             Codegen'd from schemas: Python, TypeScript, Rust (V1+)
├── cli/             polis-cli — validate, lint, dev tooling
├── contracts/       Smart contract templates (factory-deployed only)
├── docs/            Schema reference, contributor guide, examples
├── SKILLS-DESIGN.md     Doctrine: hard-skill growth curves + 9-attribute soft skills
└── MORTALITY-DESIGN.md  Doctrine: 16 death causes, needs calibration, suicide gating
```

---

## Contribution tiers

Three shapes of contribution, each with its own license + reward model.

### Tier 1 — Spec / code (recognition)
Schemas, SDK, generated bindings, examples, validators, docs, CLI. **Apache 2 / MIT.** Reward: recognition + governance vote at v2+.

### Tier 2 — Reference implementation (paid bounty)
Default industry / world / institution configs that ship with the platform. **CC-BY 4.0** (content) + **MIT** (glue code). Reward: Polis-paid bounty + named credit.

### Tier 3 — Original creation (perpetual royalty)
Original in-app creations on the running substrate — institutions you found, characters you spawn, smart-contract templates you author. Creator-owned with license-to-Polis grant; **runs only on Polis**. Reward: perpetual royalty (cap 0.5%) on in-substrate activity. Note: countries and industries are NOT in this tier — they are open-source-driven (Tier 2).

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for tier mechanics and how to propose work.

---

## Quick start (contributor)

```bash
# Clone
git clone https://github.com/the-staq/polis
cd polis

# Install CLI
pip install -e ./cli

# Validate a config locally
polis-cli validate configs/countries/england-on-polis/

# See schema reference
ls schemas/

# Run round-trip test (basketball CI fixture)
polis-cli test cli/tests/fixtures/basketball-roundtrip/
```

Full contributor guide: [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Why open

Polis's defensibility is **closed engine + open extension surface**. The same shape Roblox / AppExchange / Salesforce / Shopify proved at scale. Open schemas + SDK + reference configs let contributors author against the substrate without ever touching the engine. The engine being closed protects the moat; the schemas being open compound community value into the platform.

---

## Security

See [`SECURITY.md`](SECURITY.md) for vulnerability disclosure. Smart-contract bug bounty program TBD at v1 mainnet.

---

## Code of conduct

[Contributor Covenant 2.1](CODE_OF_CONDUCT.md).

---

## License

- **Code, SDK, schemas, CLI:** Apache 2.0 — see [`LICENSE`](LICENSE)
- **Content configs (worlds / countries / industries / institutions):** CC-BY 4.0 — see [`LICENSE-CONTENT`](LICENSE-CONTENT)
- **Smart contract templates:** Apache 2.0 (factory-deployment-only via the staq)

---

**Polis is operated by the staq. The runtime (`the-staq/polis-internal`) is closed-source. This repository (`the-staq/polis`) is the public substrate API.**
