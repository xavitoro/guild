---
name: diagnose-root-cause
description: Identify the root cause of a reproduced defect and propose a fix plan.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/diagnose-root-cause/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Diagnose a root cause

*Canonical Guild skill id: `diagnose-root-cause`*

## Applicable profiles

Artificer (product-software-engineer), Ranger (web-experience-engineer), Wizard (database-engineer), Warlock (integration-engineer)

## Inputs

- Reproduction steps and observed vs. expected behavior

## Outputs

- Root-cause analysis and fix plan

## Steps

- Trace the reproduction to the responsible code path.
- State the root cause, not just the symptom.
- Propose a fix plan and flag which profile should implement it.
