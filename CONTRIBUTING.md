# Contributing to Polis

Polis is a substrate. Your contribution adds slots, content, or tooling that other contributors and players build on. Read [`README.md`](README.md), [`GOVERNANCE.md`](GOVERNANCE.md), and the doctrine docs in the repo root ([`SKILLS-DESIGN.md`](SKILLS-DESIGN.md), [`MORTALITY-DESIGN.md`](MORTALITY-DESIGN.md)) before opening anything substantive.

This document covers:
- The three contribution tiers and which license/reward applies
- How to propose schema changes
- How to author reference configs
- Tier 3 original creation submission flow
- The DCO + CLA system
- Voice / framing / quality bar
- Review process

---

## 1. Three contribution tiers

### Tier 1 — Spec / code (recognition)

**What:** schema definitions, SDK packages, generated bindings, examples, validators, CLI tooling, docs.

**Examples:**
- Add a `civic_rights` field to `country.schema.json`
- Fix a typo in TS bindings
- Add a Python SDK example for character spawning
- Improve `polis-cli validate` error messages
- Translate contributor docs into another language

**License:** Apache 2.0 (this repository's `LICENSE`).

**Process:**
1. Open an issue describing the change (use the schema-proposal or bug-report template)
2. Wait for triage — non-substantive changes get fast-tracked; schema changes go to RFC review
3. Submit a PR with the change, signing the DCO (`-s` on commits)
4. Founder review at v0; reviewer pool review at v1+

**Reward:** named in `CONTRIBUTORS.md`, governance vote at v2+.

### Tier 2 — Reference content (paid bounty)

**What:** all open-source content that ships with the platform — countries, industries, worlds, public-domain corpus adaptations, system seeds (government incumbents, regulators, anchor characters), and reference institutions used as templates.

**Important:** Countries, industries, and worlds are **open-source-driven, not in-app founded**. The only way a new country (e.g. the Republic of Westonia), a new industry (e.g. Boxing), or a new world (e.g. Late Roman Republic) lands in the substrate is via Tier 2 PR to this repository. There is no in-app "Found a country" flow.

**Examples:**
- Author a new country template at `configs/countries/<your-country>/` (constitution + filed laws + government slots + regulators)
- Author a new industry template at `configs/industries/<your-industry>/` (professions with hard-skill growth curves, soft-skill weights, institution types, events)
- Curate a new world (V2+ milestone) — Cyberpunk 2099, Late Roman Republic, etc.
- Adapt UK Defamation Act 2013 → Foxbridge Defamation Act for England-on-Polis (or analogous public-domain source for other countries)
- Author system seeds (cabinet incumbents, regulators, anchor characters in `seeds/`)

**License:** CC-BY 4.0 (content) + MIT (any glue code).

**Process:**
1. Open an issue describing the proposed contribution. For a new country / industry / world, fork the existing template (`configs/countries/england-on-polis/`, `configs/industries/football-modern-earth/`) as the structural baseline.
2. Wait for bounty signal: the staq may post a bounty for reference work; you can also propose unsolicited.
3. Negotiate scope + bounty + timeline.
4. Submit a PR; voice / framing review per [§4 below](#4-voice-and-framing-bar).
5. Merged content ships as part of the platform; you're paid the bounty + named credit.

**Reward:** Polis-paid bounty + named credit. **No perpetual royalty** — Tier 2 contributions become part of the substrate's reference content and are bundled with the platform under CC-BY 4.0.

### Tier 3 — Original in-app creation (perpetual royalty)

**What:** original creations that spin up *inside* an existing country and industry on the running substrate — the institutions you found, the characters you spawn, and the smart-contract templates you author. These are the only Tier 3 surfaces. Countries, industries, and worlds are **not** Tier 3 — they live in Tier 2 above.

**Examples:**
- Found Brackensley Park United, a new club in the Foxbridge Premiership (a Tier 3 institution under the football industry, in England-on-Polis)
- Found the Hartford Conservatoire, an academy institution
- Spawn an original primary character (the player's narrative anchor) or a secondary character with a paid spawn fee
- Submit a smart-contract template (factory-deployed only) — e.g. a sponsorship escrow, an academy-graduate-sell-on clause

**License:** **Creator-owned with license-to-host grant to Polis.** Your creation runs only on Polis (this is what makes the substrate defensible — and it's what backs your royalty stream).

**Royalty terms:**
- **Cap: 0.5%** of in-substrate transactions involving the creation. Hard ceiling at the engine layer.
- The exact rate within the cap is set per-creation at submission, subject to founder review.
- Royalty accrues on a defined event set (e.g. ticket sales for a club institution, smart-contract execution fees for a template) and is paid out periodically per the substrate's settlement cadence.

**Process:**
1. Tier 3 creations require a **Tier 3 Contributor License Agreement (CLA)** signed before submission. The CLA grants the staq the right to host + run + collect platform fees on your creation; you retain ownership and the perpetual royalty stream.
2. Sign the CLA — drafted before V1; until then, request the current draft directly from the staq via the contact channel in [`SECURITY.md`](SECURITY.md).
3. KYC Tier 2 verification — required for any creation that will earn royalties (regulatory compliance for revenue-bearing accounts).
4. Submit your creation through the in-app "Found Institution" / "Spawn Character" / "Author Smart Contract" flow once V1 alpha opens. (V0 closed alpha pre-dates these flows; the staq curates Tier 3 directly.)
5. Pass the schema validators + voice review + LLM-judge sensitivity check + factory approval (for smart contracts).
6. Founder review at v0; reviewer pool review at v1+ (see [`GOVERNANCE.md`](GOVERNANCE.md)).
7. Merged creation goes live in the substrate; royalty stream begins.

**Reward:** perpetual royalty (capped at 0.5%) on in-substrate activity within your creation. Realistic V1+ ranges: low-to-mid four figures USD/yr for an active modest institution; higher for institutions that compound supporter engagement.

---

## 2. Schema changes (RFC process at V1+)

At v0, schema changes are founder-reviewed and approved/rejected. **Substantive schema changes require an RFC at v1+.**

A schema change is *substantive* if any of:
- Adds or removes a required field
- Changes a constraint (e.g. raising max tax rate)
- Changes the cognition.corpora structure
- Affects substrate guardrails (engine hard floors, country / industry / institution constraints)

**RFC process** (v1+, modeled on Rust RFCs / Python PEPs / Solana SIMD):
1. Open a discussion in `Discussions > Schema RFCs` describing the proposed change, motivation, and impact on existing configs
2. 14-day comment period; community + maintainers review
3. RFC accepted, rejected, or sent for revision
4. Accepted RFCs become a numbered `RFC-NNNN.md` under `docs/rfcs/` and the schema PR can land

**At v0**, skip the RFC formalism; open an issue with the proposal, get founder approval, then PR.

---

## 3. Sign-off — DCO and CLA

### Developer Certificate of Origin (DCO) — Tier 1 + Tier 2

All commits to this repository must be signed off with the DCO:

```bash
git commit -s -m "your commit message"
```

This adds a `Signed-off-by: Your Name <your.email@example.com>` trailer indicating you wrote the contribution and certify the [Developer Certificate of Origin](https://developercertificate.org/).

PRs without DCO sign-off will be blocked by CI. There's no separate CLA paperwork for Tier 1 + Tier 2.

### Tier 3 CLA

Tier 3 contributions (institutions, characters, smart-contract templates earning royalties) require an explicit Contributor License Agreement signed before review. The CLA is drafted before V1; until then, request the current draft directly from the staq.

The Tier 3 CLA grants:
- **To the staq:** the right to host, run, and operate your creation on the Polis substrate; the right to collect platform-level fees on transactions in your creation.
- **You retain:** ownership of the creation; the perpetual royalty stream (capped at 0.5%); the right to modify your creation through normal governance.
- **Restrictions:** your creation runs only on Polis; the CLA terminates if Polis ceases operations (with substrate state preservation guaranteed by the platform's wind-down policy).

---

## 4. Voice and framing bar

Polis has a distinctive editorial voice. Reference content (Tier 2) and original creations (Tier 3) must hold this voice:

- **Substrate-fictional, not real.** "England-on-Polis" not "England." "Foxbridge Defamation Act" not "UK Defamation Act 2013." LLM-judge refuses real names at the model layer.
- **Editorial, not chatbot.** Reads like a serious newspaper / academic reference, not generated SaaS marketing copy. No filler, throat-clearing, or hype words ("delve," "robust," "comprehensive," "unleash," etc.).
- **Information-dense.** Tables, lists, named entities, real numbers. Tabular numerals on every number.
- **Adapted from sources, not invented.** Most country / industry content can be adapted from public-domain or open-license sources (per `polis/configs/sources.yaml`). Adapt structure; preserve license attribution; substrate-fictionalize names.
- **Tone reference:** the existing `england-on-polis/` and `football-modern-earth/` configs are the bar. Read them before writing yours.

PRs that fail voice review will be sent back with specific notes on which lines / paragraphs / structures need rework.

---

## 5. Review process

### Tier 1 (spec / code)

- Trivial changes (typo, formatting, doc fix): merged within 48 hr of opening at v0
- Substantive changes (new field, validator behavior change): founder review at v0; reviewer pool at v1+
- Schema changes: RFC at v1+ (per §2)

### Tier 2 (reference impl)

- Bounty + scope agreed before work starts
- PR review covers: schema validation, voice / framing, completeness against agreed scope
- Merged within 1-2 weeks of PR opening if review passes

### Tier 3 (original in-app creation)

- CLA + KYC Tier 2 verification before review begins
- For institutions: meet the institution-type's `min_capital_pol` requirement set by the parent industry config (e.g. football clubs require ₽50,000 starting capital per the football industry template)
- For smart-contract templates: factory-approval review (re-entrancy, integer overflow, access-control, economic-exploit checks)
- PR review covers: schema validation, the substrate's six guardrail layers (engine hard floors / constructive bounds / contribution review / runtime / cross-country / termination), voice / framing
- Founder review at v0; reviewer pool at v1+
- Merged when all gates pass; goes live in substrate

---

## 6. PR template

Every PR includes:

- **Tier (1 / 2 / 3)** — which contribution tier
- **Summary** — what changed and why
- **Schema impact** — does this touch a schema file? If so, link to RFC (v1+) or proposing issue
- **Voice / framing review** — does the content match the bar in §4?
- **Test coverage** — for code: tests added or updated? For configs: round-trip validation passes?
- **DCO sign-off** — present in commit trailers
- **License** — confirms the contribution license (Apache 2 / CC-BY / Tier 3 CLA)

CI checks block merge until:
- Schema validators pass
- DCO sign-off present
- Voice-review checklist (Tier 2 + Tier 3) acknowledged
- Tests added for code changes

---

## 7. Code of conduct

[Contributor Covenant 2.1](CODE_OF_CONDUCT.md). Bad-faith contributions (spam, harassment, sanctioned-individual entry attempts, real-world impersonation) are deplatformed without notice.

---

## 8. Where to ask questions

- General contribution questions: GitHub Discussions
- Schema-design questions: `Discussions > Schema design`
- Tier 3 creation interest: `Discussions > Original creations`
- Security disclosure: see [`SECURITY.md`](SECURITY.md), do NOT open public issues

---

**Polis is operated by the staq. By contributing, you agree to the license, governance, and code-of-conduct terms above.**
