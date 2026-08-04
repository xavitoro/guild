---
name: prepare-pull-request
description: Package a verified change into a pull request with a clear description and linked evidence.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/skills/prepare-pull-request/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/adapters/generate_adapters.py --target . -->

# Prepare a pull request

*Canonical Guild skill id: `prepare-pull-request`*

## Applicable profiles

workflow-knowledge-orchestrator, product-software-engineer, web-experience-engineer, database-engineer, integration-engineer, data-analytics-engineer

## Inputs

- Verified code change
- Passing gate results

## Outputs

- Pull request

## Steps

- Write a description linking the requirement, the change and the verification evidence.
- Link every passing gate result the change relies on.
- Flag any known follow-up work explicitly rather than silently deferring it.
