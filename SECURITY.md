# Security policy

> Polis takes security seriously. This document covers responsible disclosure, scope, and the (TBD V1+) bug bounty program for smart-contract templates.

## Reporting a vulnerability

**Do not open public issues for security vulnerabilities.**

Instead, email: `security@the-staq.com` (TBD — placeholder until org is provisioned)

Include:
- A description of the vulnerability
- Steps to reproduce
- Affected components (schemas, SDK, CLI, smart-contract templates, or — if you've identified an issue with the engine — the engine)
- Your name and contact preference for credit / response
- An optional PGP-encrypted version (key TBD)

**Response time:** acknowledgement within 72 hours; initial triage within 7 days; remediation timeline communicated within 14 days.

---

## Scope

In scope:
- Schema definitions in `polis/schemas/` (validator-bypass, constraint-evasion bugs)
- SDK packages in `polis/sdk/` (validation correctness, deserialization safety)
- CLI in `polis/cli/` (privilege escalation, arbitrary-code-execution via config files)
- Smart contract templates in `polis/contracts/` (re-entrancy, integer overflow, access control, economic exploits)
- Reference configs in `polis/configs/` (substrate-rule violations encoded in content)

Out of scope (this repository):
- Engine vulnerabilities — `polis-internal` security disclosure is handled separately; report via the same email
- Third-party dependencies (report upstream and CC us)
- Hosted infrastructure — the staq handles via standard incident channels

---

## Smart-contract bug bounty

**Active V1+ at mainnet promotion.** Until then:
- V0 closed alpha contracts deploy on Devnet only; no real money flows
- Smart-contract templates ship with audited libraries (OpenZeppelin / Anchor templates)
- Pre-mainnet audit budget: $20-50K per V0-PLAN R9
- Critical bugs reported pre-mainnet still receive recognition + reward at our discretion

**V1+ bounty (when active):**
- Critical (loss of funds, unauthorized minting): $25K-$100K depending on severity and scope
- High (DoS, governance bypass, treasury drain): $5K-$25K
- Medium (information disclosure, minor invariant break): $500-$5K
- Low (best-practice issue, gas optimization): $100-$500

Specific terms TBD before V1 mainnet launch.

---

## Disclosure policy

We follow **coordinated disclosure**:

1. You report privately
2. We acknowledge + triage
3. We work on a fix
4. Once fixed (or 90 days from acknowledgement, whichever is earlier), we publish:
   - The vulnerability details
   - The fix
   - Credit to the reporter (unless they opt out)

Public disclosure before remediation is strongly discouraged but not prohibited; we ask for at least 30 days. If we don't respond within 7 days of your initial report, public disclosure is at your discretion.

---

## Hall of fame

Contributors who responsibly disclose vulnerabilities will be listed here (with their permission). TBD as Polis ships.

---

## What is NOT a vulnerability

- Schema-design preferences ("I think `country.taxation` should have an additional field") — open as a schema RFC instead
- Voice / framing preferences in reference content — open as a Tier 1 issue
- Disagreements with substrate guardrails (the engine-level hard floors: CSAM prohibition, real-world threats, sanctions compliance) — open as a discussion

For these, use GitHub Issues + Discussions normally.

---

**the staq · 2026**
