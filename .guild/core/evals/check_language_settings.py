#!/usr/bin/env python3
"""Fixture: proves that the human chooses the languages Guild uses in a project
(GUILD_MASTER_SPEC.md principle 15 / section 3.2 / definition-of-done item 15) —
conversation, state prose and git — rather than a profile picking one.

Canonical half — always runs, over .guild/core/ only:
  1. default-policies.yaml declares the principle and a language_protocol naming
     the settings file and field, the three settings, who asks, that only the
     human chooses, the steps that ask, and the rules.
  2. project.schema.json can record all three settings, each as a language tag,
     and requires all three once `languages` is present.
  3. Every step named in language_protocol.asked_in_steps exists, is run by the
     asking profile, invokes triage-request, and is the first step of its
     workflow — the languages are asked before any other question — and outputs
     the language settings.
  4. The triage-request skill asks for the languages before anything else, except
     the not-yet-onboarded check of section 9.1.
  5. Every profile's AGENT.md tells it to read the languages from project.yaml.
  6. The adapter generator carries the rule into the generated subagents and into
     the AGENTS.md / CLAUDE.md blocks.

State half — runs only when .guild/state/project.yaml exists:
  7. A project.yaml with `languages` validates against the schema. One without it
     is a warning, not an error: state that predates section 3.2 stays valid, and
     the DM asks for the languages at the next triage.

Usage:
    python3 .guild/core/evals/check_language_settings.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

GUILD_ROOT = Path(__file__).resolve().parents[2]  # .guild/
REPO_ROOT = GUILD_ROOT.parent
CORE_ROOT = GUILD_ROOT / "core"
STATE_ROOT = GUILD_ROOT / "state"
PROJECT_YAML = STATE_ROOT / "project.yaml"

PRINCIPLE = "the_human_chooses_the_conversation_state_prose_and_git_languages"
SETTINGS = ["conversation", "state_prose", "git"]
ASKER = "workflow-knowledge-orchestrator"
TRIAGE_SKILL = "triage-request"
REQUIRED_RULES = {
    "the_three_languages_are_asked_before_any_other_onboarding_question",
    "each_language_is_asked_as_options_plus_free_text",
    "every_profile_reads_the_languages_from_the_settings_file_and_never_infers_one",
    "missing_language_settings_are_asked_at_the_next_triage_never_assumed",
    "ids_aliases_keys_file_names_answer_keys_and_verbatim_evidence_are_never_translated",
}


def _load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    # 1. Policy
    policies = _load_yaml(CORE_ROOT / "policies" / "default-policies.yaml")
    if PRINCIPLE not in policies.get("principles", []):
        errors.append(f"[policy] principle '{PRINCIPLE}' is not declared")
    protocol = policies.get("language_protocol") or {}
    if not protocol:
        errors.append("[policy] default-policies.yaml declares no language_protocol")
    if protocol.get("settings_file") != ".guild/state/project.yaml":
        errors.append("[policy] language_protocol.settings_file is not .guild/state/project.yaml")
    if protocol.get("settings_field") != "languages":
        errors.append("[policy] language_protocol.settings_field is not 'languages'")
    if sorted(protocol.get("settings", [])) != sorted(SETTINGS):
        errors.append(f"[policy] language_protocol.settings must be exactly {SETTINGS}")
    if protocol.get("asked_by") != ASKER:
        errors.append(f"[policy] language_protocol.asked_by must be '{ASKER}'")
    if protocol.get("chosen_by") != "human":
        errors.append("[policy] language_protocol.chosen_by must be 'human'")
    for rule in sorted(REQUIRED_RULES - set(protocol.get("rules", []))):
        errors.append(f"[policy] language_protocol is missing rule '{rule}'")

    # 2. Schema
    schema = json.loads((CORE_ROOT / "schemas" / "project.schema.json").read_text(encoding="utf-8"))
    languages = schema.get("properties", {}).get("languages", {})
    if not languages:
        errors.append("[schema] project.schema.json cannot record `languages`")
    else:
        if sorted(languages.get("required", [])) != sorted(SETTINGS):
            errors.append(f"[schema] `languages` must require exactly {SETTINGS}")
        for setting in SETTINGS:
            if "pattern" not in languages.get("properties", {}).get(setting, {}):
                errors.append(f"[schema] languages.{setting} is not constrained to a language tag")

    # 3. Workflow steps
    steps_by_id = {}
    for path in sorted((CORE_ROOT / "workflows").glob("*/workflow.yaml")):
        workflow = _load_yaml(path)
        for index, step in enumerate(workflow.get("steps", [])):
            steps_by_id[step["id"]] = (workflow["id"], index, step)
    asked_in = protocol.get("asked_in_steps", [])
    if not asked_in:
        errors.append("[workflow] language_protocol.asked_in_steps names no step")
    for step_id in asked_in:
        if step_id not in steps_by_id:
            errors.append(f"[workflow] '{step_id}' in asked_in_steps is not a workflow step")
            continue
        workflow_id, index, step = steps_by_id[step_id]
        where = f"{workflow_id}/{step_id}"
        if index != 0:
            errors.append(f"[workflow] {where} is not the first step, so the languages would not "
                          f"be asked before any other question")
        if step.get("responsible_profile") != ASKER:
            errors.append(f"[workflow] {where} is not run by '{ASKER}'")
        if step.get("invoked_skill") != TRIAGE_SKILL:
            errors.append(f"[workflow] {where} does not invoke '{TRIAGE_SKILL}'")
        if not any("project.yaml" in out for out in step.get("expected_output_artifacts", [])):
            errors.append(f"[workflow] {where} does not output the language settings in project.yaml")

    # 4. Triage skill asks first — only the not-yet-onboarded check (section 9.1) may precede it
    triage = _load_yaml(CORE_ROOT / "skills" / TRIAGE_SKILL / "SKILL.yaml")
    triage_steps = triage.get("steps") or []
    asks = [i for i, text in enumerate(triage_steps)
            if "project.yaml" in text and all(word in text for word in ("converses", "state prose", "git"))]
    if not asks:
        errors.append(f"[skill] {TRIAGE_SKILL} has no step asking for the three languages")
    elif any("section 9.1" not in triage_steps[i] for i in range(asks[0])):
        errors.append(f"[skill] {TRIAGE_SKILL} asks something other than the onboarding check before "
                      f"the three languages")

    # 5. Every profile reads the languages
    agent_docs = sorted((CORE_ROOT / "agents").glob("*/AGENT.md"))
    for path in agent_docs:
        text = path.read_text(encoding="utf-8")
        if "`languages`" not in text or "section 3.2" not in text:
            errors.append(f"[agent] {path.relative_to(REPO_ROOT)} does not point the profile at "
                          f"the recorded languages")

    # 6. Generator carries the rule
    generator = (CORE_ROOT / "adapters" / "generate_adapters.py").read_text(encoding="utf-8")
    for marker in ("language_note", "### Languages", "section 3.2"):
        if marker not in generator:
            errors.append(f"[adapter] generate_adapters.py does not emit '{marker}'")

    # 7. State
    state_checked = PROJECT_YAML.exists()
    if state_checked:
        project = _load_yaml(PROJECT_YAML) or {}
        if "languages" not in project:
            warnings.append(f"{PROJECT_YAML.relative_to(REPO_ROOT)} records no languages; the DM "
                            f"asks for them at the next triage")
        else:
            for error in Draft202012Validator(schema).iter_errors(project):
                errors.append(f"[state] {PROJECT_YAML.relative_to(REPO_ROOT)}: {error.message}")

    print(f"Language-settings check: {len(agent_docs)} profiles, {len(asked_in)} asking step(s)"
          + ("" if state_checked else "; no .guild/state/project.yaml (canonical checks only)"))
    for warning in warnings:
        print(f"WARNING {warning}")
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("\nOK: the human chooses the conversation, state-prose and git languages at onboarding, "
          "before any other question, and every profile reads them from project.yaml.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
