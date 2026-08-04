# Review code in a pull request

*Canonical skill id: `review-code`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Review a pull request's correctness, test coverage and adherence to linked acceptance criteria.

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
