<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/request-human-decision/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Put a pending decision to the human

*Canonical Guild skill id: `request-human-decision`*

## Goal

Turn a decision no profile can make from the project itself into an answerable request, present it to the human, and record the answer — so nothing stays pending by default.

## Applicable profiles

DM (workflow-knowledge-orchestrator), the human

## Inputs

- An open question a profile could not resolve inside its own boundary, or an ambiguity blocking a step
- What the answer unblocks
- The evidence and constraints the asking profile already has

## Outputs

- A decision request in .guild/state/planning/decisions/
- The request presented to the human in the canonical format
- A decision record, or an explicitly recorded deferral

## Steps

- Confirm this is a decision and not a Red-tier action. A Red-tier action is an approval, blocks outright and never carries a default.
- State the question in the project's own terms, so it can be answered without reading the repository, and name what it blocks: profiles, work items or runs.
- Give at least two options, each with the consequence of choosing it.
- Give the asking profile's own recommendation and why. A request without one pushes the analysis back onto the person being asked.
- State the default that applies if nobody answers: which option, from when, and what brings the question back. Work is never blocked indefinitely, and a default is never permanent.
- Present it to the human with every field in human_interaction.decision_request_required_fields, naming the asking and blocked profiles by alias, and mark the request presented.
- Never apply a default the human has not been shown. An unshown default is a profile deciding by assumption.
- Record the answer as a decision record linked to the request in both directions, or record an explicit deferral naming the default now in force — silence is not a deferral.
- Remove the request from the project status's open decisions only once it is answered, deferred with its default recorded, or withdrawn.
