#!/usr/bin/env python3
"""Fixture: proves the "independent QA and security gates" invariant
(GUILD_MASTER_SPEC.md principle 6 / definition-of-done item 7) holds
structurally across every agent manifest and every workflow step, not just
by convention.

Checks:
  1. Every one of the 14 agent manifests forbids every Red-tier action
     listed in .guild/core/policies/default-policies.yaml's approval_required
     (no profile may unilaterally merge to a protected branch, deploy to
     production, etc.).
  2. Every profile that can edit code (allowed_capabilities includes
     edit_code_in_branch) forbids approve_own_qa_result and
     approve_own_security_result.
  3. quality-assurance-engineer cannot edit code, and forbids
     approve_security_result (it cannot stand in for the security gate).
  4. product-security-engineer cannot edit code, and forbids
     approve_qa_result (it cannot stand in for the QA gate).
  5. Every workflow step whose gates include a Red-tier action has
     responsible_profile 'human' — a Red-tier gate is never satisfied by an
     agent profile's own say-so.

Usage:
    python3 .guild/core/evals/check_independent_gates.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

GUILD_ROOT = Path(__file__).resolve().parents[2]  # .guild/
CORE_ROOT = GUILD_ROOT / "core"
QA_ID = "quality-assurance-engineer"
SECURITY_ID = "product-security-engineer"


def load_all(glob_pattern: str) -> dict[str, dict]:
    out = {}
    for path in sorted(CORE_ROOT.glob(glob_pattern)):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        out[data["id"]] = data
    return out


def main() -> int:
    errors: list[str] = []

    policies = yaml.safe_load((CORE_ROOT / "policies" / "default-policies.yaml").read_text(encoding="utf-8"))
    red_actions = set(policies["approval_required"])

    agents = load_all("agents/*/manifest.yaml")
    workflows = load_all("workflows/*/workflow.yaml")

    for agent_id, agent in agents.items():
        forbidden = set(agent["forbidden_capabilities"])
        allowed = set(agent["allowed_capabilities"])

        missing_red = red_actions - forbidden
        if missing_red:
            errors.append(
                f"[red-not-forbidden] {agent_id}: does not forbid Red-tier action(s) "
                f"{sorted(missing_red)}"
            )

        if "edit_code_in_branch" in allowed:
            for cap in ("approve_own_qa_result", "approve_own_security_result"):
                if cap not in forbidden:
                    errors.append(
                        f"[self-approval-allowed] {agent_id}: can edit code but does not forbid "
                        f"'{cap}'"
                    )

    if QA_ID in agents:
        qa = agents[QA_ID]
        if "edit_code_in_branch" in qa["allowed_capabilities"]:
            errors.append(f"[qa-can-edit] {QA_ID}: must not be able to edit product code")
        if "approve_security_result" not in qa["forbidden_capabilities"]:
            errors.append(f"[qa-can-approve-security] {QA_ID}: must forbid 'approve_security_result'")
    else:
        errors.append(f"[missing-profile] {QA_ID} not found under .guild/core/agents/")

    if SECURITY_ID in agents:
        sec = agents[SECURITY_ID]
        if "edit_code_in_branch" in sec["allowed_capabilities"]:
            errors.append(f"[security-can-edit] {SECURITY_ID}: must not be able to edit product code")
        if "approve_qa_result" not in sec["forbidden_capabilities"]:
            errors.append(f"[security-can-approve-qa] {SECURITY_ID}: must forbid 'approve_qa_result'")
    else:
        errors.append(f"[missing-profile] {SECURITY_ID} not found under .guild/core/agents/")

    for wf_id, wf in workflows.items():
        for step in wf["steps"]:
            step_red = red_actions & set(step.get("gates", []))
            if step_red and step["responsible_profile"] != "human":
                errors.append(
                    f"[red-gate-not-human] {wf_id}/{step['id']}: gates {sorted(step_red)} include "
                    f"Red-tier action(s) but responsible_profile is '{step['responsible_profile']}', "
                    f"not 'human'"
                )

    print(
        f"Independent-gate check: {len(agents)} agents, {len(workflows)} workflows, "
        f"{len(red_actions)} Red-tier actions from default-policies.yaml."
    )
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s).")
        return 1

    print("\nOK: independent QA/security gates and Red-tier human-approval gating hold structurally.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
