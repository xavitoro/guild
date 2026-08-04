---
name: create-threat-model
description: Assess a change or architecture proposal for security risk and classify findings.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/skills/create-threat-model/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/adapters/generate_adapters.py --target . -->

# Create a threat model

*Canonical Guild skill id: `create-threat-model`*

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
