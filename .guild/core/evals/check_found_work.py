#!/usr/bin/env python3
"""Fixture: proves that nothing a profile found is dropped (GUILD_MASTER_SPEC.md
principle 14 / section 8.1 / definition-of-done item 14), rather than relying on a
profile remembering to write it down somewhere someone might read.

Canonical half — always runs, over .guild/core/ only:
  1. default-policies.yaml declares the principle and a found_work_protocol naming
     where found work is recorded, what kind of item it becomes, who may record
     one, who it is assigned to, who may schedule it, and the rules — including
     that blocking work is not debt, that recording never authorizes doing, and
     that a TODO comment is not a record.
  2. The record-technical-debt skill exists, applies to every profile, and says
     what an item must carry.
  3. task.schema.json can express found work and makes an unsourced item
     unwritable: a technical_debt item requires an origin with a finder, a place
     and at least one piece of evidence, and milestone is not required of it —
     found work is recorded unscheduled.
  4. project-status.schema.json requires open_technical_debt and accepts only
     work-item ids in it, so found work can never be a bare sentence.
  5. project-plan.schema.json references the task schema for its work items
     rather than restating the shape, so the two cannot drift apart.
  6. Every workflow declares step_protocol.on_found_work.
  7. Every profile may record found work, and only the product owner may schedule
     it — recording is open to whoever found the evidence, prioritizing is not.

State half — runs only when .guild/state/planning/project-plan.yaml exists:
  8. Every technical_debt item carries a TD- id, a real finding profile, a place
     it was found and checkable evidence, and is assigned to a profile that
     actually owns an area.
  9. An item with a milestone was scheduled by the product owner and is no longer
     'proposed'; an unscheduled one carries no milestone and so cannot inflate
     milestone progress.
 10. Every open item is listed by id in project-status.yaml and named in
     PROJECT_STATUS.md, where a person will actually see it, and every listed id
     resolves to an item that is genuinely still open.
 11. No file under .guild/state/ parks found work in a TODO or FIXME note
     (the marker opening a line, not the word appearing in prose).

Usage:
    python3 .guild/core/evals/check_found_work.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

GUILD_ROOT = Path(__file__).resolve().parents[2]  # .guild/
REPO_ROOT = GUILD_ROOT.parent
CORE_ROOT = GUILD_ROOT / "core"
STATE_ROOT = GUILD_ROOT / "state"
PLAN_YAML = STATE_ROOT / "planning" / "project-plan.yaml"
STATUS_YAML = STATE_ROOT / "planning" / "project-status.yaml"
STATUS_MD = STATE_ROOT / "planning" / "PROJECT_STATUS.md"
OWNERSHIP_YAML = STATE_ROOT / "knowledge" / "ownership.yaml"

SKILL_ID = "record-technical-debt"
SCHEDULER = "product-owner"
PRINCIPLE = "found_non_blocking_work_becomes_a_recorded_task_never_a_note"
ITEM_KIND = "technical_debt"
ID_SERIES = "TD"
TD_ID = re.compile(r"^TD-[0-9]{3}$")
OPEN_STATES = {"proposed", "planned", "ready", "in_progress", "blocked", "in_review"}
CLOSED_STATES = {"completed", "cancelled"}
REQUIRED_RULES = {
    "work_found_outside_the_current_step_that_blocks_nothing_is_recorded_as_a_technical_debt_item",
    "work_that_blocks_the_current_step_is_not_debt_it_is_escalated_or_decided",
    "every_found_item_states_who_found_it_where_and_with_what_evidence",
    "a_found_item_is_assigned_to_the_owner_of_the_area_it_was_found_in",
    "a_found_item_is_recorded_unscheduled_and_recording_it_never_authorizes_doing_it",
    "only_the_product_owner_schedules_found_work_into_a_milestone",
    "unscheduled_found_work_is_excluded_from_milestone_progress",
    "every_open_technical_debt_item_is_listed_by_id_in_project_status",
    "a_run_does_not_close_with_found_work_left_unrecorded",
    "a_todo_comment_or_a_ledger_note_is_not_a_record_of_found_work",
}
# A parked note, not a mention: the marker opens the line (after list or comment
# markup) and introduces something, as "# TODO: ..." or "- FIXME - ..." do. Prose
# that names the marker — including this repository's own rule about it — is not a
# note, and a rule that could not state what it forbids would be unwritable.
NOTE_MARKER = re.compile(r"^[\s#\-*/>]*(TODO|FIXME)\b\s*[:\-]")


def load_all(base: Path, glob_pattern: str) -> dict[str, dict]:
    out = {}
    for path in sorted(base.glob(glob_pattern)):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        out[data["id"]] = data
    return out


def main() -> int:  # noqa: C901 - one linear proof, read top to bottom
    errors: list[str] = []

    policies = yaml.safe_load((CORE_ROOT / "policies" / "default-policies.yaml").read_text(encoding="utf-8"))
    agents = load_all(CORE_ROOT, "agents/*/manifest.yaml")
    skills = load_all(CORE_ROOT, "skills/*/SKILL.yaml")
    workflows = load_all(CORE_ROOT, "workflows/*/workflow.yaml")

    # 1. policy declaration
    if PRINCIPLE not in policies.get("principles", []):
        errors.append(f"[policy] default-policies.yaml does not declare principle '{PRINCIPLE}'")
    protocol = policies.get("found_work_protocol")
    if not protocol:
        errors.append("[policy] default-policies.yaml declares no found_work_protocol block, so nothing "
                      "fixes what happens to a change a profile finds and does not make")
        protocol = {}
    else:
        if protocol.get("item_kind") != ITEM_KIND:
            errors.append(f"[policy] found_work_protocol.item_kind is '{protocol.get('item_kind')}', "
                          f"not '{ITEM_KIND}'")
        if protocol.get("id_series") != ID_SERIES:
            errors.append(f"[policy] found_work_protocol.id_series is '{protocol.get('id_series')}', "
                          f"not '{ID_SERIES}'")
        if protocol.get("scheduled_by") != SCHEDULER:
            errors.append(f"[policy] found_work_protocol.scheduled_by is "
                          f"'{protocol.get('scheduled_by')}', not '{SCHEDULER}' — anyone able to "
                          f"schedule their own findings sets project priority from inside their own step")
        if protocol.get("recorded_by") != "any_profile":
            errors.append(f"[policy] found_work_protocol.recorded_by is '{protocol.get('recorded_by')}' — "
                          f"the profile that found the problem is the one holding its evidence, so "
                          f"recording is not restricted")
        if not protocol.get("plan_file"):
            errors.append("[policy] found_work_protocol names no plan_file, so found work has nowhere to go")
        missing_rules = REQUIRED_RULES - set(protocol.get("rules", []))
        if missing_rules:
            errors.append(f"[policy] found_work_protocol.rules is missing {sorted(missing_rules)}")

    # 2. the skill that records found work
    skill = skills.get(SKILL_ID)
    if not skill:
        errors.append(f"[missing-skill] '{SKILL_ID}' does not exist under .guild/core/skills/")
    else:
        missing_profiles = set(agents) - set(skill["applicable_profiles"])
        if missing_profiles:
            errors.append(f"[skill-not-universal] {SKILL_ID}: {sorted(missing_profiles)} cannot run it, "
                          f"so what those profiles find has nowhere to go")
        body = " ".join(skill["steps"] + skill["inputs"] + skill["outputs"]).lower()
        for token in ("origin", "evidence", "milestone", "block"):
            if token not in body:
                errors.append(f"[skill-incomplete] {SKILL_ID}: never mentions '{token}'")

    # 3. the schema makes an unsourced or auto-scheduled item unwritable
    task_schema = json.loads((CORE_ROOT / "schemas" / "task.schema.json").read_text(encoding="utf-8"))
    kinds = task_schema.get("properties", {}).get("kind", {}).get("enum", [])
    if ITEM_KIND not in kinds:
        errors.append(f"[schema-cannot-express] task.schema.json: 'kind' cannot be '{ITEM_KIND}', so "
                      f"found work is indistinguishable from planned work")
    if "milestone" in task_schema.get("required", []):
        errors.append("[schema-forces-scheduling] task.schema.json requires a milestone of every work "
                      "item, so found work cannot be recorded unscheduled and recording it would "
                      "silently commit the project to doing it")
    origin = task_schema.get("properties", {}).get("origin", {})
    for field in ("discovered_by", "discovered_in", "evidence", "recorded_at"):
        if field not in origin.get("required", []):
            errors.append(f"[schema-optional] task.schema.json: origin.{field} is not required — found "
                          f"work with no traceable origin is indistinguishable from an opinion")
    if origin.get("properties", {}).get("evidence", {}).get("minItems", 0) < 1:
        errors.append("[schema-optional] task.schema.json: origin.evidence does not require at least "
                      "one piece of checkable evidence")
    conditional = json.dumps(task_schema.get("allOf", []))
    if "origin" not in conditional or ITEM_KIND not in conditional:
        errors.append("[schema-unconditional] task.schema.json: nothing requires an origin specifically "
                      f"of a '{ITEM_KIND}' item")

    # 4. found work can never be a bare sentence in the status file
    status_schema = json.loads((CORE_ROOT / "schemas" / "project-status.schema.json").read_text(encoding="utf-8"))
    if "open_technical_debt" not in status_schema.get("required", []):
        errors.append("[schema-optional] project-status.schema.json: open_technical_debt is not "
                      "required, so a project can hide what it found by omitting the field")
    pattern = status_schema.get("properties", {}).get("open_technical_debt", {}).get("items", {}).get("pattern")
    if pattern != r"^TD-[0-9]{3}$":
        errors.append("[schema-loose] project-status.schema.json: open_technical_debt does not restrict "
                      "entries to work-item ids")

    # 5. the plan does not restate the work-item shape
    plan_schema = json.loads((CORE_ROOT / "schemas" / "project-plan.schema.json").read_text(encoding="utf-8"))
    ref = plan_schema.get("properties", {}).get("work_items", {}).get("items", {}).get("$ref")
    if ref != "https://schemas.guild.dev/task/v1":
        errors.append("[schema-duplicated] project-plan.schema.json: work_items does not reference the "
                      "task schema, so a plan's work items and task.schema.json can drift apart")

    # 6. workflows route found work
    for wf_id, wf in workflows.items():
        route = (wf.get("step_protocol") or {}).get("on_found_work")
        if route != SKILL_ID:
            errors.append(f"[no-found-work-route] workflows/{wf_id}: step_protocol.on_found_work is "
                          f"'{route}', expected '{SKILL_ID}'")

    # 7. everyone records, one profile schedules
    for profile_id, agent in agents.items():
        allowed = set(agent["allowed_capabilities"])
        forbidden = set(agent["forbidden_capabilities"])
        if "record_technical_debt" not in allowed:
            errors.append(f"[cannot-record] {profile_id}: does not allow 'record_technical_debt', so "
                          f"what it finds can only become a note")
        if profile_id == SCHEDULER:
            if "schedule_technical_debt" not in allowed:
                errors.append(f"[nobody-schedules] {profile_id}: does not allow "
                              f"'schedule_technical_debt', so found work can never be prioritized")
        elif "schedule_technical_debt" not in forbidden:
            errors.append(f"[scheduling-not-exclusive] {profile_id}: does not forbid "
                          f"'schedule_technical_debt' — a profile that schedules its own findings sets "
                          f"project priority from inside whatever it happened to be doing")

    # 8. the spec states the rule a person can read
    spec = (CORE_ROOT / "spec" / "GUILD_MASTER_SPEC.md").read_text(encoding="utf-8")
    if "### 8.1" not in spec:
        errors.append("[spec] GUILD_MASTER_SPEC.md has no section 8.1 defining how found work becomes "
                      "a task")
    if "Nothing found is dropped" not in spec:
        errors.append("[spec] GUILD_MASTER_SPEC.md does not declare 'Nothing found is dropped' as a "
                      "design principle")

    # ---------------------------------------------------------------- state
    state_checked = PLAN_YAML.exists()
    debt: dict[str, dict] = {}
    if state_checked:
        plan = yaml.safe_load(PLAN_YAML.read_text(encoding="utf-8"))
        owners = set()
        if OWNERSHIP_YAML.exists():
            ownership = yaml.safe_load(OWNERSHIP_YAML.read_text(encoding="utf-8"))
            owners = {a["owner_profile"] for a in ownership.get("areas", [])}

        for item in plan.get("work_items", []):
            if item.get("kind") != ITEM_KIND:
                if str(item["id"]).startswith(f"{ID_SERIES}-"):
                    errors.append(f"[mislabelled-item] project-plan.yaml: '{item['id']}' uses the "
                                  f"found-work id series but is not kind '{ITEM_KIND}'")
                continue
            debt[item["id"]] = item
            where = f"project-plan.yaml: '{item['id']}'"
            if not TD_ID.match(item["id"]):
                errors.append(f"[bad-id] {where} is found work but is not in the TD-### series")
            origin_data = item.get("origin") or {}
            finder = origin_data.get("discovered_by")
            if finder not in agents:
                errors.append(f"[bad-finder] {where}: origin.discovered_by '{finder}' is not a profile")
            if not origin_data.get("evidence"):
                errors.append(f"[unevidenced] {where}: no origin evidence — found work with nothing to "
                              f"check is an opinion")
            if item.get("assigned_profile") not in agents:
                errors.append(f"[unowned] {where}: assigned_profile "
                              f"'{item.get('assigned_profile')}' is not a profile")
            elif owners and item["assigned_profile"] not in owners:
                errors.append(f"[unowned-area] {where}: assigned to '{item['assigned_profile']}', which "
                              f"owns no area in the ownership map — found work is assigned to the owner "
                              f"of the area it was found in")
            status = item.get("status")
            if item.get("milestone"):
                if item.get("scheduled_by") != SCHEDULER:
                    errors.append(f"[self-scheduled] {where}: has milestone "
                                  f"'{item['milestone']}' but scheduled_by is "
                                  f"'{item.get('scheduled_by')}', not '{SCHEDULER}'")
                if status == "proposed":
                    errors.append(f"[half-scheduled] {where}: has a milestone but is still 'proposed'")
            else:
                if item.get("scheduled_by"):
                    errors.append(f"[scheduled-nowhere] {where}: names a scheduler but has no milestone")
                if status not in ("proposed", "cancelled"):
                    errors.append(f"[unscheduled-but-active] {where}: status '{status}' without a "
                                  f"milestone — found work moves beyond 'proposed' only once the "
                                  f"product owner schedules it")

        status_yaml = yaml.safe_load(STATUS_YAML.read_text(encoding="utf-8")) if STATUS_YAML.exists() else {}
        listed = list(status_yaml.get("open_technical_debt", []))
        status_md = STATUS_MD.read_text(encoding="utf-8") if STATUS_MD.exists() else ""

        for td_id in listed:
            item = debt.get(td_id)
            if item is None:
                errors.append(f"[dangling-open-debt] project-status.yaml lists '{td_id}', which is no "
                              f"found-work item in the plan")
            elif item.get("status") in CLOSED_STATES:
                errors.append(f"[closed-but-listed] project-status.yaml still lists '{td_id}', whose "
                              f"status is '{item['status']}'")
        for td_id, item in debt.items():
            if item.get("status") in OPEN_STATES:
                if td_id not in listed:
                    errors.append(f"[hidden-open-debt] '{td_id}' is open found work but is not listed in "
                                  f"project-status.yaml open_technical_debt")
                if status_md and td_id not in status_md:
                    errors.append(f"[hidden-from-the-human] '{td_id}' is open found work but never "
                                  f"appears in PROJECT_STATUS.md, the file a person actually reads")

        for path in sorted(STATE_ROOT.rglob("*")):
            if path.suffix not in (".md", ".yaml", ".yml") or not path.is_file():
                continue
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if NOTE_MARKER.search(line):
                    rel = path.relative_to(REPO_ROOT)
                    errors.append(f"[parked-as-a-note] {rel}:{number}: found work parked in a TODO or "
                                  f"FIXME note instead of the plan")

    print(f"Found-work check: {len(agents)} profiles, {len(workflows)} workflows"
          + (f", {len(debt)} technical-debt item(s)"
             if state_checked else "; no .guild/state/ plan (canonical checks only)"))
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("\nOK: work a profile found and did not do is an owned, evidenced item in the plan, "
          "unscheduled until it is prioritized, and visible where a person reads.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
