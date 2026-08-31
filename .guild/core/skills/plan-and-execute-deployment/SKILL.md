# Plan and execute a deployment

*Canonical skill id: `plan-and-execute-deployment`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Plan and, once approved, execute a deployment with a documented rollback path.

## Applicable profiles

Cleric (cloud-devops-engineer)

## Preconditions

- The change has a passing quality-assurance-engineer gate result.

## Inputs

- Verified change with a passing QA gate

## Outputs

- Deployment/rollback plan
- Deployment execution record

## Steps

- Write a deployment plan including a rollback path.
- Confirm the QA gate, and security gate where applicable, are passing.
- Execute the deployment only after any required human approval is recorded.
