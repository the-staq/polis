# Foxbridge Corporations Act

*An Act consolidating the law of registered corporations in England-on-Polis: incorporation, governance, share capital, directors' duties, accounts, dissolution. Adapted from the UK Companies Act 2006 (OGL v3.0). Substrate-fictionalised per `polis/configs/sources.yaml`.*

---

## Part 1 — Incorporation

### §1 Forms of corporation

(1) The forms of registered corporation in England-on-Polis are:
  (a) **private company limited by shares** (suffix: Limited / Ltd);
  (b) **public company limited by shares** (suffix: PLC); subject to Foxbridge Securities Regulation;
  (c) **company limited by guarantee** (typically not-for-profit; suffix: Limited);
  (d) **community-interest company** (suffix: CIC); locked asset, capped distributions;
  (e) **football-club mutual** (suffix: MFC); supporter-owned, governance per Foxbridge Football Act.

*Substrate note: a substrate institution mapped to a corporation form must declare the form in `institution.governance.structure` and align governance defaults to the form's statutory floor.*

### §2 Registration

(1) Incorporation requires filing with the **Foxbridge Companies Registry**:
  (a) memorandum of association;
  (b) articles of association (may adopt model articles);
  (c) statement of capital and initial shareholdings;
  (d) statement of proposed officers;
  (e) registered office address;
  (f) statement of compliance.

(2) On registration, the registrar issues a certificate of incorporation. The corporation is a separate legal person from its members, with limited liability for share capital.

## Part 2 — Capital and shares

### §3 Share capital

(1) A company has authorised share capital (an upper limit) and issued share capital (shares actually allotted).

(2) Shares may be of various classes (ordinary, preference, redeemable) with rights set in the articles.

(3) **Reductions of capital** require:
  (a) a special resolution;
  (b) a solvency statement (or court confirmation for public companies);
  (c) protection for creditors.

### §4 Issuance and transfer

(1) Existing shareholders typically have **pre-emption rights** on new issues (right of first refusal pro-rata).

(2) Transfers of shares must be in writing; shareholdings are recorded in the register of members maintained by the company.

### §5 Dividends and distributions

Distributions to shareholders may be made only out of distributable profits (accumulated realised profits less accumulated realised losses), per the Foxbridge Accounting Standards Framework.

## Part 3 — Governance

### §6 Directors

(1) Every private company must have at least one director; every public company at least two.

(2) A director must be a natural person aged 16 or over (or, where character-substrate applies, a substrate character with persistent identity and capacity).

(3) Directors are appointed and removed per the articles; statutory grounds for disqualification apply (Foxbridge Company Directors Disqualification Order).

### §7 Directors' duties

(1) **Duty to act within powers**: a director must act in accordance with the company's constitution and exercise powers only for proper purposes.

(2) **Duty to promote success of the company**: act in the way the director considers, in good faith, would be most likely to promote the success of the company for the benefit of members as a whole, having regard to:
  (a) likely consequences in the long term;
  (b) interests of employees;
  (c) relationships with suppliers, customers, and others;
  (d) impact on community and environment;
  (e) reputation for high standards of business conduct;
  (f) need to act fairly between members.

(3) **Duty to exercise independent judgment**.

(4) **Duty to exercise reasonable care, skill, and diligence**.

(5) **Duty to avoid conflicts of interest**.

(6) **Duty not to accept benefits from third parties**.

(7) **Duty to declare interests in proposed transactions**.

### §8 Members and meetings

(1) Decisions reserved to members include amendment of articles, change of name, capital reductions, voluntary winding up, removal of director.

(2) An **annual general meeting** must be held within 6 months of the financial year-end (public companies) or as required by articles (private companies; written-resolution alternative permitted).

(3) Quorum: minimum 2 members in person or by proxy unless articles specify otherwise.

## Part 4 — Accounts and audit

### §9 Accounts

(1) Every company must keep adequate accounting records and prepare annual accounts giving a **true and fair view**.

(2) Public companies must prepare consolidated accounts where they have subsidiaries.

### §10 Audit

(1) Public companies must have their accounts audited annually by a registered auditor.

(2) Private companies are audit-exempt below specified thresholds (turnover, balance sheet, employees) but must prepare and file accounts.

(3) Audit reports must state whether the accounts give a true and fair view and comply with the Foxbridge Accounting Standards Framework.

## Part 5 — Reorganisation, mergers, takeovers

### §11 Mergers and acquisitions

(1) Schemes of arrangement under court supervision are the principal mechanism for restructuring.

(2) **Public-company takeovers** are governed by the Foxbridge Takeover Code (mandatory bid threshold at 30%; pari-passu treatment of shareholders).

(3) Mergers raising competition concerns are referred to the Foxbridge Competition Commission.

### §12 Conversion between forms

A company may convert between private/public/CIC/mutual forms subject to procedural requirements and member approval.

## Part 6 — Football-specific corporate provisions

### §13 Fit-and-proper directors

Cross-reference: Foxbridge Football Act §20. The general fit-and-proper test of company law is supplemented by sport-specific disqualifications for owners and directors of licensed football clubs.

### §14 Heritage protections

Tier 1 and Tier 2 club articles must include heritage protections (kit, name, ground move) consistent with Foxbridge Football Act §17. Such articles are deemed entrenched: amendment requires supporters' trust formal consultation per the Football Act.

### §15 Mutual football clubs

A football-club mutual (suffix MFC) holds shares on trust for supporter-members. Distributions are capped; voting rights are one-member-one-vote regardless of stake.

## Part 7 — Insolvency and dissolution

### §16 Solvency

Cross-reference: Foxbridge Bankruptcy Act (`laws/commercial/bankruptcy-act.md`).

### §17 Strike-off

A company that has not traded for 12 months may apply to be struck from the register. Creditors may object.

## Part 8 — Citation, commencement, and extent

### §18 Short title, commencement, and extent

(1) This Act may be cited as the **Foxbridge Corporations Act**.

(2) This Act came into force on **2026-08-01** in-world.

(3) This Act extends to England-on-Polis only.

---

*Adapted from Companies Act 2006 (UK), OGL v3.0. Substrate-fictionalised by the staq, 2026. CC-BY-4.0 per `polis/LICENSE-CONTENT`.*
