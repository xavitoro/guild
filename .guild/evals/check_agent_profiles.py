#!/usr/bin/env python3
"""Fixture: proves the fourteen canonical Guild agent profiles exist, each
validates against the agent manifest schema, and no id is missing, extra,
or duplicated relative to the roster in GUILD_MASTER_SPEC.md section 3.

Usage:
    python3 .guild/evals/check_agent_profiles.py
Exit code is 0 when the roster matches exactly, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

GUILD_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = GUILD_ROOT / "agents"
SCHEMA_PATH = GUILD_ROOT / "schemas" / "agent-manifest.schema.json"

# Canonical roster: (id, alias) — from GUILD_MASTER_SPEC.md section 3.
CANONICAL_ROSTER = {
    "workflow-knowledge-orchestrator": "DM",
    "product-owner": "Paladin",
    "business-analyst": "Fighter",
    "product-experience-designer": "Druid",
    "ux-content-designer": "Bard",
    "web-experience-engineer": "Ranger",
    "product-software-engineer": "Artificer",
    "database-engineer": "Wizard",
    "integration-engineer": "Warlock",
    "quality-assurance-engineer": "Barbarian",
    "product-security-engineer": "Rogue",
    "cloud-devops-engineer": "Cleric",
    "product-data-analyst": "Sorcerer",
    "data-analytics-engineer": "Monk",
}


def main() -> int:
    errors: list[str] = []

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    found: dict[str, str] = {}
    for manifest_path in sorted(AGENTS_DIR.glob("*/manifest.yaml")):
        data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        rel = manifest_path.relative_to(GUILD_ROOT.parent)

        schema_errors = list(validator.iter_errors(data))
        if schema_errors:
            for e in schema_errors:
                errors.append(f"[invalid] {rel}: {e.message}")
            continue

        profile_id = data["id"]
        if profile_id in found:
            errors.append(
                f"[duplicate-id] {rel}: id '{profile_id}' already used by "
                f"{found[profile_id]}"
            )
            continue
        found[profile_id] = str(rel)

        if data["alias"] != CANONICAL_ROSTER.get(profile_id):
            errors.append(
                f"[alias-mismatch] {rel}: alias '{data['alias']}' does not match "
                f"expected '{CANONICAL_ROSTER.get(profile_id)}' for id '{profile_id}'"
            )

    missing = set(CANONICAL_ROSTER) - set(found)
    extra = set(found) - set(CANONICAL_ROSTER)
    for m in sorted(missing):
        errors.append(f"[missing-profile] '{m}' ({CANONICAL_ROSTER[m]}) has no manifest under .guild/agents/")
    for e in sorted(extra):
        errors.append(f"[unexpected-profile] '{e}' is not part of the canonical fourteen-profile roster")

    print(f"Agent profile check: {len(found)}/{len(CANONICAL_ROSTER)} canonical profiles found.")
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print(f"\nOK: all {len(CANONICAL_ROSTER)} profiles present, schema-valid, and unique.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
