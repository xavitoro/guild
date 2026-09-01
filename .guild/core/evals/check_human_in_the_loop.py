#!/usr/bin/env python3
"""Fixture: proves that nothing is left pending by default (GUILD_MASTER_SPEC.md
principle 13 / sections 11.1-11.2 / definition-of-done item 13), rather than
relying on a profile remembering to ask.

Canonical half — always runs, over .guild/core/ only:
  1. default-policies.yaml declares decision_request_required_fields and a
     decision_protocol naming where requests and records live, who presents,
     who answers, and the rules — including that a default never applies
     before the human has been shown it, that deferral is explicit, and that
     Red-tier actions are approvals rather than decision requests.
  2. The request-human-decision skill exists, is answerable by the human,
     and requires options, a recommendation and a default.
  3. The decision-request schema requires options (at least two), a
     recommendation and a default with an effective moment and a revisit
     trigger — a request that cannot state those cannot be written at all.
  4. project-status.schema.json accepts only decision-request ids in
     open_decisions, so an open decision can never be a bare sentence.
  5. Every workflow declares step_protocol.on_blocked_decision, and every
     profile escalates what it cannot decide to a person instead of
     assuming — with only the orchestrator allowed to present a request.

State half — runs only when .guild/state/planning/decisions/ exists:
  6. Every id in project-status open_decisions resolves to a request that is
     genuinely still open, and every still-open request is listed there and
     named in PROJECT_STATUS.md, where a person will actually see it.
  7. Every request is internally coherent: real asking profile, recommended
     and default options that exist, presented/answered/deferred states
     carrying the fields those states require.
  8. Every ledger open question blocked on the human has been escalated into
     a request — nothing blocked on a person stays a private note.

Usage:
    python3 .guild/core/evals/check_human_in_the_loop.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

GUILD_ROOT = Path(__file__).resolve().parents[2]  # .guild/
REPO_ROOT = GUILD_ROOT.parent
CORE_ROOT = GUILD_ROOT / "core"
STATE_ROOT = GUILD_ROOT / "state"
REQUESTS_DIR = STATE_ROOT / "planning" / "decisions"
STATUS_YAML = STATE_ROOT / "planning" / "project-status.yaml"
STATUS_MD = STATE_ROOT / "planning" / "PROJECT_STATUS.md"
LEDGER_DIR = STATE_ROOT / "knowledge" / "profiles"

ORCHESTRATOR = "workflow-knowledge-orchestrator"
DECISION_SKILL = "request-human-decision"
HUMAN = "human"

REQUIRED_RULES = {
    "an_open_question_blocked_on_the_human_becomes_a_decision_request",
    "every_decision_request_states_options_a_recommendation_and_a_default",
    "a_default_never_applies_before_the_human_has_been_shown_it",
    "deferral_is_an_explicit_recorded_answer_not_silence",
    "a_run_does_not_close_with_a_decision_it_needs_unpresented",
    "every_open_decision_is_listed_by_id_in_project_status",
    "red_tier_actions_are_approvals_not_decision_requests_and_never_carry_a_default",
}
REQUIRED_REQUEST_FIELDS = {
    "options_with_consequences",
    "recommendation",
    "default_if_unanswered",
    "when_the_default_takes_effect",
    "what_brings_it_back",
}
OPEN_STATES = {"open", "presented", "deferred"}


def load_all(base: Path, glob_pattern: str) -> dict[str, dict]:
    out = {}
    for path in sorted(base.glob(glob_pattern)):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        out[data["id"]] = data
    return out


def main() -> int:
    errors: list[str] = []

    policies = yaml.safe_load((CORE_ROOT / "policies" / "default-policies.yaml").read_text(encoding="utf-8"))
    agents = load_all(CORE_ROOT, "agents/*/manifest.yaml")
    skills = load_all(CORE_ROOT, "skills/*/SKILL.yaml")
    workflows = load_all(CORE_ROOT, "workflows/*/workflow.yaml")

    # 1. policy declaration
    fields = set(policies.get("human_interaction", {}).get("decision_request_required_fields", []))
    missing_fields = REQUIRED_REQUEST_FIELDS - fields
    if missing_fields:
        errors.append(f"[policy] human_interaction.decision_request_required_fields is missing "
                      f"{sorted(missing_fields)}")
    protocol = policies.get("decision_protocol")
    if not protocol:
        errors.append("[policy] default-policies.yaml declares no decision_protocol block")
        protocol = {}
    else:
        if protocol.get("presented_by") != ORCHESTRATOR:
            errors.append(f"[policy] decision_protocol.presented_by is "
                          f"'{protocol.get('presented_by')}', not '{ORCHESTRATOR}'")
        if protocol.get("answered_by") != HUMAN:
            errors.append(f"[policy] decision_protocol.answered_by is "
                          f"'{protocol.get('answered_by')}', not '{HUMAN}'")
        missing_rules = REQUIRED_RULES - set(protocol.get("rules", []))
        if missing_rules:
            errors.append(f"[policy] decision_protocol.rules is missing {sorted(missing_rules)}")
    for principle in (
        "no_decision_is_left_pending_without_an_owner_a_default_and_a_person_asked",
        "ambiguity_is_escalated_to_a_person_never_resolved_by_assumption",
    ):
        if principle not in policies.get("principles", []):
            errors.append(f"[policy] default-policies.yaml does not declare principle '{principle}'")

    # 2. the skill that puts a decision to a person
    skill = skills.get(DECISION_SKILL)
    if not skill:
        errors.append(f"[missing-skill] '{DECISION_SKILL}' does not exist under .guild/core/skills/")
    else:
        if HUMAN not in skill["applicable_profiles"]:
            errors.append(f"[skill-unanswerable] {DECISION_SKILL}: the human is not an applicable "
                          f"profile, so nothing in it is actually answered by a person")
        if ORCHESTRATOR not in skill["applicable_profiles"]:
            errors.append(f"[skill-unpresented] {DECISION_SKILL}: '{ORCHESTRATOR}' is not an "
                          f"applicable profile, so nobody presents the request")
        body = " ".join(skill["steps"] + skill["outputs"]).lower()
        for token in ("option", "recommendation", "default"):
            if token not in body:
                errors.append(f"[skill-incomplete] {DECISION_SKILL}: never mentions '{token}'")

    # 3. the schema makes an incomplete request unwritable
    schema_path = CORE_ROOT / "schemas" / "decision-request.schema.json"
    if not schema_path.exists():
        errors.append("[missing-schema] .guild/core/schemas/decision-request.schema.json does not exist")
        schema = {}
    else:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        required = set(schema.get("required", []))
        for field in ("options", "recommendation", "default_if_unanswered", "blocks", "status"):
            if field not in required:
                errors.append(f"[schema-optional] decision-request.schema.json: '{field}' is not required")
        options = schema.get("properties", {}).get("options", {})
        if options.get("minItems", 0) < 2:
            errors.append("[schema-optional] decision-request.schema.json: options does not require at "
                          "least two choices")
        default = schema.get("properties", {}).get("default_if_unanswered", {})
        for field in ("option", "in_force_from", "revisit_when"):
            if field not in default.get("required", []):
                errors.append(f"[schema-optional] decision-request.schema.json: "
                              f"default_if_unanswered.{field} is not required")

    # 4. an open decision can never be a bare sentence
    status_schema = json.loads((CORE_ROOT / "schemas" / "project-status.schema.json").read_text(encoding="utf-8"))
    pattern = status_schema["properties"]["open_decisions"].get("items", {}).get("pattern")
    if pattern != "^DR-[0-9]{3}$":
        errors.append("[schema-loose] project-status.schema.json: open_decisions does not restrict "
                      "entries to decision-request ids")

    # 5. workflows route a blocked step to a person; profiles never assume
    for wf_id, wf in workflows.items():
        route = (wf.get("step_protocol") or {}).get("on_blocked_decision")
        if route != DECISION_SKILL:
            errors.append(f"[no-decision-route] workflows/{wf_id}: step_protocol.on_blocked_decision is "
                          f"'{route}', expected '{DECISION_SKILL}'")
    for profile_id, agent in agents.items():
        escalations = " ".join(agent["escalation_conditions"]).lower()
        if "decision request" not in escalations:
            errors.append(f"[assumes-instead-of-asking] {profile_id}: no escalation condition routes a "
                          f"decision it cannot make to a person as a decision request")
        allowed = set(agent["allowed_capabilities"])
        forbidden = set(agent["forbidden_capabilities"])
        if profile_id == ORCHESTRATOR:
            if "present_decision_request" not in allowed:
                errors.append(f"[cannot-present] {profile_id}: does not allow 'present_decision_request'")
        elif "present_decision_request" not in forbidden:
            errors.append(f"[presentation-not-exclusive] {profile_id}: does not forbid "
                          f"'present_decision_request'")

    # ---------------------------------------------------------------- state
    state_checked = REQUESTS_DIR.exists()
    requests: dict[str, dict] = {}
    if state_checked:
        for path in sorted(REQUESTS_DIR.glob("*.yaml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            rel = path.relative_to(REPO_ROOT)
            requests[data["id"]] = data

            option_ids = {o["option"] for o in data["options"]}
            if data["recommendation"]["option"] not in option_ids:
                errors.append(f"[bad-recommendation] {rel}: recommends option "
                              f"'{data['recommendation']['option']}', which is not one of its options")
            if data["default_if_unanswered"]["option"] not in option_ids:
                errors.append(f"[bad-default] {rel}: defaults to option "
                              f"'{data['default_if_unanswered']['option']}', which is not one of its "
                              f"options")
            if data["raised_by"] not in agents and data["raised_by"] != HUMAN:
                errors.append(f"[bad-raiser] {rel}: raised_by '{data['raised_by']}' is not a profile")
            status = data["status"]
            if status in ("presented", "answered", "deferred") and not data.get("presented_at"):
                errors.append(f"[unshown] {rel}: status '{status}' but it was never presented — a "
                              f"default may not apply before the human has been shown it")
            if status in ("answered", "deferred"):
                for field in ("answered_at", "answer", "answered_by"):
                    if not data.get(field):
                        errors.append(f"[silent-close] {rel}: status '{status}' without '{field}' — "
                                      f"silence is not an answer")

        status_yaml = yaml.safe_load(STATUS_YAML.read_text(encoding="utf-8")) if STATUS_YAML.exists() else {}
        listed = list(status_yaml.get("open_decisions", []))
        status_md = STATUS_MD.read_text(encoding="utf-8") if STATUS_MD.exists() else ""

        for dr_id in listed:
            request = requests.get(dr_id)
            if request is None:
                errors.append(f"[dangling-open-decision] project-status.yaml lists '{dr_id}', which has "
                              f"no request under .guild/state/planning/decisions/")
            elif request["status"] not in OPEN_STATES:
                errors.append(f"[closed-but-listed] project-status.yaml still lists '{dr_id}', whose "
                              f"status is '{request['status']}'")
        for dr_id, request in requests.items():
            if request["status"] in OPEN_STATES:
                if dr_id not in listed:
                    errors.append(f"[hidden-open-decision] '{dr_id}' is still open but is not listed in "
                                  f"project-status.yaml open_decisions")
                if status_md and dr_id not in status_md:
                    errors.append(f"[hidden-from-the-human] '{dr_id}' is still open but never appears in "
                                  f"PROJECT_STATUS.md, the file a person actually reads")

        escalated = {r.get("source_question") for r in requests.values()}
        for path in sorted(LEDGER_DIR.glob("*.yaml")) if LEDGER_DIR.exists() else []:
            ledger = yaml.safe_load(path.read_text(encoding="utf-8"))
            rel = path.relative_to(REPO_ROOT)
            for question in ledger.get("open_questions", []):
                if question.get("blocked_on") != HUMAN or question.get("status") != "open":
                    continue
                if not question.get("escalated_as") and question["id"] not in escalated:
                    errors.append(f"[stranded-question] {rel}: '{question['id']}' is blocked on the "
                                  f"human but was never escalated into a decision request")
                elif question.get("escalated_as") and question["escalated_as"] not in requests:
                    errors.append(f"[dangling-escalation] {rel}: '{question['id']}' names request "
                                  f"'{question['escalated_as']}', which does not exist")

    open_count = sum(1 for r in requests.values() if r["status"] in OPEN_STATES)
    print(f"Human-in-the-loop check: {len(agents)} profiles, {len(workflows)} workflows"
          + (f", {len(requests)} decision request(s), {open_count} still open"
             if state_checked else "; no .guild/state/ decision requests (canonical checks only)"))
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("\nOK: nothing is pending without an owner, a default and a person actually asked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
