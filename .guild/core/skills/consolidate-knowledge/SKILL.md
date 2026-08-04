# Consolidate knowledge

*Canonical skill id: `consolidate-knowledge`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Fold evidence-backed outcomes of a workflow run into canonical planning and project memory.

## Applicable profiles

workflow-knowledge-orchestrator

## Inputs

- Workflow run outcome and its evidence

## Outputs

- Updated project-memory entries
- Updated planning/status artifacts

## Steps

- Check that every proposed memory entry cites verifiable evidence.
- Update .guild/state/knowledge/project-memory.yaml and its Markdown view.
- Update .guild/state/planning/ state to reflect the run's outcome.
