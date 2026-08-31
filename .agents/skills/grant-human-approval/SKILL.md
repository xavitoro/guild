<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/grant-human-approval/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Grant human approval

*Canonical Guild skill id: `grant-human-approval`*

## Goal

Record explicit human approval for a Red-tier action before it proceeds.

## Applicable profiles

the human

## Inputs

- An approval request in the canonical format, naming the asking profile (the DM) and the profile blocked on the answer, each by alias and canonical id
- Description of the Red-tier action, its policy key and its context
- Gate results and artifacts that back the request

## Outputs

- Approval record / gate result

## Steps

- Check that the request states every field required by human_interaction.approval_request_required_fields in .guild/core/policies/default-policies.yaml, including which profile is asking and which profile is blocked, named by alias.
- Return an incomplete or unattributed request to the DM instead of answering it.
- Review the proposed action, its evidence and the stated effect of approving and of rejecting.
- Approve, reject or request changes explicitly, addressing the asking profile by alias.
- Record the decision as a gate result whose requested_by names the requesting profile's canonical id, before the action proceeds.
