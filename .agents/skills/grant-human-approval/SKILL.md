<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/grant-human-approval/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Grant human approval

*Canonical Guild skill id: `grant-human-approval`*

## Goal

Record explicit human approval for a Red-tier action before it proceeds.

## Applicable profiles

human

## Inputs

- Description of the Red-tier action and its context

## Outputs

- Approval record / gate result

## Steps

- Review the proposed action and its context.
- Approve, reject or request changes explicitly.
- Record the decision as a gate result before the action proceeds.
