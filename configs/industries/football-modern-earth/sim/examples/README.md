# Football examples — few-shot calibration vocabulary

This directory is the **calibration source** for the football match sim. Per
`DECISION-CALIBRATION-SOURCE.md`: sim handlers query an LLM-as-environment
with these examples as few-shot anchors. The LLM extrapolates from its
pretrained world knowledge, calibrated by these examples to football's
specific tone, era, and style.

## What goes here

One subdirectory per event type. One YAML file per example.

```
examples/
├── README.md           ← this file
├── shot/               ← 10+ canonical shot examples
├── foul/               ← 10+ canonical foul examples
├── card/               ← yellow + red card examples
├── goal/               ← celebration + tactical context for goals
├── dribble/            ← deceptive moves (legover, Cruyff turn, etc.)
├── pass/               ← pass types (through-ball, cross, switch, lofted)
├── save/               ← goalkeeper actions
└── set_piece/          ← corners, free-kicks, throw-ins, penalties
```

Numbering convention: `01-descriptive-slug.yaml`, `02-another-slug.yaml`. Two
digits + hyphen-separated slug. Numbers are stable ordering hints (used when
the substrate picks "first N examples" for prompt budget reasons).

## What makes a good example

Quality > quantity. Ten well-curated examples beat a thousand mediocre ones.
For each event type, aim for canonical examples that span:

- **Range of difficulty** — novice / intermediate / expert / virtuoso
- **Range of context** — when does this happen? Open play, set piece, counter,
  late-game desperation, opening-15-minute energy?
- **Range of outcomes** — what typically happens after? Defender beaten? Ball
  recovered? Foul drawn? Goal? Miss?
- **Era + region awareness** — a 1970s Cruyff turn looks different from a 2020s
  Mbappé chop; both belong, tagged with era metadata

Anti-examples:
- Don't author "average" or "typical" events — those are statistical means and
  not what few-shot anchors are for
- Don't pile on rare-but-cool events (no example file should be "the bicycle
  kick someone scored once in 1987"); each example should describe a
  recognizable pattern, not a one-off incident
- Don't author examples that duplicate existing ones in shape — examples
  should expand the vocabulary, not echo it

## Example file shape

See `shot/01-close-range-tap-in.yaml` for a worked example. Required fields:

- `id` — stable kebab-case slug, unique within event type
- `name` — human-readable (1 line)
- `category` — sub-type within the event type (e.g., "close-range-finish",
  "speculative-shot", "tactical-foul")
- `difficulty` — `novice` | `intermediate` | `expert` | `virtuoso`
- `historical_origin` — when + where this pattern emerged (1–3 sentences)
- `prerequisites` — what character skills enable this (skill name + minimum)
- `context_examples` — 2–4 short descriptions of match situations where this
  appears
- `mechanics` — 2–4 lines describing the physical / tactical execution
- `typical_outcomes` — list of outcome + likelihood pairs
- `narrative_examples` — 2–3 rich prose passages showing what this looks like
  in commentary / journalism style
- `metadata.contributed_by` — your GitHub handle
- `metadata.license` — `CC-BY-4.0` (the open repo's content license)
- `metadata.era` — `"1960-present"` | `"2010-present"` | etc. — used to filter
  examples by era when running historical-era sims
- `metadata.region` — geographic origin (when meaningful)

## Authoring workflow

1. Pick an event type with thin coverage (look at the per-directory count)
2. Brainstorm 1–3 canonical patterns NOT already represented
3. Author one YAML per pattern; follow the shape above
4. PR: `examples(football): add {pattern-name} to {event_type} vocabulary`
5. Reviewers (substrate maintainers + football-shepherds) check:
   - Does this expand the vocabulary or duplicate it?
   - Is the narrative honest (no propaganda / no real-player slander)?
   - Are prerequisites realistic?
   - Is the typical_outcomes list complete enough to inform the LLM?
6. Merge → LLM picks up next sim run; no engine changes, no schema migrations

## How examples reach the LLM

At sim bootstrap, the football handler (`../handlers.py`):

1. Walks this directory tree, loading all YAMLs
2. Builds an in-memory index keyed by event type + (later) era + region tags
3. For each LLM-driven decision point (shot_attempt, foul, dribble), the
   handler:
   - Filters examples by event type
   - Optionally filters further by current match state (e.g., "minute >= 75 +
     trailing by 1 goal" might prefer desperation-pattern examples)
   - Selects up to N examples (prompt budget; default 5)
   - Formats as a few-shot prompt block
   - Passes to `sim.llm_hook.decide_with_examples(...)` (substrate hook
     signature)
4. The LLM hook returns an action + a brief narrative reason
5. Handler emits the resulting Event into the sim log

For CI / deterministic test runs, the StubLLMHook ignores examples and uses
the Poisson rates from `../derived_distributions.yaml` instead. Production
runs (V0.5+, polis-internal) wire a real LLM.

## Adding a new event type

When the existing event types don't cover what you want to model (e.g., you
want to add `nutmeg/` as a dribble sub-vocabulary), the path is:

1. Create the subdirectory: `mkdir nutmeg/`
2. Author 3–5 starter examples
3. Optionally update `../rules.yaml` if the kernel needs to know about the
   new event type for decision-point dispatch (most often it doesn't — sub-
   types live inside `dribble/` and the LLM picks the right one)
4. PR: `examples(football): add nutmeg event sub-type to dribble vocabulary`

## License

All examples in this directory are CC-BY-4.0 (the polis open repo's content
license per `LICENSE-CONTENT`). Contributing means agreeing to that license.
Attribution flows: every example's `metadata.contributed_by` is preserved in
the open repo's git history.
