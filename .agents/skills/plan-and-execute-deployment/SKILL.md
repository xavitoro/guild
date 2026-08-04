<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/plan-and-execute-deployment/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Plan and execute a deployment

*Canonical Guild skill id: `plan-and-execute-deployment`*

## Goal

Plan and, once approved, execute a deployment with a documented rollback path.

## Applicable profiles

cloud-devops-engineer

## Inputs

- Verified change with a passing QA gate

## Outputs

- Deployment/rollback plan
- Deployment execution record

## Steps

- Write a deployment plan including a rollback path.
- Confirm the QA gate, and security gate where applicable, are passing.
- Execute the deployment only after any required human approval is recorded.
