# Polis Governance

> **Status:** v0.1 — governance evolves V0 → V1 → V2+ as the platform matures.

---

## V0 — closed alpha (months 1-12)

### Decision authority
- **Founder-only review** on all PRs to this repository
- All schema changes, content additions, smart-contract templates require founder approval
- Founder retains absolute veto

### PR review
- DCO sign-off required (CI-enforced)
- Tier 2 + Tier 3 contributions go through voice / framing review per [`CONTRIBUTING.md §4`](CONTRIBUTING.md#4-voice-and-framing-bar)
- Tier 3 creations must pass all six substrate guardrail layers (engine hard floors, constructive bounds, contribution review gates, runtime, cross-country, termination)

### Schema RFCs
- Skipped at v0; founder approves substantive schema changes via issue + PR
- Documented retroactively as RFC-NNNN under `docs/rfcs/` once RFC process activates at v1

### Conflict resolution
- Founder is final arbiter
- Code of Conduct violations: founder-only deplatforming decisions

---

## V1 — mainnet launch (months 18-30+)

### Decision authority
- **Reviewer pool** of 3-5 trusted contributors gets merge rights on Tier 1 contributions (schemas, SDK, docs)
- Founder retains veto + sole authority on Tier 3 (original creations earning royalties)
- T&S deplatforming decisions remain founder-only (SM&CR analog)

### Schema RFCs
- **RFC process activates** for substantive schema changes (modeled on Rust RFCs / Python PEPs / Solana SIMD)
- 14-day comment period; reviewer pool + community input
- RFC accepted → numbered `RFC-NNNN.md` under `docs/rfcs/` → schema PR can land
- Founder retains veto on RFCs that conflict with substrate guardrails

### Reviewer pool selection
- Trusted contributors with sustained Tier 1 + Tier 2 contributions over V0
- Invited by founder; serves at founder discretion at V1
- 3-5 maintainers initial; expandable as community grows

### Conflict resolution
- Disputes between contributors → reviewer pool mediation
- Disputes about Tier 3 creations → founder + reviewer pool joint review
- Code of Conduct violations: reviewer pool can recommend, founder decides

---

## V2+ — mature platform (post-validation)

### Decision authority (split by domain)
- **Schema RFCs:** RFC process + reviewer pool approval; founder retains veto only on guardrail-affecting changes
- **Tier 1 + Tier 2 contributions:** reviewer pool merge rights; founder veto removed except on legal / regulatory matters
- **Tier 3 creations:** founder + reviewer pool joint review (founder retains veto on T&S grounds only)
- **Treasury / parameter decisions:** POLIS-token DAO governance (per PRD §12.3) for non-substrate-correctness matters (treasury allocation, grant programs, parameter tuning)
- **Substrate correctness:** never DAO-governed. Schema integrity, guardrails, T&S enforcement remain operator-controlled.

### Reviewer pool
- Maintainer council of 7-15 trusted contributors
- Term-limited (e.g. 2-year terms); rotating membership
- Selection process documented separately at V2+ activation

### RFC process
- Mature: comment period varies by impact (7 days for clarifications, 30 days for substantive); explicit acceptance criteria; tracked in `docs/rfcs/`

### What stays operator-controlled forever
- Engine source (closed-source forever; this is the substrate's defensibility)
- T&S enforcement (SM&CR-style accountability requires a human / operator)
- Sanctions screening (engine hard floor — non-overridable by any country, industry, or institution)
- Custodial wallet / commerce / fiat ramp / KYC operations (regulatory)
- Polis trademark + brand

---

## Governance principles (across all stages)

1. **Substrate correctness is never DAO-governed.** Schema integrity, guardrails, T&S enforcement are operator-controlled at all times.
2. **Royalty streams are inviolable.** Tier 3 creator royalties (PRD §6.3-6.4) cannot be reduced or removed without explicit creator consent. New royalty mechanics (e.g. royalty-on-secondary-market) require RFC.
3. **Open contribution surface stays open.** Schemas, SDK, reference configs, smart contract templates are public Apache 2 / CC-BY 4.0 forever. PRD §5.2 commits to this.
4. **Founder veto preserves substrate safety.** Even at V2+, founder retains override only on engine-level safety (CSAM, real threats, sanctions compliance). Per V0-PLAN §3.7.
5. **Community decisions are reversible by default.** Anything the DAO or reviewer pool decides should be reversible by subsequent vote. Irreversible changes (license changes, governance overhauls) require supermajority + founder consent.

---

## Amendment process

This document evolves with the platform.

- V0 → V1 transition: this document is rewritten; founder + first reviewer pool ratify
- V1 → V2+ transition: RFC + reviewer pool approval + founder ratification
- Amendments at V2+: RFC process; supermajority of reviewer pool + founder consent

Versioned at the top of this file. Amendments require updating the version + adding an entry to a changelog (TBD).

---

**Last updated:** 2026-05-09 (v0.1, V0 stage)
**Next review:** at V1 mainnet launch
