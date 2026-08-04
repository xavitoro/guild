---
name: write-interface-copy
description: Produce interface copy tied to concrete screen states and actions.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/write-interface-copy/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Write interface copy

*Canonical Guild skill id: `write-interface-copy`*

## Applicable profiles

ux-content-designer

## Inputs

- Wireframes and screen-state specifications

## Outputs

- Copy deck

## Steps

- Write copy for every state and action in the specification.
- Cover error, confirmation and empty states explicitly.
- Check terminology against the existing glossary.
