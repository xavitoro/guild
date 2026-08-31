# Triage a request

*Canonical skill id: `triage-request`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

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
