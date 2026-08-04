#!/usr/bin/env python3
"""Smoke test: proves the generated Codex/Claude Code adapters actually cover
everything the `add-feature` workflow needs to run, end to end.

For every step in .guild/core/workflows/add-feature/workflow.yaml, checks that:
  - the step's responsible_profile ('human' excepted) has a generated
    .claude/agents/<id>.md subagent, with a tools: line and a source header
    pointing back at its canonical manifest;
  - the step's invoked_skill has a generated .claude/skills/<id>/SKILL.md
    and .agents/skills/<id>/SKILL.md, each with a source header pointing
    back at its canonical SKILL.yaml.

Then runs the adapter drift check to confirm nothing generated is stale.

This is a demonstration of coverage for one concrete workflow, not a
replacement for .guild/core/evals/check_workflow_refs.py (which checks
every workflow's references against the canonical catalogue, independent
of whether adapters have been generated).

Usage:
    python3 .guild/core/evals/smoke_test_add_feature.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

CORE_ROOT = Path(__file__).resolve().parents[1]  # .guild/core/
REPO_ROOT = Path(__file__).resolve().parents[3]
WORKFLOW_PATH = CORE_ROOT / "workflows" / "add-feature" / "workflow.yaml"
GENERATED_MARKER = "GENERATED FILE — DO NOT EDIT BY HAND."


def check_generated_file(path: Path, source_fragment: str, errors: list[str]):
    if not path.exists():
        errors.append(f"[missing] {path.relative_to(REPO_ROOT)} was not generated")
        return
    text = path.read_text(encoding="utf-8")
    if GENERATED_MARKER not in text:
        errors.append(f"[no-header] {path.relative_to(REPO_ROOT)} is missing its generated-file header")
    if source_fragment not in text:
        errors.append(
            f"[bad-source] {path.relative_to(REPO_ROOT)} does not reference its canonical source "
            f"'{source_fragment}'"
        )


def main() -> int:
    errors: list[str] = []
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))

    profiles_seen: set[str] = set()
    skills_seen: set[str] = set()

    for step in workflow["steps"]:
        profile = step["responsible_profile"]
        skill = step["invoked_skill"]

        if profile != "human" and profile not in profiles_seen:
            agent_path = REPO_ROOT / ".claude" / "agents" / f"{profile}.md"
            check_generated_file(
                agent_path, f".guild/core/agents/{profile}/manifest.yaml", errors
            )
            if agent_path.exists() and "tools:" not in agent_path.read_text(encoding="utf-8"):
                errors.append(f"[no-tools] {agent_path.relative_to(REPO_ROOT)} has no tools: grant")
        profiles_seen.add(profile)

        if skill not in skills_seen:
            codex_skill_path = REPO_ROOT / ".agents" / "skills" / skill / "SKILL.md"
            claude_skill_path = REPO_ROOT / ".claude" / "skills" / skill / "SKILL.md"
            check_generated_file(codex_skill_path, f".guild/core/skills/{skill}/SKILL.yaml", errors)
            check_generated_file(claude_skill_path, f".guild/core/skills/{skill}/SKILL.yaml", errors)
        skills_seen.add(skill)

    print(
        f"add-feature smoke test: {len(workflow['steps'])} steps, "
        f"{len(profiles_seen)} distinct profiles, {len(skills_seen)} distinct skills."
    )
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("Every profile and skill add-feature needs has a generated Codex/Claude Code adapter.")

    drift = subprocess.run(
        [sys.executable, str(CORE_ROOT / "adapters" / "generate_adapters.py"),
         "--target", str(REPO_ROOT), "--check"],
        capture_output=True, text=True,
    )
    print(drift.stdout.strip())
    if drift.returncode != 0:
        print(drift.stderr.strip())
        print("\nFAILED: generated adapters have drifted from canonical sources.")
        return 1

    print("\nOK: add-feature is fully covered by up-to-date generated adapters.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
