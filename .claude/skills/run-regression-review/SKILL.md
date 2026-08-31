---
name: run-regression-review
description: Verify a change against its acceptance criteria and check for regressions.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/run-regression-review/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Run a regression review

*Canonical Guild skill id: `run-regression-review`*

## Applicable profiles

Barbarian (quality-assurance-engineer)

## Inputs

- Code change / pull request
- Acceptance criteria or original reproduction steps

## Outputs

- Test results
- Gate result: pass or fail

## Steps

- Derive or reuse a test plan from the acceptance criteria.
- Run automated and, where warranted, exploratory checks.
- Record a pass/fail gate result referencing each criterion.
