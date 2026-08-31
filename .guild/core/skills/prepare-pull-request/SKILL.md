# Prepare a pull request

*Canonical skill id: `prepare-pull-request`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Package a verified change into a pull request with a clear description and linked evidence.

## Applicable profiles

DM (workflow-knowledge-orchestrator), Artificer (product-software-engineer), Ranger (web-experience-engineer), Wizard (database-engineer), Warlock (integration-engineer), Monk (data-analytics-engineer)

## Inputs

- Verified code change
- Passing gate results

## Outputs

- Pull request

## Steps

- Write a description linking the requirement, the change and the verification evidence.
- Link every passing gate result the change relies on.
- Flag any known follow-up work explicitly rather than silently deferring it.
