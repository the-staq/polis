#!/usr/bin/env python3
"""
Basketball match v1 — deterministic stub simulator.

Tests V0-PLAN substrate invariant: same rng_seed + same lineup state ALWAYS
produces same outcome. Replayable from disk; CI runs this and compares stdout
against a golden file (golden.txt, generated on first run, then frozen).

Real V0/V1 simulator will replace this — fork from open-source xG-shaped
basketball simulators or build minimal stat-based engine. For round-trip
fixture purposes, we just need:
  1. Read both team rosters from institutions/ (5 starters each)
  2. Compute deterministic outcome from rng_seed + skills
  3. Output stable result

Run:
    python simulator.py
    python simulator.py --explain   # show per-quarter scoring trace

CI:
    python simulator.py > /tmp/out.txt
    diff /tmp/out.txt golden.txt    # must be empty
"""

import hashlib
import sys
from pathlib import Path

# Avoid YAML dependency in CI by parsing minimal subset by hand.
# The fixtures use simple key: value YAML; no nested constructs we can't grep.

FIXTURE_ROOT = Path(__file__).parent.parent

# ─── Roster (hardcoded references to character files for fixture clarity) ───
TITANS = [
    {"id": "c_b001", "name": "Marcus Hollencourt",   "shoot": 78, "reb": 41, "play": 88, "def": 79, "ath": 74, "iq": 86},
    {"id": "c_b002", "name": "Eli Quartermaine",     "shoot": 91, "reb": 38, "play": 64, "def": 62, "ath": 70, "iq": 74},
    {"id": "c_b003", "name": "Olabode Ifowodo",      "shoot": 71, "reb": 64, "play": 58, "def": 88, "ath": 84, "iq": 79},
    {"id": "c_b004", "name": "Henrik Halverstone",   "shoot": 68, "reb": 79, "play": 71, "def": 78, "ath": 60, "iq": 91},
    {"id": "c_b005", "name": "Sasha Petrescu",       "shoot": 54, "reb": 86, "play": 42, "def": 73, "ath": 90, "iq": 64},
]

FISHERS = [
    {"id": "c_b006", "name": "Tomi Adekunle",        "shoot": 71, "reb": 44, "play": 80, "def": 74, "ath": 60, "iq": 88},
    {"id": "c_b007", "name": "Sigrid Ostmark",       "shoot": 87, "reb": 38, "play": 56, "def": 60, "ath": 72, "iq": 71},
    {"id": "c_b008", "name": "Dario Markulin",       "shoot": 58, "reb": 64, "play": 51, "def": 89, "ath": 78, "iq": 76},
    {"id": "c_b009", "name": "Aoife Brennan",        "shoot": 60, "reb": 79, "play": 48, "def": 71, "ath": 86, "iq": 58},
    {"id": "c_b010", "name": "Nathaniel Kostoff",    "shoot": 51, "reb": 84, "play": 44, "def": 79, "ath": 64, "iq": 81},
]

RNG_SEED = "0x4f9c2a7e91d3b58f"


def deterministic_rng(seed: str, salt: str) -> float:
    """Deterministic float in [0, 1) from (seed, salt) — replayable across runs."""
    h = hashlib.sha256(f"{seed}::{salt}".encode()).hexdigest()
    return int(h[:16], 16) / (1 << 64)


def team_rating(roster: list, dimension: str) -> float:
    """Aggregate roster rating in a dimension (mean of starters)."""
    return sum(p[dimension] for p in roster) / len(roster)


def simulate_quarter(home_roster: list, away_roster: list, quarter: int) -> tuple[int, int]:
    """One quarter of basketball. Returns (home_pts, away_pts).

    Deterministic: rng_seed + quarter index → same numbers every call.
    """
    home_off = (team_rating(home_roster, "shoot") + team_rating(home_roster, "play")) / 2
    home_def = team_rating(home_roster, "def")
    away_off = (team_rating(away_roster, "shoot") + team_rating(away_roster, "play")) / 2
    away_def = team_rating(away_roster, "def")

    # Possessions per quarter ~25, points per possession ~1.0 baseline
    home_eff = (home_off - away_def) / 100.0           # offensive minus defensive opponent
    away_eff = (away_off - home_def) / 100.0
    home_var = (deterministic_rng(RNG_SEED, f"home-q{quarter}") - 0.5) * 6
    away_var = (deterministic_rng(RNG_SEED, f"away-q{quarter}") - 0.5) * 6

    home_pts = round(20 + home_eff * 12 + home_var)
    away_pts = round(20 + away_eff * 12 + away_var)
    return max(home_pts, 12), max(away_pts, 12)    # floor at 12; no quarter is shut out


def simulate(explain: bool = False) -> dict:
    home_total, away_total = 0, 0
    quarters = []
    for q in range(1, 5):
        h, a = simulate_quarter(TITANS, FISHERS, q)
        home_total += h
        away_total += a
        quarters.append((q, h, a))

    return {
        "home": {"name": "Foxbridge Titans", "id": "foxbridge-titans", "score": home_total},
        "away": {"name": "Ravensby Fishers", "id": "ravensby-fishers", "score": away_total},
        "quarters": quarters,
        "rng_seed": RNG_SEED,
    }


def render(result: dict, explain: bool):
    print(f"Hartshire Basketball Combination · Week 1 · {result['rng_seed']}")
    print("─" * 72)
    print(f"  {result['home']['name']:24s}  {result['home']['score']:3d}")
    print(f"  {result['away']['name']:24s}  {result['away']['score']:3d}")
    print("─" * 72)
    if explain:
        print("Quarter scoring:")
        for q, h, a in result["quarters"]:
            print(f"  Q{q}: {h:3d} - {a:3d}")
        print()
    winner = result["home"] if result["home"]["score"] > result["away"]["score"] else result["away"]
    print(f"  Winner: {winner['name']} ({winner['id']})")


if __name__ == "__main__":
    explain = "--explain" in sys.argv
    result = simulate(explain=explain)
    render(result, explain)
