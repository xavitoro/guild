<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/claim-ownership/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Claim ownership of an area

*Canonical Guild skill id: `claim-ownership`*

## Goal

Take explicit, recorded ownership of the part of the project a step touches, before any work on it starts.

## Applicable profiles

DM (workflow-knowledge-orchestrator), Paladin (product-owner), Fighter (business-analyst), Druid (product-experience-designer), Bard (ux-content-designer), Ranger (web-experience-engineer), Artificer (product-software-engineer), Wizard (database-engineer), Warlock (integration-engineer), Barbarian (quality-assurance-engineer), Rogue (product-security-engineer), Cleric (cloud-devops-engineer), Sorcerer (product-data-analyst), Monk (data-analytics-engineer)

## Inputs

- The step's scope and its required input artifacts
- The current ownership map
- This profile's own knowledge ledger

## Outputs

- A claimed or confirmed area, recorded in this profile's ledger
- The claim handed to the DM (workflow-knowledge-orchestrator) for the ownership map
- Open questions for anything the step needs that falls outside the claimed boundary

## Steps

- Read the ownership map and find the area this step falls in.
- If this profile already owns that area, confirm the boundary still matches the work, and state how it has moved if it has.
- If no area covers the work, propose one — a name, an explicit boundary of what is inside and what is not, and the concrete paths it covers.
- If another profile owns it, do not start: hand the work back to the DM to route to its owner. Two owners for one part is a boundary error, not collaboration.
- Record the claimed area in this profile's own ledger under owned_areas, and read that ledger's existing entries for the area before starting — that accumulated knowledge is what ownership is for.
- Hand the DM the claim so it can record the area, its owner, the ledger path and the related areas whose owners this work must coordinate with.
