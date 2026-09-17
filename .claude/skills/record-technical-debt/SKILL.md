---
name: record-technical-debt
description: Turn a change this step found but is not going to make — one that blocks nothing — into an owned, evidenced technical-debt work item in the plan, so it stops being a note and starts being work.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/record-technical-debt/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Record found work as technical debt

*Canonical Guild skill id: `record-technical-debt`*

## Applicable profiles

DM (workflow-knowledge-orchestrator), Paladin (product-owner), Fighter (business-analyst), Druid (product-experience-designer), Bard (ux-content-designer), Ranger (web-experience-engineer), Artificer (product-software-engineer), Wizard (database-engineer), Warlock (integration-engineer), Barbarian (quality-assurance-engineer), Rogue (product-security-engineer), Cleric (cloud-devops-engineer), Sorcerer (product-data-analyst), Monk (data-analytics-engineer)

## Inputs

- A change noticed while doing something else, outside the current step's scope
- The evidence that makes it checkable — paths, artifacts, check output
- The ownership map, to find the area's owner
- The current plan, to see whether the same finding is already recorded

## Outputs

- A technical_debt work item in .guild/state/planning/project-plan.yaml with an origin and evidence
- The item's id listed in the project status's open technical debt
- The item id carried in the handoff and, when the run keeps one, in the run record's discovered work

## Steps

- Decide what this is before recording anything. A change that blocks the current step is not debt: it is part of the task, an escalation to the area's owner, or a decision request. A question nobody can answer from the project itself is a decision request, not found work. Found work is something already known to need doing, that nobody is doing now.
- Keep doing the current task. Recording found work never enlarges the current step, and never becomes a reason to start the found work instead.
- Check the plan first: if the same finding is already recorded, add the new evidence to that item rather than creating a second one. Two items for one problem is how a backlog becomes unreadable.
- State the change as an outcome another profile could pick up without re-deriving it: what is wrong, and what would be true once it is fixed. Not a symptom, and not an opinion about style.
- Record it as a work item with kind: technical_debt and an id in the TD- series, status proposed and no milestone — unscheduled. Recording found work never commits the project to doing it.
- Give it an origin: who found it, the run, step or work item it was found during, and evidence anyone can check. Found work with no traceable origin is indistinguishable from an opinion.
- Assign it to the profile that owns the area it was found in, read from the ownership map — not to whoever found it, and never to nobody. Found work arrives with an owner.
- Never schedule it. Only the Paladin (product-owner) gives found work a milestone, because scheduling is prioritization; a profile that scheduled its own findings would be setting project priority from inside whatever it happened to be doing.
- List the item's id in the project status's open technical debt, so found work is readable in one place instead of scattered across ledgers and comments.
- Never leave the finding as a TODO or FIXME comment, a ledger note or a sentence in a summary. If the observation also belongs in this profile's ledger, record both and link them: the ledger entry says what is true, the work item says what will change.
- Hand the item id on with the step's other pointers, and name it when the run is consolidated — a run does not close with found work left unrecorded.
