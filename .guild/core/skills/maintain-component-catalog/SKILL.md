# Maintain a component catalog

*Canonical skill id: `maintain-component-catalog`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Set up or update an isolated, browsable catalog of UI components so each can be developed,
reviewed and visually verified independently of the full application.

## Applicable profiles

web-experience-engineer

## Inputs

- Implemented or changed UI components
- Wireframes and screen-state specifications, if available

## Outputs

- Component catalog entry per new or changed component

## Steps

- Add or update a catalog entry for each new or changed component.
- Cover the component's meaningful states (default, empty, error, loading, etc.), not just the happy path.
- Verify the catalog builds and runs in isolation from the full application.
