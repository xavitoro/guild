# Diagnose a root cause

*Canonical skill id: `diagnose-root-cause`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Identify the root cause of a reproduced defect and propose a fix plan.

## Applicable profiles

product-software-engineer, web-experience-engineer, database-engineer, integration-engineer

## Inputs

- Reproduction steps and observed vs. expected behavior

## Outputs

- Root-cause analysis and fix plan

## Steps

- Trace the reproduction to the responsible code path.
- State the root cause, not just the symptom.
- Propose a fix plan and flag which profile should implement it.
