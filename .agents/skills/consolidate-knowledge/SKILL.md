<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/consolidate-knowledge/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Consolidate knowledge

*Canonical Guild skill id: `consolidate-knowledge`*

## Goal

Fold evidence-backed outcomes of a workflow run into canonical planning and project memory.

## Applicable profiles

DM (workflow-knowledge-orchestrator)

## Inputs

- Workflow run outcome and its evidence
- The ledger entries and open questions the run's owners recorded

## Outputs

- Updated project-memory entries
- Updated planning/status artifacts
- Refreshed ownership-map pointers
- Every decision this run needed either answered or explicitly deferred

## Steps

- Collect the knowledge pointers the run's owners handed over, rather than re-deriving what they learned.
- Sweep the owners' open questions: anything blocked on the human becomes a decision request and is presented before this run is recorded complete. A run does not close with a decision it needed left unpresented.
- Check that every proposed memory entry cites verifiable evidence.
- Promote a ledger entry into canonical memory only through a memory proposal, and set promoted_to on that entry so both layers stay linked.
- Update .guild/state/knowledge/project-memory.yaml and its Markdown view.
- Refresh the ownership map: new or changed areas and boundaries, each owner's newest entry id, open questions and related areas — pointers only, never a copy of what an owner knows.
- Update .guild/state/planning/ state to reflect the run's outcome.
