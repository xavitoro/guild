---
name: rollback-deployment
description: Revert a deployment that has failed or regressed, using its documented rollback path.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/rollback-deployment/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Roll back a deployment

*Canonical Guild skill id: `rollback-deployment`*

## Applicable profiles

cloud-devops-engineer

## Inputs

- Deployment execution record
- Observed failure/regression

## Outputs

- Rollback execution record

## Steps

- Confirm the failure against monitoring/alerting evidence.
- Execute the documented rollback path.
- Record the rollback outcome and notify the DM.
