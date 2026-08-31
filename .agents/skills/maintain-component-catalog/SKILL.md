<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/maintain-component-catalog/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Maintain a component catalog

*Canonical Guild skill id: `maintain-component-catalog`*

## Goal

Set up or update an isolated, browsable catalog of UI components so each can be developed, reviewed and visually verified independently of the full application.

## Applicable profiles

Ranger (web-experience-engineer)

## Inputs

- Implemented or changed UI components
- Wireframes and screen-state specifications, if available

## Outputs

- Component catalog entry per new or changed component

## Steps

- Add or update a catalog entry for each new or changed component.
- Cover the component's meaningful states (default, empty, error, loading, etc.), not just the happy path.
- Verify the catalog builds and runs in isolation from the full application.
