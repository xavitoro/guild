# Create a threat model

*Canonical skill id: `create-threat-model`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Assess a change or architecture proposal for security risk and classify findings.

## Applicable profiles

product-security-engineer

## Inputs

- Code change / pull request or architecture proposal

## Outputs

- Threat model or security review report
- Classified findings

## Steps

- Identify trust boundaries and attack surface touched by the change.
- Review authorization logic, secret handling and dependency risk.
- Classify findings by severity with recommended remediation.
