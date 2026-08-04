#!/usr/bin/env python3
"""Fixture: validates the semantic references between workflows, profiles, skills
and run records that plain JSON Schema validation cannot express:

  - Every workflow step's responsible_profile is either 'human' or a real
    agent profile id under .guild/agents/.
  - Every workflow step's invoked_skill is a real skill id under
    .guild/skills/.
  - Every skill's applicable_profiles are either 'human' or real agent
    profile ids.
  - Every run record's workflow_id is a real workflow id, and every one of
    its steps' step_id belongs to that specific workflow.

Usage:
    python3 .guild/evals/check_workflow_refs.py
Exit code is 0 when every reference resolves, 1 otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

GUILD_ROOT = Path(__file__).resolve().parents[1]
HUMAN = "human"


def load_all(glob_pattern: str) -> dict[str, dict]:
    """Loads YAML files matching glob_pattern, keyed by their declared id."""
    out = {}
    for path in sorted(GUILD_ROOT.glob(glob_pattern)):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        out[data["id"]] = data
    return out


def main() -> int:
    errors: list[str] = []

    agents = load_all("agents/*/manifest.yaml")
    skills = load_all("skills/*/SKILL.yaml")
    workflows = load_all("workflows/*/workflow.yaml")
    runs = load_all("runs/*.yaml")

    valid_profiles = set(agents) | {HUMAN}
    valid_skills = set(skills)

    for skill_id, skill in skills.items():
        for profile in skill["applicable_profiles"]:
            if profile not in valid_profiles:
                errors.append(
                    f"[skill-bad-profile] skill '{skill_id}' lists applicable_profiles "
                    f"'{profile}', which is not '{HUMAN}' or a known agent profile id"
                )

    for wf_id, wf in workflows.items():
        step_ids = set()
        for step in wf["steps"]:
            step_ids.add(step["id"])
            profile = step["responsible_profile"]
            skill_id = step["invoked_skill"]
            if profile not in valid_profiles:
                errors.append(
                    f"[workflow-bad-profile] {wf_id}/{step['id']}: responsible_profile "
                    f"'{profile}' is not '{HUMAN}' or a known agent profile id"
                )
            if skill_id not in valid_skills:
                errors.append(
                    f"[workflow-bad-skill] {wf_id}/{step['id']}: invoked_skill '{skill_id}' "
                    f"is not a known skill id"
                )
            elif profile in agents and profile not in skills[skill_id]["applicable_profiles"] \
                    and profile != HUMAN:
                errors.append(
                    f"[workflow-profile-not-applicable] {wf_id}/{step['id']}: responsible_profile "
                    f"'{profile}' invokes skill '{skill_id}', but that skill's "
                    f"applicable_profiles does not include '{profile}'"
                )

    for run_id, run in runs.items():
        wf_id = run["workflow_id"]
        if wf_id not in workflows:
            errors.append(f"[run-bad-workflow] {run_id}: workflow_id '{wf_id}' is not a known workflow id")
            continue
        known_step_ids = {s["id"] for s in workflows[wf_id]["steps"]}
        for run_step in run["steps"]:
            if run_step["step_id"] not in known_step_ids:
                errors.append(
                    f"[run-bad-step] {run_id}: step_id '{run_step['step_id']}' does not belong "
                    f"to workflow '{wf_id}'"
                )
        missing = known_step_ids - {s["step_id"] for s in run["steps"]}
        if missing:
            errors.append(
                f"[run-incomplete] {run_id}: does not account for workflow step(s) {sorted(missing)}"
            )

    print(
        f"Reference check: {len(agents)} agents, {len(skills)} skills, "
        f"{len(workflows)} workflows, {len(runs)} run records."
    )
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("\nOK: every workflow/skill/profile/run reference resolves.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
