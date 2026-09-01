---
name: record-profile-knowledge
description: Append what a step verified to the owning profile's own knowledge ledger and hand the orchestrator a pointer to it rather than a copy.
---

<!-- GENERATED FILE — DO NOT EDIT BY HAND.
     Source of truth: .guild/core/skills/record-profile-knowledge/SKILL.yaml (schema guild.skill-manifest/v1)
     Regenerate: python3 .guild/core/adapters/generate_adapters.py --target . -->

# Record what an interaction taught this profile

*Canonical Guild skill id: `record-profile-knowledge`*

## Applicable profiles

DM (workflow-knowledge-orchestrator), Paladin (product-owner), Fighter (business-analyst), Druid (product-experience-designer), Bard (ux-content-designer), Ranger (web-experience-engineer), Artificer (product-software-engineer), Wizard (database-engineer), Warlock (integration-engineer), Barbarian (quality-assurance-engineer), Rogue (product-security-engineer), Cleric (cloud-devops-engineer), Sorcerer (product-data-analyst), Monk (data-analytics-engineer)

## Inputs

- The work just completed and the evidence it produced
- This profile's own knowledge ledger

## Outputs

- New ledger entries, or an explicit statement that nothing new was verified
- Open questions for what could not be resolved inside this boundary
- Knowledge pointers for the handoff

## Steps

- State what this step verified that the ledger does not already record. If nothing, say so explicitly — a silent step exit is indistinguishable from an owner that stopped paying attention.
- Append one entry per fact, identified KN-<this profile's canonical id>-<next sequence>, naming the owned area, the statement, evidence anyone can check, and the interaction it came from.
- Phrase each entry so another profile could act on it without re-deriving it.
- Record what could not be resolved inside this boundary as an open question, naming the profile or the human whose answer would close it.
- Never record private reasoning, temporary logs, unsupported opinions, secrets or personal data — a ledger entry is a verified observation, not a working note.
- Write only this profile's own ledger. Knowledge belonging to another area goes to its owner as an open question, never into this ledger.
- Hand the DM (workflow-knowledge-orchestrator) the new entry ids as the handoff's knowledge pointers, not their content.
- Propose an entry for canonical project memory only once it is stable and matters beyond this area, as a memory proposal for the DM to consolidate.
