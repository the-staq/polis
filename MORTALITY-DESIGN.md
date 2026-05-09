# Mortality layer doctrine — Polis V0.1.2

**Status.** Active V0.1.2. Schemas: `mortality.schema.json` v0.1.0 (new), `character.schema.json` v0.1.2, `world.schema.json` v0.1.1, `country.schema.json` v0.1.1.

**Why this exists.** Founder directive — *"characters need to have dependencies like food, health etc. is that wired in, and they can also die and different things can cause their death."* Until V0.1.2 the substrate had needs as a 10-dimension vector and an `is_alive` boolean, but no decay rates, no mortality model, no cause-of-death catalogue, no death-event record, no estate cascade. PRD §10.2-§10.3 specified the loop in prose; this document operationalises it.

**V0 stance.** Permissive severity (deaths are rare, mostly acute or long-arc chronic) + suicide engine-gated.

---

## Mental model

```
                ┌────────────────────────────────────────────────┐
                │ World-level needs_calibration (per dimension)  │
                │   decay_per_day · seek_threshold · damage_floor│
                │   days_at_floor_to_health_damage               │
                │   health_damage_per_day_below_floor            │
                └────────────────┬───────────────────────────────┘
                                 │ applied uniformly
                                 ▼
                ┌────────────────────────────────────────────────┐
                │       Character.state.needs (10 dims)          │
                │  hunger thirst energy health warmth comfort    │
                │  hygiene mood social purpose                   │
                └────────────┬─────────────────────┬─────────────┘
                             │                     │
                CharacterLifeWorkflow   MortalityTickWorkflow
                (decisions, shopping)   (weekly per character)
                             │                     │
                             ▼                     ▼
                ┌────────────────────────────────────────────────┐
                │  Character.state.vital_status                  │
                │   life_expectancy_age (sampled from country)   │
                │   biological_age_modifier (lifestyle)          │
                │   chronic_conditions[]                         │
                │   death_event (null while alive)               │
                └─────────────────────┬──────────────────────────┘
                                      │ on death
                                      ▼
                ┌────────────────────────────────────────────────┐
                │   CharacterDeathEvent saga                     │
                │   • populate state.vital_status.death_event    │
                │   • is_alive ← false; cycle_state ← deceased   │
                │   • terminate active contracts                 │
                │   • distribute estate per Property Act §5      │
                │   • vacate institution roles                   │
                │   • open succession paths                      │
                │   • notify relationships graph                 │
                │   • write public_record entries (obituary)     │
                └────────────────────────────────────────────────┘
```

---

## What changed (additive only)

### 1. New `polis/schemas/mortality.schema.json`

Defines four reusable structures via `$defs`:

| `$def` | Purpose |
|---|---|
| `death_cause` | Enumerated cause-of-death taxonomy (16 entries; engine refuses any cause not in enum) |
| `death_event` | The record written when a character dies — when, where, by whom, narrative, supporting evidence, estate-completion timestamp |
| `vital_status` | Lifetime mortality bookkeeping for a character — life expectancy, modifiers, chronic conditions, death_event slot |
| `needs_calibration` | World-level decay/threshold/floor parameters for all 10 needs dimensions |
| `actuarial_life_expectancy` | Country-level life-expectancy distribution by sex |

Plus two world-level controls:

| Control | Default | Effect |
|---|---|---|
| `v0_severity` | `permissive` | Deaths rare; mostly acute or long-arc chronic. `off` for CI; `realistic` for full PRD §10.2-§10.3 |
| `suicide_safeguarding_policy` | `engine_gated_v0` | Engine refuses `death_event.cause: suicide` without explicit `safeguarding_signoff_id` |

### 2. Death-cause catalogue

```yaml
- natural_age              # past life_expectancy_age; rolling probability
- illness_untreated        # health below floor for N weeks, no FNHS contact
- illness_terminal         # severity: terminal in chronic_conditions, expected date approaches
- acute_injury             # accident, single-event
- sport_injury_acute       # on-pitch / training (cross-ref football-act §10)
- violence_assault         # criminal-code §4-§5 outcome
- violence_war             # conflict.schema.json outcome
- suicide                  # ENGINE-GATED — see safeguarding policy below
- exposure                 # warmth floor + no shelter sustained
- malnutrition             # hunger/thirst floor sustained
- vehicle_accident
- workplace_accident
- doping_overdose          # cross-ref football-act §18-§19
- substance_overdose
- childbirth_complication
- unknown                  # forensic findings pending
```

Every catalogued cause has a defined invocation pathway (decay+rolling-probability for chronic; event-driven for acute). New causes require schema PR per OPEN-SOURCE.md Tier 2.

### 3. Character schema gets `state.vital_status`

```yaml
state:
  is_alive: true
  vital_status:
    life_expectancy_age: 84
    biological_age_modifier: -3      # athletic; lives longer
    chronic_conditions: []
    death_event: null                # populated atomically on death
```

When a character dies:
- `is_alive` flips false
- `cycle_state` becomes `deceased`
- `vital_status.death_event` is populated atomically (transactional)
- `CharacterLifeWorkflow` is terminated; no further LLM cycles
- `CharacterDeathEvent` saga fires to cascade consequences

### 4. World schema gets `mortality.needs_calibration`

Every world declares decay/seek-threshold/damage-floor for each of the 10 need dimensions, plus health-specific `mortality_threshold` and `weekly_mortality_probability_at_zero_health`. Modern Earth 2026 will use realistic-ish values; a fantasy world might declare longer life and slower decay.

### 5. Country schema gets `actuarial_life_expectancy`

England-on-Polis: mean 81.4 (female 83.1, male 79.7), stddev ~9.5. Used at character spawn to sample `life_expectancy_age`.

---

## How a character dies — the four paths

### Path 1 — Natural age (chronic)

After `vital_status.life_expectancy_age + biological_age_modifier`, `MortalityTickWorkflow` rolls a weekly probability of `natural_age` death that increases each year past the expectancy. Permissive at V0: probability ramps slowly.

### Path 2 — Untreated illness or sustained needs deprivation (chronic)

Sustained `health < mortality_threshold` triggers weekly rolls per `weekly_mortality_probability_at_zero_health`. Permissive at V0 — most characters seek FNHS treatment via `seek_threshold` long before this fires.

### Path 3 — Acute injury / accident / violence / sport injury (event-driven)

A workflow outside the mortality loop (e.g. `MatchSimulator`, `ConflictWorkflow`, `RoadAccidentWorkflow`, `AssaultWorkflow`) emits an `AcuteDeathEvent` with cause + supporting evidence. `MortalityTickWorkflow` does not roll for these; they're imposed by the upstream workflow.

### Path 4 — Suicide (gated)

The `suicide` cause is in the catalogue but the engine **refuses** to write `death_event.cause: suicide` unless `safeguarding_signoff_id` is non-null. There is no V0 workflow that produces a signoff. Result: at V0, no character can die by suicide via any LLM-generated narrative or any automated workflow. Authored end-of-life arcs requiring suicide as cause (e.g. a literary tragedy embedded in a story-mode world) will need a future V1+ Foxbridge-authority signoff workflow with documented safeguarding policy.

---

## Safeguarding policy

The substrate ships harm-reduction floors that override author intent and player will alike (constitutional Article XI):

1. **Suicide is engine-gated.** No LLM narrative can flip a character to `cause: suicide`. No auto-decide rule can. No player ping-response can. Only an authored workflow with explicit signoff can.

2. **Safeguarding signoff requires** (V1+ when the workflow ships):
   - the world's mortality.suicide_safeguarding_policy must be `narrowly_authorised_v1`
   - the founder must hold a "story-mode tragedy authorisation" record on the world
   - the in-world arc must have established narrative cause prior to death (no abrupt ends)
   - public_record must include resources for real-world player wellbeing (helpline, signposting)

3. **Even with signoff, content limits apply.** Method depiction is excluded from `death_event.narrative` per substrate content policy. Cause is recorded as `suicide`; method is not detailed.

4. **Real-world players come first.** If an in-world arc would distress a real-world player to the point of substrate concern, the engine has standing authority to refuse. This is non-overridable.

Players can configure their characters' `governance.standing_orders` to refuse high-distress arcs; the substrate honours this above any narrative pressure.

---

## Engine workflow contracts

| Workflow | Trigger | Action |
|---|---|---|
| `MortalityTickWorkflow` | weekly per character, in-world | Apply needs decay since last tick; advance chronic_conditions; roll natural_age / illness_untreated / illness_terminal probabilities; deterministic per (character_id, week_number, rng_seed) |
| `AcuteDeathEvent` (from upstream workflows) | event-driven | Caller provides cause + evidence; MortalityTickWorkflow does not arbitrate |
| `CharacterDeathEvent` saga | atomic, on any path | Populate death_event; flip is_alive; cycle_state ← deceased; terminate contracts; estate distribute; vacate institutions; notify relationships; write obituary |
| `EstateDistributionWorkflow` | step in saga | Per Foxbridge Property Act §5 (will / intestacy); delivers POL balance + property + institution shares to heirs |
| `ContractTerminationOnDeathWorkflow` | step in saga | Forfeit clauses, signing-on bonus pro-rata, image-rights residuals — all pulled from contract.schema.json `breach_remedies` |
| `InstitutionRoleVacateWorkflow` | step in saga | Sets `institution.staff.roles[].incumbent_character_id: null`, opens succession paths |

All workflows are deterministic given input state; replays are bit-identical.

---

## Worked exemplars in seeds

- `polis/seeds/modern-earth-2026/england-on-polis/football/characters/footballers/marsh-bennett.yaml` — alive: full vital_status with `is_alive: true`, life_expectancy 84, athletic modifier -3, no chronic conditions, death_event null.

- `polis/seeds/modern-earth-2026/england-on-polis/football/characters/memoriam/sandiland.yaml` — deceased: full populated death_event with `cause: sport_injury_acute`, dated 2018-10-13 at Riverpark (Eastfen), narrative, ruling institution (Foxbridge Coroner Eastfen District), supporting evidence URIs, estate distributed timestamp. Substrate-fictional. Demonstrates the populated state.

The Sandiland exemplar is referenced by:
- Marsh-Bennett (`relationships[]` includes mentor relationship)
- Federation rulebook (Sandiland Provisions on cardiac screening)
- Hartwell FC (Sandiland Stand at Brackensley Park; annual memorial fixture)

This is how substrate keeps the dead present without re-invoking their workflow.

---

## What is NOT changed by this layer

- `lot.schema.json`, `industry.schema.json`, `institution.schema.json`, `contract.schema.json`, `conflict.schema.json` — unchanged (they consume the death record but don't define it).
- `soft_skills.schema.json` — unchanged.
- Existing seed YAMLs continue to parse (vital_status is optional at character spawn; engine fills defaults from country.actuarial_life_expectancy if absent).
- Match simulator — unchanged. Adding sudden-cardiac-arrest probability to match events is a separate V1+ industry-level workflow.
- Engine hard floors (CSAM, real-world threats, sanctions) — unchanged. They sit ABOVE this mortality layer.

---

## V0 → V1+ trajectory

**V0** lands schemas, the catalogue, world+country actuarial parameters, two worked exemplars (alive + deceased). MortalityTickWorkflow is **specified but not yet implemented**; characters with `vital_status` are inert until the engine ships the workflow. This means: no V0 character will actually die from chronic mortality. Acute deaths (sport injury during a simulated match) are possible if a match-simulator workflow chooses to emit `AcuteDeathEvent`; the V0 deterministic match simulator does NOT emit them by default.

**V1+** adds:
- `MortalityTickWorkflow` engine implementation (deterministic, idempotent, replay-safe)
- `CharacterDeathEvent` saga with full cascade
- Estate distribution per Property Act §5
- Institution role-vacate
- Contract-termination-on-death
- Sandiland-Provisions style cardiac-screening sub-workflow at football-academy level
- Suicide-safeguarding workflow (only with explicit founder authorisation per world)
- Per-condition probability tables for `chronic_conditions`
- Lifestyle modifiers feeding `biological_age_modifier`

---

## License

CC-BY 4.0 per `polis/LICENSE-CONTENT`. Authored by the staq, 2026-05-09.
