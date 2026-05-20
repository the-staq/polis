# Football governance corpus

The rule books, regulations, and statutes that the football industry runs under.
Consumed by the substrate's `PlausibilityJudge`, `ConflictWorkflow`, press recap
LLM, and (V0.5+) sim refereeing handlers via the retrieval index per
V0-PLAN §3.10.

Loader: `markdown-tree` (per `polis/configs/industries/football-modern-earth/industry.yaml`
→ `cognition.corpora.governance.loader`). Implementation:
`polis-internal/app/retrieval/ingestion/football/governance_loader.py`.

## Sources to acquire (operator-provided)

V0 alpha posture — fair-use research per V0-PLAN R13. Re-review at V1 commercialization.

| Source | License | Notes |
|---|---|---|
| **IFAB Laws of the Game** | CC-BY-4.0 | The Laws of football. Available at [theifab.com/laws](https://www.theifab.com/laws/). PDF only on the official site; community markdown conversions exist on GitHub. |
| **FIFA Regulations on the Status and Transfer of Players (RSTP)** | Publicly available | Governs transfers, contracts, eligibility. PDF on fifa.com. |
| **FA Rules and Regulations** | Publicly available | English football's national regulator. thefa.com → handbook. |
| **EFL Regulations** | Publicly available | English Football League (Championship + below). |
| **Premier League Handbook** | Publicly available | Premier League-specific rules (PSR / squad sizes / etc.). |

Operator obtains markdown versions (or converts from PDF), drops one source per
subdirectory under `sources/`:

```
cognition/governance/
├── README.md                                ← this file
├── sources/
│   ├── ifab-laws/                           ← IFAB Laws of the Game
│   │   ├── 01-the-field-of-play.md
│   │   ├── 02-the-ball.md
│   │   ├── ...
│   │   └── 17-the-corner-kick.md
│   ├── fifa-rstp/                           ← FIFA RSTP
│   │   └── ...
│   └── fa-rules/                            ← FA Rules
│       └── ...
└── chunks.yaml                              ← computed output (committed)
```

## Generating `chunks.yaml`

From `polis-internal/app/`:

```bash
uv run python -m app.retrieval.ingestion.football.governance_loader \
    --corpus-root ../../polis/configs/industries/football-modern-earth/cognition/governance/sources/ifab-laws \
    --output     ../../polis/configs/industries/football-modern-earth/cognition/governance/chunks-ifab-laws.yaml \
    --source-id  ifab-laws-of-the-game \
    --source-url https://www.theifab.com/laws/latest/ \
    --source-license CC-BY-4.0
```

Repeat per source (`--source-id fifa-rstp`, `--source-id fa-rules`, etc.). Each
source produces its own `chunks-<id>.yaml`. The V0.5+ retrieval index ingests
each chunks file into pgvector with `voyage-3` embeddings (per
`industry.yaml → cognition.embedding_model`).

The CLI prints the `polis/configs/sources.yaml` entry after each run — paste
into the provenance audit trail.

## What each chunk looks like

```yaml
chunks:
  - chunk_id: ifab-laws-of-the-game-law-12-fouls-and-misconduct-section-1-direct-free-kick-offences
    source_id: ifab-laws-of-the-game
    source_file: ifab-laws/12-fouls-and-misconduct.md
    section_path:
      - "Law 12 — Fouls and Misconduct"
      - "Section 1 — Direct Free Kick Offences"
    word_count: 412
    metadata:
      section_depth: 2
    text: |
      A direct free kick is awarded if a player commits any of the following
      offences against an opponent in a manner considered by the referee to
      be careless, reckless or using excessive force:
      ...
```

Citations from `PlausibilityJudge` / `ConflictWorkflow` / press recap reference
`chunk_id` + `section_path` so readers can trace any cited rule back to its
exact location in the source.

## Pending

- **First markdown corpus drop** — operator clones IFAB Laws (or community
  markdown), runs the loader, commits `chunks-ifab-laws.yaml` to this dir.
- **V0.5+ pgvector embedding** — retrieval-index reads each chunks file,
  embeds via `voyage-3`, writes to pgvector with `source_id` namespace.
- **Sources.yaml entries** — one per source acquired. CLI prints them.
- **Per-clause cross-references** — IFAB Laws often references "as defined in
  Law X" between sections. V0.5+ enhancement: extract these as edges between
  chunks for graph-aware retrieval.
