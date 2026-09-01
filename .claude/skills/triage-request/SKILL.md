---
name: triage-request
description: Confirm scope, urgency and the applicable workflow for an incoming request before any other profile acts.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/triage-request/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Triage a request

*Canonical Guild skill id: `triage-request`*

## Applicable profiles

DM (workflow-knowledge-orchestrator)

## Inputs

- Incoming request or work item
- The current ownership map

## Outputs

- Scoped brief
- Selected workflow id
- Ownership assignment: which areas the request touches, who owns each, and where their ledgers are

## Steps

- Read the request and any linked work item.
- Identify which of the six canonical workflows applies.
- Confirm scope boundaries and flag missing information back to the requester.
- Record the selection as the first step of the workflow run.
- Read the ownership map to see which areas the request touches and which profile owns each, and route every part to its owner rather than to whoever is available.
- Follow a pointer into an owner's ledger only where the routing decision actually needs that detail; otherwise route the question to the owner and let them answer it.
- Record any part of the request that no area covers as unowned, so the first profile to work on it claims it before starting.
- Check the open decision requests before starting: one whose answer would change this run's scope is presented to the human first, rather than guessed at.
