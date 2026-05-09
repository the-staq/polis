# polis-cli

Local validation, lint, and dev tooling for substrate configs.

## Status

TBD until foundation work lands.

## Planned commands

```bash
# Validate a config against its schema
polis-cli validate configs/countries/england-on-polis/

# Lint substrate-discipline rules (V0-PLAN §5.1) locally before commit
polis-cli lint .

# Run round-trip test against toy basketball CI fixture
polis-cli test configs/industries/basketball-ci-fixture/

# Generate language bindings from schemas
polis-cli codegen --target python --output sdk/polis-sdk-py/

# Inspect schema bounds + must-include floors
polis-cli inspect schemas/country.schema.json --field taxation.income_tax_rate

# Verify provenance for a corpus chunk
polis-cli source-trace --chunk-id <id>

# Dev server (runs schema validation as you edit configs)
polis-cli watch configs/countries/england-on-polis/
```

## Local-first principle

`polis-cli` is the contributor's primary local tool. No network calls except:
- Optional: cloud LLM for content drafting (opt-in)
- Optional: corpus fetching from `sources.yaml` URLs (opt-in, cached locally)

Pre-commit hooks per V0-PLAN T1: `polis-cli lint` runs as a `pre-commit` hook before any commit lands.

## License

Apache 2.0 per [`../LICENSE`](../LICENSE).
