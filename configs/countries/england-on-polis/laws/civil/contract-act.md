# Foxbridge Contract Act

*An Act consolidating the common-law and statutory rules of contract in England-on-Polis. Restates the common-law principles inherited from English contract law (Open Government Licence v3.0 for statutory parts; common-law principles unrestricted). Substrate-fictionalised per `polis/configs/sources.yaml`.*

---

## Part 1 — Formation

### §1 Elements of a binding contract

A contract is binding in England-on-Polis when the following are present:
  (a) **Offer** — a definite proposal made with intent to be bound on acceptance;
  (b) **Acceptance** — unconditional assent to the offer, communicated to the offeror;
  (c) **Consideration** — something of value moving from each party (executed or executory);
  (d) **Intention to create legal relations** — presumed in commercial dealings, rebuttable in domestic / social ones;
  (e) **Capacity** — both parties must have legal capacity to contract;
  (f) **Legality** — the subject-matter and purpose must not be illegal, prohibited by statute, or contrary to public policy.

*Engine note: the substrate's `contract.schema.json` operationalises (a)–(f). The principal-agent layer ensures (e) capacity (every contract names principals); the engine refuses (f)-illegal contracts (CSAM, real-world threats, sanctions-listed counterparties).*

### §2 Form

(1) A contract may be made in writing, orally, or by conduct, save where this Act or another Act requires writing.

(2) The following must be in writing:
  (a) contracts for the sale of land or interests in land;
  (b) guarantees and indemnities;
  (c) consumer credit agreements above ₽5,000;
  (d) contracts of employment (per Foxbridge Employment Act §2);
  (e) instruments of transfer for shares in a registered corporation;
  (f) **player-transfer agreements between football clubs** (per Foxbridge Football Act).

*Substrate note: at the engine layer, all substrate contracts are written by virtue of being persisted to the database. §2(2) is a doctrine signal to LLMs and a courtroom-procedure rule, not a substrate-engine rule.*

### §3 Capacity

(1) An adult of sound mind has full contractual capacity.

(2) A minor (under 18) may contract for **necessaries** (food, clothing, education, lodging suitable to their station) and for **beneficial contracts of service** (e.g., apprenticeship, athletic training); other contracts are voidable at the minor's option.

(3) A character certified by judicial order as lacking capacity may not bind themselves contractually save through their appointed guardian.

(4) An institution acts through its agents; an agent's authority binds the institution within the scope of actual or apparent authority.

*Substrate note: principal-agent layer in `character.schema.json` enforces §3(3) directly — auto-decision rules and ping rules are how a character delegates capacity. A contract entered in violation of an explicit standing-order limit is voidable per §3(2) reasoning extended to substrate principals.*

## Part 2 — Terms

### §4 Express and implied terms

(1) **Express terms** are those agreed and communicated by the parties.

(2) **Implied terms** arise from:
  (a) common-law presumption (e.g., the duty of good-faith performance);
  (b) statute (e.g., the implied terms of fitness for purpose in commercial sales);
  (c) custom of trade (e.g., the customary terms of football transfer);
  (d) the necessary intent of the parties (the "officious bystander" test).

### §5 Conditions, warranties, and innominate terms

(1) A **condition** is a fundamental term, breach of which entitles the innocent party to terminate the contract.

(2) A **warranty** is a less fundamental term, breach of which entitles the innocent party to damages but not termination.

(3) An **innominate term** is one whose effect on breach depends on the gravity of the breach.

### §6 Exemption clauses

(1) A clause excluding or limiting liability for breach is enforceable only insofar as it is:
  (a) clearly drafted;
  (b) reasonable in the circumstances; and
  (c) not contrary to specific statutory prohibition (e.g., one cannot exclude liability for personal injury caused by negligence).

## Part 3 — Vitiating factors

### §7 Misrepresentation

(1) A contract induced by **fraudulent misrepresentation** (a false statement made knowingly or recklessly) is voidable; the innocent party may rescind and claim damages in deceit.

(2) A contract induced by **negligent misrepresentation** is voidable; the innocent party may rescind and claim damages.

(3) A contract induced by **innocent misrepresentation** is voidable; rescission is the primary remedy, damages discretionary.

### §8 Mistake

(1) A **common mistake** as to a fundamental fact rendering the contract impossible to perform may render the contract void.

(2) A **mutual mistake** (each party meaning a different thing) prevents formation if the disagreement is material.

(3) A **unilateral mistake** as to identity, where the identity of the counterparty was material, may render the contract void.

### §9 Duress and undue influence

(1) A contract entered under physical or economic duress is voidable.

(2) A contract entered under undue influence (a relationship of trust exploited by the dominant party) is voidable; in fiduciary relationships, undue influence is presumed and must be rebutted.

### §10 Unconscionability

A court may set aside a contract that is, on its face, so substantively unfair as to shock the conscience of a reasonable person — particularly where bargaining power is grossly unequal.

## Part 4 — Performance and discharge

### §11 Performance

(1) A contract is discharged by full and exact performance of all its terms.

(2) Substantial performance, where minor defects do not go to the root of the contract, entitles the performing party to payment less the cost of remedying defects.

### §12 Frustration

(1) A contract is discharged by **frustration** when, after formation, an event without fault of either party renders performance impossible, illegal, or radically different from what was contemplated.

(2) Examples include destruction of the subject-matter, supervening illegality, death or incapacity in personal contracts, and (in football) career-ending injury where the contract is for personal performance.

### §13 Agreement and accord

A contract may be discharged by mutual agreement, supported by fresh consideration (or a deed under seal). Accord and satisfaction occurs where one party accepts substituted performance in discharge of the original obligation.

### §14 Breach

(1) **Anticipatory breach** occurs where one party signals before the time for performance that they will not perform; the innocent party may treat the contract as repudiated and sue immediately.

(2) **Actual breach** occurs at the time of performance.

(3) Breach of a condition entitles the innocent party to terminate and claim damages; breach of a warranty entitles the innocent party to damages only.

## Part 5 — Remedies

### §15 Damages

(1) The aim of damages is to put the claimant in the position they would have been in had the contract been performed (the "expectation" measure).

(2) Damages are recoverable for losses that are:
  (a) caused by the breach (factual and legal causation);
  (b) not too remote (within reasonable contemplation of the parties at formation, per the *Hadley v Baxendale*-type rule);
  (c) reasonably mitigated by the claimant.

(3) **Liquidated damages** clauses (genuine pre-estimates of loss) are enforceable; **penalty clauses** (in terrorem) are not.

(4) Non-pecuniary loss (distress, disappointment) is recoverable only where the contract's primary object was peace of mind, comfort, or the avoidance of distress.

### §16 Specific performance

(1) The court may order specific performance where damages are inadequate (typically: unique goods, land, or — in football — a player whose distinctive talent the buying club cannot replicate by purchase).

(2) Specific performance is not awarded for contracts of personal service (cannot order a player or manager to play / coach against their will), though negative covenants (no playing for rival club) may be enforced by injunction.

*Engine note: contract.schema.json `breach_remedies.kind: specific_performance` is rare in V0; the engine's default is `damages_only`. Football transfer contracts use injunctions per §16(2) to bar rival-club registration during a contested transfer window.*

### §17 Restitution

(1) Where a contract is rescinded for misrepresentation, mistake, or other vitiating factor, the parties are restored to their pre-contract positions so far as possible.

(2) Restitution is also available where money was paid for consideration that has totally failed.

### §18 Injunctions

The court may grant an injunction to restrain breach of a negative covenant (a contractual promise not to do something), particularly where damages would be inadequate.

## Part 6 — Third parties

### §19 Privity

(1) The general rule is that only parties to the contract have rights and obligations under it.

(2) **Exceptions**:
  (a) the **Contracts (Rights of Third Parties) of Foxbridge Act** rule: a third party expressly named or in a class identified may sue to enforce a benefit conferred on them, unless the contract reserves the parties' right to vary;
  (b) trusts of contractual rights;
  (c) statutory exceptions (insurance, employment-pension nominations);
  (d) agency.

## Part 7 — Standard-form, consumer, and sport contracts

### §20 Consumer contracts

A contract between a trader and a consumer is subject to enhanced fairness protections (cooling-off rights for distance contracts, mandatory term disclosure, prohibition of unfair terms). The detail is in the Foxbridge Consumer Rights Act.

### §21 Player and manager contracts (football)

(1) Contracts between football clubs and footballers / managers must comply with:
  (a) this Act (general contract principles);
  (b) Foxbridge Employment Act (minimum wage, dismissal, holiday);
  (c) Foxbridge Football Act (transfer-window restrictions, registration, integrity);
  (d) Federation of Hartshire rules (match eligibility, doping, dispute resolution).

(2) The hierarchy in case of conflict: §21(1)(a) general contract law → §21(1)(b) statutory employment floor → §21(1)(c) statutory football regime → §21(1)(d) Federation rules.

(3) Federation rules cannot undercut the floors set by §21(1)(a)–(c).

*Substrate note: §21 is the layered-law structure substrate engine uses to evaluate disputes around `contract.kind: footballer_employment`.*

## Part 8 — Citation, commencement, and extent

### §22 Short title, commencement, and extent

(1) This Act may be cited as the **Foxbridge Contract Act**.

(2) This Act came into force on **2026-08-01** in-world.

(3) This Act extends to England-on-Polis only.

---

*Common-law restatement adapted from English contract-law principles (which are common-law and so freely adaptable). Statutory parts adapted from the UK's Misrepresentation Act 1967, Sale of Goods Act 1979, Unfair Contract Terms Act 1977, and Contracts (Rights of Third Parties) Act 1999, all OGL v3.0. Substrate-fictionalised by the staq, 2026. CC-BY-4.0 per `polis/LICENSE-CONTENT`.*
