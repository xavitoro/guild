---
name: consolidate-knowledge
description: Fold evidence-backed outcomes of a workflow run into canonical planning and project memory.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/skills/consolidate-knowledge/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/adapters/generate_adapters.py --target . -->

# Consolidate knowledge

*Canonical Guild skill id: `consolidate-knowledge`*

## Applicable profiles

workflow-knowledge-orchestrator

## Inputs

- Workflow run outcome and its evidence

## Outputs

- Updated project-memory entries
- Updated planning/status artifacts

## Steps

- Check that every proposed memory entry cites verifiable evidence.
- Update .guild/knowledge/project-memory.yaml and its Markdown view.
- Update .guild/planning/ state to reflect the run's outcome.
