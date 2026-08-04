# Reproduce a defect

*Canonical skill id: `reproduce-defect`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Reproduce a reported defect deterministically before any fix is attempted.

## Applicable profiles

quality-assurance-engineer

## Inputs

- Defect report

## Outputs

- Confirmed reproduction steps
- Observed vs. expected behavior

## Steps

- Attempt the reported steps in a controlled environment.
- Record the minimal steps that reliably reproduce the defect.
- If it cannot be reproduced, document exactly what was tried.
