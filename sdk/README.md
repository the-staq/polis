# Polis SDK

Codegen'd from `polis/schemas/` per V0-PLAN A3.

## Targets

| Package | Status | Description |
|---|---|---|
| `polis-sdk-py` | TBD | Python — Pydantic v2 models + SQLAlchemy mirrors + retrieval client |
| `polis-sdk-ts` | TBD | TypeScript — type definitions + JSON Schema validators (ajv) |
| `polis-sdk-rs` | V1+ | Rust — for performance-sensitive contributors |

## Codegen pipeline

The schema files in `polis/schemas/*.schema.json` are canonical. CI generates language bindings via:

- Python: `datamodel-code-generator` → Pydantic v2 models; SQLAlchemy mirrors hand-written and parity-tested
- TypeScript: `json-schema-to-typescript` → type definitions
- Rust (V1+): `schemafy` or `quicktype`

```bash
# Run codegen locally (TBD until foundation work)
polis-cli codegen --target python --output sdk/polis-sdk-py/
polis-cli codegen --target typescript --output sdk/polis-sdk-ts/
```

## Usage (TBD when SDK ships)

```python
from polis_sdk import Country, Industry, Institution, Character

# Validate a config
country = Country.parse_file("configs/countries/england-on-polis/")
country.validate()

# Inspect schema bounds
print(Country.schema_bounds("taxation.income_tax_rate"))  # {"min": 0.0, "max": 0.65}
```

## License

Apache 2.0 per [`../LICENSE`](../LICENSE).
