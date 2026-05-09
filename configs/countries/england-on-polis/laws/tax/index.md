# Foxbridge Tax — index

*Plain-language commentary on the Foxbridge tax regime. Authoritative rates live in the YAML files in this directory and are duplicated in `country.yaml`. Where this commentary differs from the YAML, the YAML wins.*

---

## Overview

England-on-Polis levies tax through **Inland Revenue Foxbridge** under the authority of the **Treasury Minister**. Five principal taxes:

| Tax | Schedule file | Rate at V0 |
|-----|---------------|------------|
| Income tax | `income-tax-brackets.yaml` | progressive 0–50% |
| Corporate tax | `corporate-tax.yaml` | 22% |
| Capital gains tax | `capital-gains.yaml` | 25% |
| Property tax | `property-tax.yaml` | 1.2% annual on real property |
| Transfer tax | `transfer-tax.yaml` | 4% on transfer agreements (incl. football) |

The fiscal year runs **6 April to 5 April**. Returns are due by 31 January (online) following the end of the fiscal year.

## Income tax

Withheld at source (PAYE) for employed earners. Self-assessed for self-employed, high investment income, or income above ₽100,000. Personal allowance ₽12,500, tapered above ₽125,000. Brackets:

- 20% on income ₽12,500 – ₽50,000
- 30% on income ₽50,000 – ₽125,000
- 40% on income ₽125,000 – ₽250,000
- 50% on income above ₽250,000

Maximum effective rate is bounded by Constitution Article IV §3 (no expropriation; max income tax 65% per substrate guardrails).

## Corporate tax

Headline rate **22%** on company profits, applied to all corporate forms registered under Foxbridge Corporations Act §1. Football-club mutuals are subject at the same rate; not-for-profit Community Interest Companies have access to capped distribution allowances.

## Capital gains

Headline rate **25%** on net gains from disposal of capital assets. Annual exempt amount ₽12,300. Principal-private-residence exemption applies to a sole or main home. Footballer image-rights companies are subject at the corporate rate; gains on disposal of player registrations by clubs are subject to corporate tax, not CGT.

## Property tax

Annual **1.2%** of registered taxable value of real property. Levied on residential and commercial real property; football grounds and stadia subject. Capital region (county of Foxbridge) may levy additional council-tax-equivalent under Constitution Article VI §2.

## Transfer tax

**4%** on transfers of:
  (a) real property (paid by the buyer);
  (b) shares above thresholds;
  (c) **football transfer fees** (paid by the selling club, per Foxbridge Football Act §8(3)).

## Anti-avoidance

The Foxbridge General Anti-Abuse Rule applies to arrangements whose main purpose is tax avoidance and which lack commercial substance. HMRC-equivalent has discretion to recharacterise transactions per the Rule.

## Football-tax interaction

(1) Player wages: PAYE at source, employer payroll-tax overlay.
(2) Image rights: corporate-rate where genuine commercial structure; recharacterised per anti-avoidance where purpose is salary-disguise.
(3) Transfer fees: 4% transfer tax payable by selling club within 30 days of registration of the transfer.
(4) Loyalty / signing bonus: spread over contract term for income-tax recognition; full tax in year paid where the bonus is genuinely transactional.

## Authority and compliance

Inland Revenue Foxbridge enforces compliance:
  (a) civil penalties for late filing (₽100), late payment (5% surcharge + interest);
  (b) criminal prosecution for serious evasion under Foxbridge Criminal Code §11–§12;
  (c) public register of tax-defaulting companies maintained for amounts above thresholds.

## Files in this directory

```
laws/tax/
├── index.md                      ← this file
├── income-tax-brackets.yaml      ← canonical bracket schedule
├── corporate-tax.yaml            ← corporate rate, allowances, group rules
├── capital-gains.yaml            ← CGT rates, allowances, exemptions
├── property-tax.yaml             ← real-property annual rate
└── transfer-tax.yaml             ← transfer tax (football, real estate, shares)
```

---

*Adapted from UK tax provisions: Income Tax (Earnings and Pensions) Act 2003, Corporation Tax Act 2010, Taxation of Chargeable Gains Act 1992, Stamp Duty Land Tax Act 2003, all OGL v3.0. Substrate-fictionalised by the staq, 2026. CC-BY-4.0 per `polis/LICENSE-CONTENT`.*
