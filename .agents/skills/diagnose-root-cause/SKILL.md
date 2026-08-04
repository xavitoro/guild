<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/skills/diagnose-root-cause/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/adapters/generate_adapters.py --target . -->

# Diagnose a root cause

*Canonical Guild skill id: `diagnose-root-cause`*

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
