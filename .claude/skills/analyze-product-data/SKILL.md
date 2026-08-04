---
name: analyze-product-data
description: Interpret product usage and feedback data to form or evaluate an evidence-backed hypothesis.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/analyze-product-data/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Analyze product data

*Canonical Guild skill id: `analyze-product-data`*

## Applicable profiles

product-data-analyst

## Inputs

- Analytics data and events
- Question or hypothesis under evaluation

## Outputs

- Analysis report with evidence, confidence and caveats

## Steps

- Pull the relevant usage, conversion or error data.
- State findings with evidence and known limitations, not just a conclusion.
- Flag when data is insufficient rather than forcing a conclusion.
