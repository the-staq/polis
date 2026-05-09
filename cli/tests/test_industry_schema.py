#!/usr/bin/env python3
"""
Schema invariant tests for industry.schema.json.

Validates the v0.1.1 conditional fields (format-discriminator if/then) catch
bad configs at validation time — this is what locks the schema-as-substrate
guarantee. If a schema PR breaks these tests, the PR is wrong.

Engine-side invariants NOT expressible in pure JSON Schema (count-balance,
tier-graph linearity) are documented in industry.schema.json's
competition_hierarchy.description and tested via TODO: engine integration
tests once the engine ships.

Run:
    python3 polis/cli/tests/test_industry_schema.py

Exit 0 on all pass; nonzero on any failure.
"""
import copy
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("FAIL — pyyaml not installed (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema
except ImportError:
    print("FAIL — jsonschema not installed (pip install jsonschema)", file=sys.stderr)
    sys.exit(2)


REPO = Path(__file__).resolve().parents[2]
SCHEMA = json.load(open(REPO / "schemas" / "industry.schema.json"))
BASKETBALL = yaml.safe_load(open(REPO / "configs" / "industries" / "basketball" / "industry.yaml"))


def expect_valid(config: dict, label: str) -> bool:
    try:
        jsonschema.validate(config, SCHEMA)
        print(f"  ✓ {label}")
        return True
    except jsonschema.ValidationError as e:
        print(f"  ✗ {label} — {e.message[:120]}")
        return False


def expect_invalid(config: dict, label: str, must_match_substring: str = "") -> bool:
    try:
        jsonschema.validate(config, SCHEMA)
        print(f"  ✗ {label} — schema accepted bad config")
        return False
    except jsonschema.ValidationError as e:
        if must_match_substring and must_match_substring not in e.message:
            print(f"  ✗ {label} — caught wrong error: '{e.message[:80]}'")
            return False
        print(f"  ✓ {label}")
        return True


def main():
    failures = 0

    print("Positive tests — known-good configs validate")
    if not expect_valid(BASKETBALL, "basketball industry.yaml v0.1 validates"):
        failures += 1

    # league_with_playoff with promoted_via_playoff present
    good = copy.deepcopy(BASKETBALL)
    good["competition_hierarchy"]["tiers"][1]["format"] = "league_with_playoff"
    good["competition_hierarchy"]["tiers"][1]["promotion_relegation"]["promoted_via_playoff"] = 1
    if not expect_valid(good, "league_with_playoff with promoted_via_playoff"):
        failures += 1

    # swiss_system with rounds present
    good = copy.deepcopy(BASKETBALL)
    good["competition_hierarchy"]["tiers"][0]["format"] = "swiss_system"
    good["competition_hierarchy"]["tiers"][0]["rounds"] = 9
    if not expect_valid(good, "swiss_system with rounds"):
        failures += 1

    # group_then_knockout with both fields
    good = copy.deepcopy(BASKETBALL)
    good["competition_hierarchy"]["tiers"][0]["format"] = "group_then_knockout"
    good["competition_hierarchy"]["tiers"][0]["groups_count"] = 4
    good["competition_hierarchy"]["tiers"][0]["qualifiers_per_group"] = 2
    if not expect_valid(good, "group_then_knockout with groups_count + qualifiers_per_group"):
        failures += 1

    print()
    print("Negative tests — bad configs rejected")

    # league_with_playoff missing promoted_via_playoff
    bad = copy.deepcopy(BASKETBALL)
    bad["competition_hierarchy"]["tiers"][1]["format"] = "league_with_playoff"
    bad["competition_hierarchy"]["tiers"][1]["promotion_relegation"].pop("promoted_via_playoff", None)
    if not expect_invalid(bad, "league_with_playoff without promoted_via_playoff", "promoted_via_playoff"):
        failures += 1

    # swiss_system missing rounds
    bad = copy.deepcopy(BASKETBALL)
    bad["competition_hierarchy"]["tiers"][0]["format"] = "swiss_system"
    bad["competition_hierarchy"]["tiers"][0].pop("rounds", None)
    if not expect_invalid(bad, "swiss_system without rounds", "rounds"):
        failures += 1

    # group_then_knockout missing fields
    bad = copy.deepcopy(BASKETBALL)
    bad["competition_hierarchy"]["tiers"][0]["format"] = "group_then_knockout"
    bad["competition_hierarchy"]["tiers"][0].pop("groups_count", None)
    bad["competition_hierarchy"]["tiers"][0].pop("qualifiers_per_group", None)
    if not expect_invalid(bad, "group_then_knockout without groups_count / qualifiers_per_group", "groups_count"):
        failures += 1

    # missing tier_rank (now required at v0.1.1)
    bad = copy.deepcopy(BASKETBALL)
    bad["competition_hierarchy"]["tiers"][0].pop("tier_rank", None)
    if not expect_invalid(bad, "tier without tier_rank field", "tier_rank"):
        failures += 1

    # promoted_count without promoted_to (allowed shape — soft warning,
    # engine catches at config-load); this should still validate JSON-Schema-wise
    # Confirms we're not over-tightening.

    print()
    if failures == 0:
        print(f"All schema invariant tests passed.")
        return 0
    else:
        print(f"FAIL — {failures} test(s) failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
