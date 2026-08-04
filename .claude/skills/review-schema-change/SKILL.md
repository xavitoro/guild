---
name: review-schema-change
description: Design or review a database schema/migration change for integrity, concurrency, compatibility and migration risk.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/skills/review-schema-change/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/adapters/generate_adapters.py --target . -->

# Review a schema change

*Canonical Guild skill id: `review-schema-change`*

## Applicable profiles

database-engineer

## Inputs

- Proposed schema or migration change

## Outputs

- Reviewed schema/migration
- Migration risk assessment

## Steps

- Check constraints, indexes and transaction boundaries.
- Assess concurrency and backward-compatibility risk.
- Document a rollback or mitigation path.
