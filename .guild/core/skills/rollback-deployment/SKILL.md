# Roll back a deployment

*Canonical skill id: `rollback-deployment`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Revert a deployment that has failed or regressed, using its documented rollback path.

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
