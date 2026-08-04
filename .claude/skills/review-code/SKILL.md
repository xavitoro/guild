---
name: review-code
description: Review a pull request's correctness, test coverage and adherence to linked acceptance criteria.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/skills/review-code/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/adapters/generate_adapters.py --target . -->

# Review code in a pull request

*Canonical Guild skill id: `review-code`*

## Applicable profiles

quality-assurance-engineer

## Inputs

- Pull request
- Linked requirement or acceptance criteria, if any

## Outputs

- Review comments
- Gate result: pass or fail

## Steps

- Check the change against linked acceptance criteria, if any.
- Review test coverage and code quality.
- Record a pass/fail gate result with specific comments.
