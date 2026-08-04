<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/skills/implement-fix/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/adapters/generate_adapters.py --target . -->

# Implement a fix

*Canonical Guild skill id: `implement-fix`*

## Goal

Apply a fix for a diagnosed defect without introducing a regression.

## Applicable profiles

product-software-engineer, web-experience-engineer, database-engineer, integration-engineer

## Inputs

- Root-cause analysis and fix plan

## Outputs

- Code change / pull request

## Steps

- Implement the fix per the agreed plan.
- Add or update a test that would have caught the original defect.
- Re-run the original reproduction steps to confirm the defect is gone.
