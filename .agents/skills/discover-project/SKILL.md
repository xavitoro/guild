<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/discover-project/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Discover a project

*Canonical Guild skill id: `discover-project`*

## Goal

Produce an evidence-based picture of a repository's stack, structure, conventions and operational setup.

## Applicable profiles

DM (workflow-knowledge-orchestrator), Artificer (product-software-engineer), Cleric (cloud-devops-engineer)

## Inputs

- Repository read access

## Outputs

- Project discovery report

## Steps

- Inventory languages, frameworks and package manifests.
- Identify existing conventions, tests and CI configuration.
- Note anything undocumented or ambiguous rather than guessing.
- Summarize findings as evidence-backed statements with file references.
