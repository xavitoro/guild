# Grant human approval

*Canonical skill id: `grant-human-approval`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

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
