#!/usr/bin/env python3
"""Fixture: proves the human-facing surfaces actually name profiles by their
alias (GUILD_MASTER_SPEC.md section 3.1 / definition-of-done item 11), rather
than leaving the roster as decoration in the spec.

Checks:
  1. .guild/core/policies/default-policies.yaml declares the alias-first
     principle and human_interaction.address_profiles_by: alias.
  2. Every agent's AGENT.md carries a "Speaking to the human" section that
     names that profile's own alias.
  3. Every workflow.md step-table row names the responsible profile by alias
     (or "Human" for a `responsible_profile: human` step), and every Mermaid
     node label is prefixed with that alias.
  4. Every skill's core SKILL.md renders its applicable profiles by alias.
  5. The grant-human-approval skill requires the request to identify profiles
     by alias.

The complementary invariant — that aliases never leak into machine fields —
is checked too: no workflow step's responsible_profile, and no skill's
applicable_profiles entry, may be an alias.

Usage:
    python3 .guild/core/evals/check_alias_presence.py
Exit code is 0 when every human-facing surface is attributed, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

GUILD_ROOT = Path(__file__).resolve().parents[2]  # .guild/
REPO_ROOT = GUILD_ROOT.parent
CORE_ROOT = GUILD_ROOT / "core"
HUMAN = "human"


def load_all(glob_pattern: str) -> dict[str, dict]:
    out = {}
    for path in sorted(CORE_ROOT.glob(glob_pattern)):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        out[data["id"]] = data
    return out


def main() -> int:
    errors: list[str] = []

    agents = load_all("agents/*/manifest.yaml")
    skills = load_all("skills/*/SKILL.yaml")
    workflows = load_all("workflows/*/workflow.yaml")
    roster = {agent_id: agent["alias"] for agent_id, agent in agents.items()}
    aliases = set(roster.values())

    def alias_of(profile_id: str) -> str:
        return "Human" if profile_id == HUMAN else roster[profile_id]

    # 1. policy declaration
    policies = yaml.safe_load((CORE_ROOT / "policies" / "default-policies.yaml").read_text(encoding="utf-8"))
    if "human_facing_messages_identify_the_profile_by_alias" not in policies["principles"]:
        errors.append("[policy] default-policies.yaml does not declare the alias-first principle")
    if policies.get("human_interaction", {}).get("address_profiles_by") != "alias":
        errors.append("[policy] default-policies.yaml human_interaction.address_profiles_by is not 'alias'")

    # 2. AGENT.md self-introduction
    for agent_id, agent in agents.items():
        path = CORE_ROOT / "agents" / agent_id / "AGENT.md"
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(REPO_ROOT)
        if "## Speaking to the human" not in text:
            errors.append(f"[no-speaking-section] {rel}: no 'Speaking to the human' section")
        elif agent["alias"] not in text.split("## Speaking to the human", 1)[1].split("\n## ", 1)[0]:
            errors.append(f"[unattributed] {rel}: its 'Speaking to the human' section never names '{agent['alias']}'")

    # 3. workflow.md rows and diagram labels
    for workflow_id, workflow in workflows.items():
        path = CORE_ROOT / "workflows" / workflow_id / "workflow.md"
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(REPO_ROOT)
        for step in workflow["steps"]:
            profile = step["responsible_profile"]
            if profile != HUMAN and profile not in roster:
                continue  # check_workflow_refs.py owns unresolvable profiles
            alias = alias_of(profile)
            row = re.search(rf"^\| `{re.escape(step['id'])}` \|(.*)\|$", text, flags=re.M)
            if not row:
                errors.append(f"[missing-row] {rel}: step '{step['id']}' has no step-table row")
            elif alias not in row.group(1):
                errors.append(f"[unattributed-row] {rel}: step '{step['id']}' does not name '{alias}'")
            node = re.search(rf'^    {re.escape(step["id"])}(?:\[|\{{\{{)"([^"]*)"', text, flags=re.M)
            if not node:
                errors.append(f"[missing-node] {rel}: step '{step['id']}' has no diagram node")
            elif not node.group(1).startswith(f"{alias} — "):
                errors.append(f"[unattributed-node] {rel}: node '{step['id']}' is not labeled '{alias} — ...'")

    # 4. core SKILL.md applicable profiles
    for skill_id, skill in skills.items():
        path = CORE_ROOT / "skills" / skill_id / "SKILL.md"
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(REPO_ROOT)
        section = re.search(r"## Applicable profiles\n\n(.+)\n", text)
        if not section:
            errors.append(f"[no-profiles-section] {rel}: no 'Applicable profiles' section")
            continue
        for profile in skill["applicable_profiles"]:
            expected = "the human" if profile == HUMAN else f"{roster.get(profile, profile)} ({profile})"
            if expected not in section.group(1):
                errors.append(f"[unattributed-skill] {rel}: expected '{expected}' in its applicable profiles")

    # 5. the approval skill itself demands attribution
    approval = skills.get("grant-human-approval")
    if approval and not any("alias" in item for item in approval["inputs"] + approval["steps"]):
        errors.append("[approval-unattributed] grant-human-approval never requires the request to name a profile by alias")

    # complementary: aliases stay out of machine fields
    for workflow_id, workflow in workflows.items():
        for step in workflow["steps"]:
            if step["responsible_profile"] in aliases:
                errors.append(
                    f"[alias-in-field] workflows/{workflow_id}: step '{step['id']}' uses alias "
                    f"'{step['responsible_profile']}' as responsible_profile instead of a canonical id")
    for skill_id, skill in skills.items():
        for profile in skill["applicable_profiles"]:
            if profile in aliases:
                errors.append(
                    f"[alias-in-field] skills/{skill_id}: applicable_profiles contains alias '{profile}'")

    step_count = sum(len(w["steps"]) for w in workflows.values())
    print(f"Alias presence check: {len(agents)} profiles, {len(skills)} skills, "
          f"{len(workflows)} workflows ({step_count} steps).")
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("\nOK: every human-facing surface names its profile by alias, and no artifact field stores one.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
