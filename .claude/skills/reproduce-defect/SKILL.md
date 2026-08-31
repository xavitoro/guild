---
name: reproduce-defect
description: Reproduce a reported defect deterministically before any fix is attempted.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/reproduce-defect/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Reproduce a defect

*Canonical Guild skill id: `reproduce-defect`*

## Applicable profiles

Barbarian (quality-assurance-engineer)

## Inputs

- Defect report

## Outputs

- Confirmed reproduction steps
- Observed vs. expected behavior

## Steps

- Attempt the reported steps in a controlled environment.
- Record the minimal steps that reliably reproduce the defect.
- If it cannot be reproduced, document exactly what was tried.
