# Foxbridge Employment Act

*An Act to consolidate the law on employment, working time, minimum wage, dismissal, and industrial relations in England-on-Polis. Adapted from the Employment Rights Act 1996, Working Time Regulations 1998, and National Minimum Wage Act 1998 of the United Kingdom (Open Government Licence v3.0). Substrate-fictionalised per `polis/configs/sources.yaml`.*

---

## Part 1 — Employment relationship

### §1 Definition

An "employee" in England-on-Polis means a natural person (or, where character-substrate applies, a substrate character with persistent identity) engaged by an institution under a contract of employment, whether written or oral, full-time or part-time, fixed-term or permanent.

### §2 Written statement of particulars

(1) An employer must give every employee a written statement of particulars within **two months** of the start of employment, including:
  (a) the names of employer and employee;
  (b) the date of commencement;
  (c) the title and nature of the position;
  (d) the rate of pay (POL per period) and pay interval;
  (e) hours of work, holiday entitlement;
  (f) notice period required by either party;
  (g) place of work;
  (h) collective agreements (if applicable);
  (i) procedures for grievance and discipline.

*Substrate note: contract.schema.json instances satisfy §2 when properly populated. Engine refuses an employment contract that lacks any of (a)–(i).*

## Part 2 — Minimum wage

### §3 Minimum wage rate

(1) The minimum wage in England-on-Polis is **₽12 per hour** (₽480 per 40-hour week; ₽25,000 per annum at standard hours).

(2) The minimum wage applies to all employees aged 18 and over.

(3) For employees aged 16-17, the minimum wage is ₽9 per hour.

(4) The Treasury Minister may by regulation revise the minimum wage; revisions take effect on the first day of the new fiscal year following parliamentary notice.

### §4 Enforcement

(1) An employer paying below the statutory minimum wage commits an offence and is liable to:
  (a) repay the underpayment to the employee;
  (b) pay a civil penalty of 200% of the underpayment to Inland Revenue Foxbridge;
  (c) be named on the public register of underpaying employers maintained by the Labour Minister.

*Engine note: ConflictWorkflow surfaces wage-underpayment as a §3 violation when contract.compensation.base_salary_pol_per_month falls below ₽2,080 (= ₽12 × 40 × 52 / 12) for a full-time role. Football-clubs are not exempt.*

## Part 3 — Working time

### §5 Maximum working week

(1) Average weekly working time, including overtime, shall not exceed **48 hours**, averaged over a 17-week reference period.

(2) An employee may opt out of §5(1) by signed agreement; the opt-out is revocable by 7 days' notice.

### §6 Rest periods

(1) An employee is entitled to:
  (a) a daily rest period of not less than **11 consecutive hours** in each 24-hour period;
  (b) a weekly rest period of not less than **24 consecutive hours** in each 7-day period;
  (c) a rest break of not less than **20 minutes** if the working day is longer than 6 hours.

### §7 Annual leave

(1) An employee is entitled to **28 days** of paid annual leave per year (5.6 weeks), which may include public holidays.

(2) Annual leave shall not be replaced by a payment in lieu except on termination of employment.

## Part 4 — Termination of employment

### §8 Notice period

(1) The minimum statutory notice an employer must give to an employee is:
  (a) one week, if the employee has been continuously employed for 1 month to 2 years;
  (b) one week per year of service, where employed 2 to 12 years (capped at 12 weeks).

(2) The minimum statutory notice an employee must give to an employer is **one week** after one month of continuous employment.

(3) A contract may specify longer notice; the longer notice prevails.

### §9 Unfair dismissal

(1) An employee with at least **2 years** of continuous service has the right not to be **unfairly dismissed**.

(2) A dismissal is fair only if the reason is:
  (a) capability or qualifications;
  (b) conduct;
  (c) redundancy;
  (d) statutory restriction (a legal bar to continued employment);
  (e) some other substantial reason.

(3) The dismissal must follow a fair procedure: investigation, opportunity to respond, written reasons, right of appeal.

### §10 Wrongful dismissal

(1) An employee dismissed in breach of contract (e.g., without contractual notice) may claim damages for wrongful dismissal in addition to or in place of an unfair-dismissal claim.

(2) Wrongful-dismissal damages are limited to losses flowing from the breach (typically the value of the notice period).

### §11 Constructive dismissal

(1) An employee who resigns in response to a fundamental breach of contract by the employer (e.g., unilateral pay cut, significant role change without consent, persistent harassment) may claim that the resignation amounts to dismissal at the employer's behest.

*Engine note: ConflictWorkflow handles §11 cases via the conflict.schema.json instance with `kind: contract_breach` and `claimant_role: employee`. Sergei Czerny's wage-underpayment dispute (basketball CI fixture, c_czerny v c_hartwell-fc) follows this branch.*

### §12 Redundancy payment

(1) An employee with at least **2 years** of continuous service who is dismissed by reason of redundancy is entitled to a redundancy payment of:
  (a) 0.5 weeks' pay per year of service for each year aged under 22;
  (b) 1 week's pay per year of service for each year aged 22 to 41;
  (c) 1.5 weeks' pay per year of service for each year aged 42 and over;

with a maximum of 20 years counted and a weekly cap of ₽700.

## Part 5 — Discrimination and harassment

### §13 Prohibited grounds

It is unlawful to discriminate against an employee or job applicant on grounds of:
  (a) sex, gender identity, sexual orientation;
  (b) race, colour, national origin, ethnic origin;
  (c) religion or belief (or lack thereof);
  (d) age;
  (e) disability;
  (f) marital or civil-partnership status;
  (g) pregnancy or maternity;
  (h) trade-union membership or activity.

### §14 Forms of discrimination

Direct discrimination, indirect discrimination, harassment (creating a hostile, degrading, or offensive environment), and victimisation (penalising someone for invoking their rights) are all unlawful.

### §15 Burden of proof

In any claim under §13–14, the employee must establish a prima facie case; thereafter the burden shifts to the employer to show that the treatment was for a non-discriminatory reason.

## Part 6 — Trade unions and industrial action

### §16 Right to associate

Every employee has the right to join a trade union of their choice. An employer may not penalise an employee for trade-union membership or non-membership, lawful trade-union activity, or use of statutory grievance procedures.

### §17 Industrial action

Lawful industrial action requires:
  (a) a secret postal ballot of affected members;
  (b) majority support of those voting;
  (c) seven days' notice to the employer.

Wildcat strikes, secondary action against unrelated employers, and political strikes are unlawful.

### §18 Collective bargaining

Where a trade union is recognised by an employer (statutorily or voluntarily), the employer must consult the union in good faith on:
  (a) pay and conditions;
  (b) collective dismissals;
  (c) transfer of undertakings;
  (d) pension changes.

## Part 7 — Sport-specific provisions

### §19 Athletes and football professionals

(1) An athlete employed by a football club, university, or other sports institution is an "employee" within §1 unless the contract clearly establishes self-employment (e.g., individual-sport prize-money contracts).

(2) The minimum-wage requirement (§3) applies to football professionals, including academy and reserve players. Academy players under 18 are subject to the youth rate (§3(3)).

(3) A footballer dismissed mid-contract has the rights of §9–10 plus contract-breach damages calculated under contract.schema.json `breach_remedies`.

(4) The Federation of Hartshire (football regulator) may impose additional fitness-to-play and integrity standards beyond §13–18; such standards must not undercut the floor set by this Act.

*Engine note: §19 is what makes contract.schema.json apply to footballer.contracts. ConflictWorkflow uses this section when ruling on Czerny-style mid-contract pay disputes.*

## Part 8 — Enforcement and remedies

### §20 Employment Tribunal of Foxbridge

(1) The Employment Tribunal of Foxbridge has exclusive jurisdiction over claims under this Act.

(2) Claims must be brought within **3 months** of the act complained of (or, in redundancy / unfair dismissal cases, within 3 months of the effective date of termination).

(3) Tribunal decisions may be appealed to the Court of Appeal of Foxbridge on points of law.

### §21 Maximum compensation

(1) Compensation for unfair dismissal is the lower of:
  (a) ₽105,000;
  (b) 52 weeks' pay.

(2) Compensation for discrimination is uncapped and may include damages for injury to feelings.

(3) Compensation for wrongful dismissal is the contractual notice period plus contractual benefits.

## Part 9 — Citation, commencement, and extent

### §22 Short title, commencement, and extent

(1) This Act may be cited as the **Foxbridge Employment Act**.

(2) This Act came into force on **2026-08-01** in-world.

(3) This Act extends to England-on-Polis only.

---

## Engine and substrate notes (not part of the Act)

- ConflictWorkflow uses §1 to confirm employee status, §3 to test wage compliance, §8–11 to test termination validity, §13–14 to test discrimination, §17 to test industrial-action lawfulness, §19 to apply sport-specific overlays, §20 for venue.
- The minimum-wage figure (₽12/hour, ₽480/week, ₽25,000/year) is duplicated in `country.yaml` `laws.labour.minimum_wage_pol_per_week: 480`. The two MUST stay in sync; CI invariant test enforces.
- Substrate engine layer has no view on §13 (discrimination); the engine refuses CSAM and real-world threats only. Country-level discrimination rules are enforced at country-content layer.
- ConflictWorkflow precedent retrieval pulls priors from the public_record corpus and from substrate-fictional case law (build out at V1+).

---

*Adapted from Employment Rights Act 1996, Working Time Regulations 1998, National Minimum Wage Act 1998, Equality Act 2010 (UK), Open Government Licence v3.0. Substrate-fictionalised by the staq, 2026. CC-BY-4.0 per `polis/LICENSE-CONTENT`.*
