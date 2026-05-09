# Skills layer doctrine — Polis V0.1.2

**Status.** Active V0.1.2. Schemas: `industry.schema.json` v0.1.2, `character.schema.json` v0.1.1, `soft_skills.schema.json` v0.1.0 (new).

**Why this exists.** Founder directive — *"inside each industry, every job needs skills that must be learned and improved on; that's how characters are ranked alongside general character soft skills."* This document operationalises that directive.

---

## Mental model

```
                              ┌─────────────────────────────┐
                              │     Character (any role)    │
                              └─────────────────────────────┘
                                            │
                ┌───────────────────────────┴────────────────────────────┐
                │                                                        │
        ┌───────▼────────────┐                              ┌────────────▼──────────┐
        │   Hard skills      │                              │   Soft skills (9)     │
        │ (per profession)   │                              │   universal           │
        │                    │                              │                       │
        │  pace 64           │                              │  composure 84         │
        │  passing 71        │                              │  charisma 58          │
        │  shooting 51       │   industry config            │  resilience 80        │
        │  stamina 78        │   defines weights →          │  integrity 88         │
        │  positioning 88    │                              │  decisiveness 72      │
        │  leadership 86     │                              │  empathy 75           │
        │                    │                              │  ambition 65          │
        │  EVOLVE WEEKLY     │                              │  ego 38               │
        │  via growth_curve  │                              │  work_ethic 87        │
        │  + training        │                              │                       │
        │  + match-minutes   │                              │  EVOLVE SLOWLY        │
        │                    │                              │  via life events      │
        └─────────┬──────────┘                              └──────────┬────────────┘
                  │                                                    │
                  │   industry.professions[].overall_rating_formula    │
                  │   (e.g. 0.70 hard + 0.30 soft for footballer)      │
                  └──────────────────┬─────────────────────────────────┘
                                     │
                                     ▼
                           overall_rating ∈ [0, 100]
                          ─────────────────────────
                       used by: scouting, contract pricing,
                       dressing-room hierarchy, labour market,
                       cross-profession comparisons
```

---

## What changed (additive only — no breaking changes)

### 1. Hard skills now declare a `growth_curve`

Each entry in `industry.professions[].base_skills[]` may declare a curve:

```yaml
- id: pace
  label: Pace
  scale: 0_to_100
  growth_curve:
    base_value_at_starting_age: 55     # academy default
    peak_age: 25                       # late-20s peak
    peak_value_max: 95                 # ceiling with elite training
    decay_after_peak_per_year: 2.5     # falls fast post-peak
    learning_rate_per_year_active: 3.5 # grows ~3.5/year when trained
    coachable: true                    # vs innate (height, frame)
```

The engine's `SkillTickWorkflow` runs once per in-world week per character, deterministically nudging each skill toward its (age, training-load, match-minutes) target. Replays are bit-identical because the tick uses `(character_id, skill_id, week_number, rng_seed)` as the state hash.

### 2. New canonical 9-attribute soft-skill taxonomy

Defined by the new `polis/schemas/soft_skills.schema.json`:

| Attribute | What it modulates |
|-----------|-------------------|
| **composure** | Performance under pressure (penalty in the 89th, hostile press conference) |
| **charisma** | Influence on others (dressing-room presence, broadcasting performance) |
| **resilience** | Bounce-back from setbacks (post-injury, post-relegation, post-scandal) |
| **integrity** | Honesty / consistency (contract-honouring, bribery-resistance, media truthfulness) |
| **decisiveness** | Speed under uncertainty (ping-resolution rate, mid-match adjustments) |
| **empathy** | Sensitivity to others' states (dressing-room conflict, mentor effectiveness) |
| **ambition** | Drive to advance (stretch-application willingness, retirement timing) |
| **ego** | Self-regard (squad-rotation acceptance, response to criticism) |
| **work_ethic** | Daily effort (multiplier on hard-skill `learning_rate`) |

Every character has these. They evolve slowly (~0.5–1.5 / in-world year) and only via life events — not weekly drills.

### 3. Each profession composes the two layers

```yaml
professions:
  - id: player
    soft_skill_weights:
      composure: 0.20
      resilience: 0.15
      work_ethic: 0.20
      decisiveness: 0.10
      ambition: 0.10
      integrity: 0.10
      empathy: 0.05
      charisma: 0.05
      ego: 0.05
    overall_rating_formula:
      hard_skills_weight: 0.70   # footballer is mostly skill
      soft_skills_weight: 0.30
      hard_skill_weights:
        leadership: 1.5          # captain bonus
```

Profession-specific weighting matters: composure is huge for goal-scorers, less for scouts; charisma is vital for broadcasters, near-zero for engineers; ego subtracts (weighted 0) for managers and broadcasters.

---

## Engine integration

| Workflow | Trigger | Action |
|---|---|---|
| `SkillTickWorkflow` | weekly per character | Apply `growth_curve` to each hard skill: nudge toward (age, training_load, match_minutes) target. Update `skills_metadata.last_tick_in_world`, `current_overall_rating`. Deterministic. |
| `SoftSkillEventWorkflow` | on life event (won title, contract dispute resolved, relegation, scandal, mentor relationship maturing) | Apply small soft-skill nudges (typically ±1–3 points). Logged with cause for replay. |
| `OverallRatingWorkflow` | after `SkillTickWorkflow` | Recompute `current_overall_rating` per `overall_rating_formula`. Cached. |
| Labour-market workflows | on transfer-window open | Use `current_overall_rating` for default offer pricing per `salary_distribution`. |
| `ContractWorkflow` | on contract renewal | Offer-band scaled to `current_overall_rating`. |

---

## Composability — same model, multiple industries

The football industry uses skills `pace, passing, shooting, stamina, positioning, leadership`. Basketball uses `shooting, rebounding, playmaking, defense, athleticism, bball_iq`. Banking would use `risk_judgment, capital_markets, client_management, trading_intuition`. The schema is identical; only the population of skills + curves differs per industry.

Soft skills are universal: a footballer who retires and becomes a manager (or a banker → broadcaster) carries soft skills forward unchanged. Hard skills reset to the new profession's `base_skills`. This is the substrate move that makes cross-career arcs coherent.

---

## What is NOT changed by this layer

- `lot.schema.json`, `world.schema.json`, `country.schema.json`, `institution.schema.json`, `contract.schema.json`, `conflict.schema.json` — unchanged.
- Existing seed YAMLs continue to parse (skills/skills_metadata/soft_skills are optional; engine fills defaults for npc characters).
- Match simulator — still deterministic; uses *current* skill values at kickoff, never re-derives them.
- Engine hard floors (CSAM, real-world threats, sanctions) — unchanged. Soft-skill `integrity` governs only legal-but-shady behaviours; the engine refuses Article XI violations regardless of any character's integrity score.

---

## V0 vs V1+ trajectory

**V0** lands the schema, the football + basketball industry curves, and Marsh-Bennett as the worked exemplar character. Other 20 footballers + 1 manager + 3 officers will pick up engine-default values from `growth_curve.base_value_at_starting_age` until backfilled (a 30-min editing pass per character).

**V1+** adds:
- `SkillTickWorkflow` engine implementation (deterministic, idempotent, replay-safe)
- `SoftSkillEventWorkflow` with documented life-event triggers
- Training-load adjustments via `institution.operations.training-quality`
- Mentor-bonus mechanic (high-empathy mentor + young mentee → +0.5 / year on mentee growth)
- Cross-profession ranking surface in the Found / Manage UI

---

## License

CC-BY 4.0 per `polis/LICENSE-CONTENT`. Authored by the staq, 2026-05-09.
