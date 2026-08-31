<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/triage-request/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Triage a request

*Canonical Guild skill id: `triage-request`*

## Goal

Confirm scope, urgency and the applicable workflow for an incoming request before any other profile acts.

## Applicable profiles

DM (workflow-knowledge-orchestrator)

## Inputs

- Incoming request or work item

## Outputs

- Scoped brief
- Selected workflow id

## Steps

- Read the request and any linked work item.
- Identify which of the six canonical workflows applies.
- Confirm scope boundaries and flag missing information back to the requester.
- Record the selection as the first step of the workflow run.
