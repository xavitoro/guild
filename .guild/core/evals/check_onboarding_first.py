#!/usr/bin/env python3
"""Fixture: proves that a project not yet onboarded is offered onboarding before
any other request is triaged (GUILD_MASTER_SPEC.md section 9.1 /
definition-of-done item 17).

Canonical only — there is nothing to check in state, because the condition is
precisely that state does not exist yet:
  1. default-policies.yaml declares an onboarding_protocol whose condition is
     .guild/state/project.yaml, asked by the DM in triage-request, naming both
     onboarding workflows, with the rules that keep the request and bring the
     question back.
  2. Both onboarding workflows exist, and each writes project.yaml in its first
     step — otherwise the condition could never stop being true.
  3. triage-request's first step is the onboarding check.
  4. The adapter generator carries the rule into the generated files.

Usage:
    python3 .guild/core/evals/check_onboarding_first.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

CORE_ROOT = Path(__file__).resolve().parents[1]  # .guild/core/

PROJECT_FILE = ".guild/state/project.yaml"
ASKER = "workflow-knowledge-orchestrator"
SKILL = "triage-request"
REQUIRED_RULES = {
    "a_request_in_a_project_without_the_project_file_is_first_offered_onboarding",
    "the_onboarding_question_is_asked_as_options_plus_free_text_before_anything_else",
    "the_onboarding_question_is_not_a_decision_request_because_there_is_no_state_yet",
    "the_original_request_is_kept_and_triaged_again_once_onboarding_closes",
    "continuing_without_onboarding_creates_no_project_file_so_the_question_returns",
    "a_request_to_onboard_or_create_a_project_skips_the_question",
}


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    protocol = _load_yaml(CORE_ROOT / "policies" / "default-policies.yaml").get("onboarding_protocol") or {}
    if not protocol:
        errors.append("[policy] default-policies.yaml declares no onboarding_protocol")
    if protocol.get("onboarded_when_exists") != PROJECT_FILE:
        errors.append(f"[policy] onboarding_protocol.onboarded_when_exists must be '{PROJECT_FILE}'")
    if protocol.get("asked_by") != ASKER:
        errors.append(f"[policy] onboarding_protocol.asked_by must be '{ASKER}'")
    if protocol.get("asked_in_skill") != SKILL:
        errors.append(f"[policy] onboarding_protocol.asked_in_skill must be '{SKILL}'")
    for rule in sorted(REQUIRED_RULES - set(protocol.get("rules", []))):
        errors.append(f"[policy] onboarding_protocol is missing rule '{rule}'")

    workflows = protocol.get("onboarding_workflows", [])
    for workflow_id in workflows:
        path = CORE_ROOT / "workflows" / workflow_id / "workflow.yaml"
        if not path.exists():
            errors.append(f"[workflow] onboarding workflow '{workflow_id}' does not exist")
            continue
        first = _load_yaml(path)["steps"][0]
        if not any("project.yaml" in out for out in first.get("expected_output_artifacts", [])):
            errors.append(f"[workflow] {workflow_id}'s first step does not write {PROJECT_FILE}, so a "
                          f"project could never stop being offered onboarding")

    steps = _load_yaml(CORE_ROOT / "skills" / SKILL / "SKILL.yaml").get("steps") or [""]
    if PROJECT_FILE not in steps[0] or "section 9.1" not in steps[0]:
        errors.append(f"[skill] {SKILL}'s first step is not the not-yet-onboarded check")

    generator = (CORE_ROOT / "adapters" / "generate_adapters.py").read_text(encoding="utf-8")
    for marker in ("### Not yet onboarded", "section 9.1"):
        if marker not in generator:
            errors.append(f"[adapter] generate_adapters.py does not emit '{marker}'")

    print(f"Onboarding-first check: {len(workflows)} onboarding workflow(s)")
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("\nOK: a project without .guild/state/project.yaml is offered onboarding before anything "
          "else, and the request is kept whatever the answer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
