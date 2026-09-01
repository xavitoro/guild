#!/usr/bin/env python3
"""Fixture: proves the distributed-ownership model (GUILD_MASTER_SPEC.md
principle 12 / section 7 / definition-of-done item 12) holds structurally,
rather than only being described in prose.

Two halves.

Canonical half — always runs, over .guild/core/ only:
  1. default-policies.yaml declares the knowledge protocol: the ownership
     map, the per-profile ledger path, who may maintain the map, who may
     consolidate canonical memory, and the protocol rules.
  2. Every agent manifest can record its own knowledge, forbids writing
     another profile's ledger, and carries the step-entry/step-exit quality
     gate. Only the orchestrator may maintain the ownership map or
     consolidate canonical memory; every other profile forbids both.
  3. The two protocol skills (claim-ownership, record-profile-knowledge)
     exist and apply to all fourteen profiles — ownership is not a
     privilege of some roles.
  4. Every workflow declares a step_protocol whose entry/exit skills
     resolve and whose index is the ownership map from the policies.

State half — runs only when .guild/state/knowledge/ownership.yaml exists,
so a fresh .guild/core/-only installation still passes:
  5. Every area has exactly one owner, that owner is a real profile, and
     its ledger path is the owner's own ledger and exists.
  6. Every ledger belongs to a real profile, is written only by that
     profile, and every entry/question id carries that profile's own id.
  7. Map and ledgers agree in both directions on who owns what, every
     pointer (last_entry, open_questions, related_areas) resolves, and
     any promoted_to points at a real project-memory entry.

Usage:
    python3 .guild/core/evals/check_ownership_model.py
Exit code is 0 when the model holds, 1 otherwise.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

GUILD_ROOT = Path(__file__).resolve().parents[2]  # .guild/
REPO_ROOT = GUILD_ROOT.parent
CORE_ROOT = GUILD_ROOT / "core"
STATE_ROOT = GUILD_ROOT / "state"
KNOWLEDGE_ROOT = STATE_ROOT / "knowledge"
OWNERSHIP_MAP = KNOWLEDGE_ROOT / "ownership.yaml"
LEDGER_DIR = KNOWLEDGE_ROOT / "profiles"
PROJECT_MEMORY = KNOWLEDGE_ROOT / "project-memory.yaml"

ORCHESTRATOR = "workflow-knowledge-orchestrator"
ENTRY_SKILL = "claim-ownership"
EXIT_SKILL = "record-profile-knowledge"

REQUIRED_RULES = {
    "each_step_begins_with_an_ownership_claim",
    "each_step_ends_with_a_ledger_entry_or_an_explicit_nothing_new",
    "exactly_one_owner_profile_per_area",
    "a_profile_writes_only_its_own_ledger",
    "the_ownership_map_holds_pointers_not_knowledge",
    "every_ledger_entry_cites_evidence",
}


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
    protocol = policies.get("knowledge_protocol")
    if not protocol:
        errors.append("[policy] default-policies.yaml declares no knowledge_protocol block")
        protocol = {}
    else:
        if protocol.get("ownership_map_maintained_by") != ORCHESTRATOR:
            errors.append(
                f"[policy] knowledge_protocol.ownership_map_maintained_by is "
                f"'{protocol.get('ownership_map_maintained_by')}', not '{ORCHESTRATOR}'"
            )
        if protocol.get("canonical_memory_consolidated_by") != ORCHESTRATOR:
            errors.append(
                f"[policy] knowledge_protocol.canonical_memory_consolidated_by is "
                f"'{protocol.get('canonical_memory_consolidated_by')}', not '{ORCHESTRATOR}'"
            )
        missing_rules = REQUIRED_RULES - set(protocol.get("rules", []))
        if missing_rules:
            errors.append(f"[policy] knowledge_protocol.rules is missing {sorted(missing_rules)}")
    for principle in (
        "every_part_of_the_project_has_exactly_one_owning_profile",
        "each_profile_accumulates_knowledge_for_the_areas_it_owns",
        "orchestration_routes_by_pointer_not_by_omniscience",
    ):
        if principle not in policies.get("principles", []):
            errors.append(f"[policy] default-policies.yaml does not declare principle '{principle}'")

    # 2. every profile owns, records, and cannot write someone else's ledger
    for profile_id, agent in agents.items():
        allowed = set(agent["allowed_capabilities"])
        forbidden = set(agent["forbidden_capabilities"])
        if "record_own_knowledge" not in allowed:
            errors.append(f"[cannot-record] {profile_id}: does not allow 'record_own_knowledge' — a "
                          f"profile that cannot record what it learned cannot own an area")
        if "write_another_profiles_ledger" not in forbidden:
            errors.append(f"[ledger-not-protected] {profile_id}: does not forbid "
                          f"'write_another_profiles_ledger'")
        is_orchestrator = profile_id == ORCHESTRATOR
        for cap in ("maintain_ownership_map", "consolidate_verified_memory"):
            if is_orchestrator and cap not in allowed:
                errors.append(f"[orchestrator-cannot-index] {profile_id}: does not allow '{cap}'")
            if not is_orchestrator and cap not in forbidden:
                errors.append(f"[index-not-exclusive] {profile_id}: does not forbid '{cap}', which "
                              f"only the orchestrator may do")
        gates = " ".join(agent["quality_gates"]).lower()
        if "claimed area" not in gates or "ledger" not in gates:
            errors.append(f"[no-step-gate] {profile_id}: no quality gate requires a claimed area on "
                          f"step entry and a ledger entry on step exit")

    # 3. the protocol skills apply to everyone
    for skill_id in (ENTRY_SKILL, EXIT_SKILL):
        skill = skills.get(skill_id)
        if not skill:
            errors.append(f"[missing-skill] '{skill_id}' does not exist under .guild/core/skills/")
            continue
        missing = set(agents) - set(skill["applicable_profiles"])
        if missing:
            errors.append(f"[skill-not-universal] {skill_id}: not applicable to {sorted(missing)}")

    # 4. every workflow brackets its steps with the protocol
    for wf_id, wf in workflows.items():
        sp = wf.get("step_protocol")
        if not sp:
            errors.append(f"[no-step-protocol] workflows/{wf_id}: declares no step_protocol")
            continue
        for field, expected in (("on_step_entry", ENTRY_SKILL), ("on_step_exit", EXIT_SKILL)):
            if sp.get(field) not in skills:
                errors.append(f"[bad-protocol-skill] workflows/{wf_id}: step_protocol.{field} "
                              f"'{sp.get(field)}' is not a known skill id")
            elif sp[field] != expected:
                errors.append(f"[unexpected-protocol-skill] workflows/{wf_id}: step_protocol.{field} "
                              f"is '{sp[field]}', expected '{expected}'")
        if protocol.get("ownership_map") and sp.get("index") != protocol["ownership_map"]:
            errors.append(f"[protocol-index-mismatch] workflows/{wf_id}: step_protocol.index "
                          f"'{sp.get('index')}' is not the policy's ownership map "
                          f"'{protocol['ownership_map']}'")

    # ---------------------------------------------------------------- state
    state_checked = False
    if OWNERSHIP_MAP.exists():
        state_checked = True
        omap = yaml.safe_load(OWNERSHIP_MAP.read_text(encoding="utf-8"))
        areas = {a["id"]: a for a in omap["areas"]}

        if omap.get("updated_by") != ORCHESTRATOR:
            errors.append(f"[map-author] {OWNERSHIP_MAP.relative_to(REPO_ROOT)}: updated_by is "
                          f"'{omap.get('updated_by')}'; only the orchestrator maintains the map")

        seen: dict[str, str] = {}
        for area in omap["areas"]:
            aid = area["id"]
            if aid in seen:
                errors.append(f"[duplicate-area] '{aid}' appears more than once in the ownership map")
            seen[aid] = area["owner_profile"]
            owner = area["owner_profile"]
            if owner not in agents:
                errors.append(f"[bad-owner] area '{aid}': owner_profile '{owner}' is not a known profile")
                continue
            expected_ledger = f".guild/state/knowledge/profiles/{owner}.yaml"
            if area["ledger"] != expected_ledger:
                errors.append(f"[bad-ledger-path] area '{aid}': ledger '{area['ledger']}' is not its "
                              f"owner's ledger '{expected_ledger}'")
            if not (REPO_ROOT / area["ledger"]).exists():
                errors.append(f"[missing-ledger] area '{aid}': ledger '{area['ledger']}' does not exist")
            for related in area.get("related_areas", []):
                if related not in areas:
                    errors.append(f"[bad-related-area] area '{aid}': related_areas references unknown "
                                  f"'{related}'")

        memory_ids = set()
        if PROJECT_MEMORY.exists():
            memory = yaml.safe_load(PROJECT_MEMORY.read_text(encoding="utf-8"))
            memory_ids = {e["id"] for e in memory.get("entries", [])}

        ledgers: dict[str, dict] = {}
        for path in sorted(LEDGER_DIR.glob("*.yaml")) if LEDGER_DIR.exists() else []:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            rel = path.relative_to(REPO_ROOT)
            profile_id = data["profile"]
            if path.stem != profile_id:
                errors.append(f"[ledger-name-mismatch] {rel}: declares profile '{profile_id}'")
                continue
            if profile_id not in agents:
                errors.append(f"[orphan-ledger] {rel}: '{profile_id}' is not a known profile")
                continue
            if data["updated_by"] != profile_id:
                errors.append(f"[foreign-writer] {rel}: updated_by '{data['updated_by']}' — a profile "
                              f"writes only its own ledger")
            ledgers[profile_id] = data

            for area_id in data["owned_areas"]:
                if area_id not in areas:
                    errors.append(f"[unmapped-claim] {rel}: claims '{area_id}', which the ownership "
                                  f"map does not list")
                elif areas[area_id]["owner_profile"] != profile_id:
                    errors.append(f"[contested-area] {rel}: claims '{area_id}', which the map assigns "
                                  f"to '{areas[area_id]['owner_profile']}'")

            for entry in data["entries"]:
                if not entry["id"].startswith(f"KN-{profile_id}-"):
                    errors.append(f"[misfiled-entry] {rel}: entry '{entry['id']}' is not filed under "
                                  f"'KN-{profile_id}-'")
                if entry["area"] not in data["owned_areas"]:
                    errors.append(f"[entry-outside-boundary] {rel}: entry '{entry['id']}' records area "
                                  f"'{entry['area']}', which this profile does not own")
                promoted = entry.get("promoted_to")
                if promoted and memory_ids and promoted not in memory_ids:
                    errors.append(f"[bad-promotion] {rel}: entry '{entry['id']}' claims promotion to "
                                  f"'{promoted}', which is not in project memory")

            for question in data.get("open_questions", []):
                if not question["id"].startswith(f"KNQ-{profile_id}-"):
                    errors.append(f"[misfiled-question] {rel}: open question '{question['id']}' is not "
                                  f"filed under 'KNQ-{profile_id}-'")
                blocked = question.get("blocked_on")
                if blocked and blocked != "human" and blocked not in agents:
                    errors.append(f"[bad-blocked-on] {rel}: open question '{question['id']}' is blocked "
                                  f"on '{blocked}', which is neither a profile nor 'human'")

        # pointers in the map must resolve into the owner's ledger
        for area in omap["areas"]:
            owner = area["owner_profile"]
            ledger = ledgers.get(owner)
            if ledger is None:
                continue
            if area["id"] not in ledger["owned_areas"]:
                errors.append(f"[unacknowledged-ownership] area '{area['id']}': the map assigns it to "
                              f"'{owner}', whose ledger does not list it in owned_areas")
            entry_ids = {e["id"] for e in ledger["entries"]}
            question_ids = {q["id"] for q in ledger.get("open_questions", [])}
            if area.get("last_entry") and area["last_entry"] not in entry_ids:
                errors.append(f"[dangling-pointer] area '{area['id']}': last_entry "
                              f"'{area['last_entry']}' is not in '{owner}'s ledger")
            for qid in area.get("open_questions", []):
                if qid not in question_ids:
                    errors.append(f"[dangling-pointer] area '{area['id']}': open question '{qid}' is "
                                  f"not in '{owner}'s ledger")

    print(f"Ownership model check: {len(agents)} profiles, {len(skills)} skills, "
          f"{len(workflows)} workflows"
          + (f", {len(yaml.safe_load(OWNERSHIP_MAP.read_text(encoding='utf-8'))['areas'])} owned areas "
             f"in .guild/state/" if state_checked else "; no .guild/state/ ownership map (canonical "
             f"checks only)"))
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("\nOK: every part has one owner, every owner records its own knowledge, and the "
          "orchestrator routes by pointer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
