# Implement a fix

*Canonical skill id: `implement-fix`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Apply a fix for a diagnosed defect without introducing a regression.

## Applicable profiles

Artificer (product-software-engineer), Ranger (web-experience-engineer), Wizard (database-engineer), Warlock (integration-engineer)

## Inputs

- Root-cause analysis and fix plan

## Outputs

- Code change / pull request

## Steps

- Implement the fix per the agreed plan.
- Add or update a test that would have caught the original defect.
- Re-run the original reproduction steps to confirm the defect is gone.
