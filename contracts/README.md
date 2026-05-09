# Polis Smart Contract Templates

Audited smart contract templates that contributors can extend for Tier 3 creations (countries, industries, institutions). **Deployed only via the staq's approved factory** (per PRD §5.2).

## Status

TBD. V0 contracts ship on Solana Devnet (or Base Sepolia — chain choice locked at V0-PLAN §10 D1).

## Planned templates

- **POL contract** — wrapped 1:1 against test USDC at V0; mainnet-promotable
- **AMM module** — POL/test-USDC pool at V0; multi-pool at V1+
- **Country-currency factory** — deployed at V0, not invoked (no V0 country mints currency)
- **Conflict resolver contracts** — for ConflictWorkflow on-chain state (V0 live for football conflicts)
- **Saga / outbox contracts** — settlement layer

## Why factory-only deployment?

Per PRD §5.3 defensibility: contributors submit smart contract templates as PRs; the staq reviews + audits + deploys via the approved factory. **No contributor deploys directly to live chains.** This protects:
- Substrate from unaudited contract risk (R9 in V0-PLAN: $20-50K audit budget)
- Users from rug-pull-shaped Tier 3 creations
- the staq's regulatory posture

## Audit gate

Every PR to `contracts/templates/` triggers (at V1+):
1. Static analysis via Slither / Anchor security tools
2. Independent audit by approved firm before deployment
3. Bug bounty in scope (per [`../SECURITY.md`](../SECURITY.md))

## License

Apache 2.0 per [`../LICENSE`](../LICENSE). Factory-deployment-only via the staq — that restriction is part of the substrate moat per PRD §5.3, not the code license.
