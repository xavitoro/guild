# Review a schema change

*Canonical skill id: `review-schema-change`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Design or review a database schema/migration change for integrity, concurrency, compatibility and migration risk.

## Applicable profiles

Wizard (database-engineer)

## Inputs

- Proposed schema or migration change

## Outputs

- Reviewed schema/migration
- Migration risk assessment

## Steps

- Check constraints, indexes and transaction boundaries.
- Assess concurrency and backward-compatibility risk.
- Document a rollback or mitigation path.
