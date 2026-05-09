# Foxbridge Football Act

*An Act regulating association football in England-on-Polis: club licensing, broadcasting, gambling, integrity, transfer regulation, supporters' interests. Adapted from the UK Football Spectators Act 1989, Football (Offences) Act 1991, Sporting Bodies (Integrity) regulations, and the FA Rules / EFL Regulations (publicly available). Substrate-fictionalised per `polis/configs/sources.yaml`.*

---

## Part 1 — Federation of Hartshire

### §1 Recognition and authority

(1) The **Federation of Hartshire** is the recognised governing body for association football in England-on-Polis.

(2) The Federation has authority to:
  (a) license clubs in tiers 1–4 of the football pyramid;
  (b) license referees and match officials;
  (c) operate the Foxbridge Cup and other Federation cups;
  (d) discipline clubs, players, managers, and officials for breaches of Federation rules;
  (e) make and amend rules consistent with this Act;
  (f) settle disputes between member clubs through arbitration.

(3) The Federation answers to the Sport Minister on matters of public policy and to the Foxbridge Conduct Authority on matters of broadcasting and gambling regulation.

*Engine note: institution `federation-of-hartshire` is the sole holder of the regulator slot `country.regulators.sport_governing_bodies[industry_id=football-modern-earth]`. Substrate enforces uniqueness.*

### §2 Federation rules

(1) Federation rules must be published, accessible, and not in conflict with this Act, the Foxbridge Contract Act, the Foxbridge Employment Act, or the Constitution.

(2) Where Federation rules conflict with primary legislation, primary legislation prevails.

(3) Federation rules may be challenged on grounds of public-law unreasonableness in the High Court of Foxbridge.

## Part 2 — Club licensing

### §3 Licence required

(1) No institution may compete in the football pyramid without a current licence from the Federation.

(2) The Federation issues licences for:
  (a) **Tier 1 — Premiership** (top tier);
  (b) **Tier 2 — Championship** (second tier);
  (c) **Tier 3 — Combination** (third tier; Hartshire Combination is the V0 league here);
  (d) **Tier 4 — Counties** (regional fourth tier).

(3) A licence may be granted, refused, varied, suspended, or revoked according to criteria in §4.

### §4 Licensing criteria

A licensee must demonstrate:
  (a) **financial sustainability** — solvency, audited accounts, reasonable forecasts;
  (b) **fit and proper persons** — directors, owners, and management free of disqualifying convictions or sanctions;
  (c) **stadium safety** — compliance with the Foxbridge Stadia Safety regulations;
  (d) **youth and academy provision** — compliant with §6;
  (e) **integrity controls** — anti-betting, anti-match-fixing, anti-doping (§9–§11);
  (f) **labour compliance** — adherence to Foxbridge Employment Act including minimum wage on all player contracts;
  (g) **community engagement** — supporter representation per §17.

### §5 Promotion and relegation

(1) The football pyramid uses promotion and relegation between adjacent tiers.

(2) Tier 1 → Tier 2: bottom 3 of Premiership relegated; top 2 of Championship + 1 playoff winner promoted (per industry config `format: league_with_playoff`).

(3) Tier 2 → Tier 3: bottom 3 of Championship relegated; top 2 of Combination + 1 playoff winner promoted.

(4) Tier 3 → Tier 4: bottom 2 of Combination relegated; top 1 of Counties + 1 playoff winner promoted (or as Federation rules specify).

(5) Promotion is conditional on the promoted club meeting the higher-tier licence criteria within 28 days of promotion.

### §6 Academies and youth

(1) Tier 1 and Tier 2 clubs must operate a youth academy compliant with Federation Academy Regulations.

(2) Players aged under 16 may sign academy scholarship terms; player contracts may not commence before age 17 in the meaning of Foxbridge Employment Act §19.

(3) Compensation for cross-club youth transfers is set by Federation tariff, payable to the developing club.

## Part 3 — Transfers and player movement

### §7 Transfer windows

(1) Player transfers between clubs are permitted only during designated **transfer windows**:
  (a) **Summer window** — 16 June to 31 August inclusive;
  (b) **Winter window** — 1 January to 31 January inclusive.

(2) Outside these windows, intra-Federation transfers are barred save for emergency goalkeeper loans and contract terminations by mutual consent.

### §8 Transfer agreements

(1) A transfer agreement is a contract between two clubs (not the player) for the assignment of registration rights.

(2) The agreement must:
  (a) be in writing per Foxbridge Contract Act §2(2)(f);
  (b) specify the fee (POL), payment schedule, sell-on clauses, performance bonuses, and any conditions;
  (c) be lodged with the Federation within 24 hours of execution;
  (d) be subject to the player's consent to a new employment contract with the buying club.

(3) Transfer fees are subject to **transfer tax at 4%** payable to Inland Revenue Foxbridge by the selling club, per `country.taxation.transfer_tax_rate: 0.04`.

(4) Cross-border transfers (V1+, when other countries spawn) are subject to additional immigration and work-permit requirements.

*Substrate note: contract.schema.json instances of `kind: transfer_agreement` are validated against §8(2). The substrate engine refuses transfer contracts logged outside §7 windows.*

## Part 4 — Broadcasting and commercial rights

### §9 Collective broadcasting

(1) Premiership and Championship broadcasting rights are sold collectively by the Federation on behalf of member clubs.

(2) Distribution of broadcasting revenue is by Federation formula (broadly: equal share + merit + facilities), published annually.

(3) Lower-tier broadcasting rights (Combination and Counties) are sold by individual clubs, subject to Federation registration.

### §10 Foxbridge Conduct Authority oversight

The Foxbridge Conduct Authority (`foxbridge-conduct-authority`) regulates:
  (a) commercial conduct, anti-competitive practice, conflicts of interest in broadcasting tenders;
  (b) the financial-fair-play rules promulgated by the Federation;
  (c) advertising and sponsorship standards in stadia and on broadcasts.

### §11 Gambling

(1) Football-related gambling is permitted only through licensed operators registered with the Foxbridge Gambling Commission.

(2) The following are prohibited:
  (a) **insider betting** — players, managers, agents, or club employees betting on football matches in any competition in which their club participates;
  (b) **fixing** — any conduct intended to influence the outcome of a match for betting or other consideration;
  (c) **tipping** — disclosure of confidential club information for betting advantage.

(3) Breach of §11(2) is a criminal offence under the Foxbridge Sporting Integrity Act and a Federation-rule breach attracting suspension.

*Engine note: ConflictWorkflow flags transactions that pattern-match insider betting via the public_record corpus + character match-affiliation graph.*

## Part 5 — Match-day and supporters

### §12 Stadium safety

Stadia must be licensed by Foxbridge Stadia Safety annually. Capacity, evacuation routes, structural integrity, and crowd-management plans are inspected.

### §13 Banning orders

A court may impose a Football Banning Order on a person convicted of a football-related offence (violence, racial chanting, pitch invasion, missile-throwing). The order bars the person from regulated football matches for a minimum of 3 years.

### §14 Racial and discriminatory chanting

Indecent, racial, or other discriminatory chanting at a regulated football match is a criminal offence, with the offence aggravated where it involves coordinated group conduct.

### §15 Pitch invasion

Going onto the playing area, or any adjacent area to which spectators are not generally admitted, without lawful authority or excuse, is a criminal offence.

### §16 Drink and drugs

Possession of alcohol on transport to / from a regulated football match, and possession of controlled drugs in a stadium, are criminal offences.

### §17 Supporters' representation

(1) Every Tier 1 and Tier 2 club must have a constituted supporters' trust or equivalent body with:
  (a) at least one observer-attendance right at the club's board meetings;
  (b) consultation rights on heritage matters (kit, colours, ground name, ground relocation, club name change).

(2) Heritage changes (kit, name, ground move) require:
  (a) supporters' trust formal consultation;
  (b) Federation approval;
  (c) for Tier 1, parliamentary notice for ground relocation more than 25 km.

## Part 6 — Anti-doping

### §18 Anti-doping authority

The **Foxbridge Anti-Doping Authority** (a sub-body of the Sport Minister's office) operates an anti-doping programme aligned with the World Anti-Doping Code.

### §19 Sanctions

A player found to have committed a doping offence is suspended for:
  (a) 4 years for a first deliberate offence;
  (b) 2 years for a non-deliberate first offence;
  (c) lifetime for a second deliberate offence.

Appeal lies to the Federation Disciplinary Tribunal and thence to the Court of Arbitration for Sport (CAS-equivalent in England-on-Polis).

## Part 7 — Owners and directors

### §20 Fit-and-proper-persons test

A person is **not** fit and proper to be a director, owner, or material shareholder (≥10%) of a licensed football club if they:
  (a) have an unspent conviction for a serious dishonesty, violence, sexual, or sport-corruption offence;
  (b) are subject to a disqualification order under the Foxbridge Companies Act;
  (c) are bankrupt or subject to an Individual Voluntary Arrangement;
  (d) appear on OFAC / UN / EU sanctions lists or any sanctions list maintained by the Foreign Secretary;
  (e) have within the previous 7 years caused a club to enter insolvency proceedings.

### §21 Owner conduct

(1) Ownership conduct that brings the game into disrepute (sustained pattern of failed wage payments, public deception of supporters, undue interference with on-field matters) may attract Federation discipline up to and including licence withdrawal.

(2) The Federation may direct disposal of ownership stakes following a fair-and-proper failure.

## Part 8 — Citation, commencement, and extent

### §22 Short title, commencement, and extent

(1) This Act may be cited as the **Foxbridge Football Act**.

(2) This Act came into force on **2026-08-01** in-world.

(3) This Act extends to England-on-Polis only.

---

## Engine and substrate notes (not part of the Act)

- §3 tier mapping reflects industry config `polis/configs/industries/football-modern-earth/industry.yaml`. The four-tier pyramid + promotion/relegation in §5 must match the industry-config tier_graph; CI invariant tests enforce.
- §4(b) fit-and-proper-persons screen runs at character-creation and at ownership-change. ConflictWorkflow uses §20 criteria.
- §8(3) transfer-tax rate is duplicated in `country.yaml` `taxation.transfer_tax_rate: 0.04`. CI invariant test enforces consistency.
- §11 insider-betting check is implemented in the engine layer (anomaly detection against character-match-affiliation graph + transaction graph).
- §17 supporter-representation is enforced as institution-config requirement at Tier 1 / Tier 2 licensing time.
- §18 anti-doping integration with the WADA-equivalent is V1+; V0 has the legal framework only.

---

*Adapted from Football Spectators Act 1989, Football (Offences) Act 1991, FA Rules, EFL Regulations (UK), all publicly available. Substrate-fictionalised by the staq, 2026. CC-BY-4.0 per `polis/LICENSE-CONTENT`.*
