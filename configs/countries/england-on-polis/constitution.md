# Constitution of England-on-Polis

*A Westminster-shape parliamentary democracy with common-law tradition. Adapted from the Constituteproject.org Westminster template (CC-BY 4.0); names substrate-fictionalised per `polis/configs/sources.yaml`.*

---

## Preamble

The People of England-on-Polis, recognising the inherited tradition of parliamentary supremacy, common law, and the rule of law, declare this Constitution to settle the form of government, the rights of the governed, and the limits of authority. The country is one and indivisible, organised as a constitutional democracy.

## I. Sovereignty

1. Sovereignty resides in the people, exercised through Parliament under the authority of this Constitution.
2. Parliament is supreme in matters within its competence, subject to the rights guaranteed by Article IV and the bounds set by the engine layer of the substrate (CSAM prohibition, real-world threats prohibition, sanctions compliance — non-overridable).
3. No subdivision, institution, or office may exercise authority beyond what this Constitution and the laws made under it allow.

## II. Government

1. The Executive is led by a Prime Minister, the head of government and head of state, who serves at the confidence of Parliament.
2. The Cabinet comprises ministers appointed by the Prime Minister, each holding portfolio responsibility for a defined area of state action (Treasury, Justice, Foreign Affairs, Sport, Labour, Home, Health).
3. Cabinet decisions are collective; ministerial dissent is resolved within Cabinet or by resignation.
4. The Civil Service is permanent, professional, and politically neutral. The Cabinet Secretary heads the Civil Service and serves successive governments.

## III. Parliament

1. Parliament consists of two chambers: a directly-elected House of Commons-Equivalent (412 seats, four-year term, FPTP) and an appointed House of Review (180 seats, twelve-year term).
2. The House of Commons-Equivalent has primacy on matters of supply (taxation, expenditure) and confidence in the government.
3. The House of Review may amend, delay, or recommend reconsideration of legislation, but may not block supply or extend the term of Parliament.
4. Bills become law on the assent of both chambers and the head of state. Money bills require only the consent of the House of Commons-Equivalent.

## IV. Rights

The following rights are guaranteed and may not be abrogated by simple legislative majority. Constitutional change to this Article requires two-thirds majority of both chambers and a popular referendum.

1. **Equality before the law.** No person shall be denied the equal protection of the laws of England-on-Polis on grounds of race, colour, sex, language, religion, political opinion, or social origin.
2. **Due process.** No person shall be deprived of life, liberty, or property without due process of law. Citizenship-stripping requires judicial ruling per Article VII.
3. **Property rights.** Lawful property may not be expropriated without due process and just compensation. Maximum income tax 65% per substrate guardrails.
4. **Press freedom.** Freedom of speech and of the press is guaranteed. Libel laws apply per the Foxbridge Defamation Act.
5. **Freedom of assembly.** Peaceful assembly is guaranteed.
6. **Freedom of movement.** Citizens have the right to enter, leave, and reside anywhere within England-on-Polis. Engine refuses workflow actions that would block emigration.
7. **Habeas corpus.** No person shall be detained without lawful authority and notice of charge.

## V. Judiciary

1. The Judiciary is independent of the Executive and Legislature.
2. The Supreme Court of Foxbridge is the apex court (9 justices, appointed by merit-commission recommendation; lifetime tenure pending good behaviour).
3. England-on-Polis follows common-law tradition: judicial precedent is binding on lower courts; superior courts may distinguish, refine, or overrule precedent.
4. Justices may not opine publicly on pending cases or extra-judicially on contested matters.

## VI. Subdivisions

1. England-on-Polis is divided into 11 counties (Hartshire, Foxbridge, Northshire, Westmark, Southhaven, Eastmoor, Midshire, Cathermere, Stonebridge, Greycombe County, Salt Fells).
2. Counties may have their own councils with limited governance authority. The county of Foxbridge (capital region) has additional taxation authority by special Act.
3. Counties may not legislate inconsistent with national law. Engine validates against country-template constraints at config-load time.

## VII. Citizenship

1. Citizenship is acquired by birth (jus soli within England-on-Polis territory or jus sanguinis to a citizen parent), by naturalisation (after 5 years of lawful residence), or by special grant of Parliament.
2. Dual citizenship is permitted.
3. Citizenship may not be stripped except by judicial ruling on grounds of fraud in acquisition or treason.

## VIII. Foreign Relations

1. The Foreign Secretary represents England-on-Polis in foreign affairs at the direction of the Prime Minister.
2. Treaties require ratification by the House of Commons-Equivalent. Treaties may not override Article IV rights or Article XI sanctions floors.
3. Recognition of new countries (V1+ when other countries spawn in the world) requires a Cabinet decision and parliamentary notice.

## IX. Currency and Economy

1. The lawful currency of England-on-Polis is POL (the substrate's reserve currency), held in custodial wallets and settled on Devnet (V0) / mainnet (V1+) per the substrate's saga / outbox.
2. Country may issue its own currency by special Act; not exercised at V0 (`country.currency.enabled: false`).
3. Monetary policy at V0 is non-discretionary (POL-only). Bank of Foxbridge holds central-bank powers but does not issue currency.

## X. Emergency Powers

1. In time of war or grave emergency, Parliament may authorise temporary suspension of specified Article IV rights for a defined period not exceeding 12 months without renewal.
2. CSAM prohibition, real-world threats prohibition, and engine-level hard floors are not subject to emergency suspension. They are non-overridable.

## XI. Engine Hard Floors

The following are guaranteed by the substrate engine and may not be overridden by any law of England-on-Polis:

1. Prohibition of CSAM in any form.
2. Prohibition of real-world threats and doxxing.
3. Compliance with OFAC / UN / EU sanctions screening on individuals and jurisdictions.
4. Anti-CSAM-imagery age-verification on imagery.
5. Anti-doxxing.

These floors apply regardless of the will of Parliament, the Cabinet, the Judiciary, or any other authority within England-on-Polis. They are part of the substrate's social contract with all worlds.

## XII. Amendment

1. Articles I, II, III, V, VI, VII, VIII, IX, X may be amended by simple majority of both chambers + head of state assent.
2. Article IV (Rights) requires two-thirds majority of both chambers + popular referendum.
3. Article XI (Engine Hard Floors) cannot be amended by any process within England-on-Polis. Engine enforces.

## XIII. Effective Date

This Constitution takes effect on the founding date of England-on-Polis (16 December 1689 in-world; 2026-08-01 in-real-world per `country.founded_in_world`). Subsequent laws and regulations are made under its authority.

---

*Adapted from Constituteproject.org Westminster template (CC-BY 4.0). Substrate-fictionalised per `polis/configs/sources.yaml`. Authored by the staq as Tier 2 reference content per OPEN-SOURCE.md.*
