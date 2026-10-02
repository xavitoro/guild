# Triage a request

*Canonical skill id: `triage-request`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Confirm scope, urgency and the applicable workflow for an incoming request before any other profile acts.

## Applicable profiles

DM (workflow-knowledge-orchestrator)

## Inputs

- Incoming request or work item
- The current ownership map
- .guild/state/project.yaml, for the project's language settings

## Outputs

- Scoped brief
- Selected workflow id
- Ownership assignment: which areas the request touches, who owns each, and where their ledgers are
- Language settings in .guild/state/project.yaml (conversation, state prose, git), when they were missing

## Steps

- Read the language settings in .guild/state/project.yaml. If the project has none — always the case when onboarding, and the case for state created before they existed — ask the human for them before anything else: the language Guild converses in, the language state prose is written in, and the language of git history, one question each, as options plus free text (GUILD_MASTER_SPEC.md section 3.2). Ask in the language the request was written in, record the answers in .guild/state/project.yaml, and speak in the chosen conversation language from then on.
- Read the request and any linked work item.
- Identify which of the six canonical workflows applies.
- Confirm scope boundaries and flag missing information back to the requester.
- Record the selection as the first step of the workflow run.
- Read the ownership map to see which areas the request touches and which profile owns each, and route every part to its owner rather than to whoever is available.
- Follow a pointer into an owner's ledger only where the routing decision actually needs that detail; otherwise route the question to the owner and let them answer it.
- Record any part of the request that no area covers as unowned, so the first profile to work on it claims it before starting.
- Check the open decision requests before starting: one whose answer would change this run's scope is presented to the human first, rather than guessed at.
