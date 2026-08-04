# Run a regression review

*Canonical skill id: `run-regression-review`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Verify a change against its acceptance criteria and check for regressions.

## Applicable profiles

quality-assurance-engineer

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
