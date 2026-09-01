# Project knowledge

This project's own knowledge, in three layers. Only the last one is canonical,
and each layer is narrower than the one below it.

```text
interaction
→ ledger entry        profiles/<profile-id>.yaml   (its owner, evidence-backed)
→ memory proposal     submitted by that owner
→ project memory      project-memory.yaml          (the DM consolidates)
```

| File | What it holds | Who writes it |
|---|---|---|
| [`ownership.yaml`](ownership.yaml) / [`OWNERSHIP.md`](OWNERSHIP.md) | The index: area, single owner, ledger location, newest entry, open questions, related areas. Pointers only. | The DM (`workflow-knowledge-orchestrator`) only |
| [`profiles/<profile-id>.yaml`](profiles/) | One profile's accumulated knowledge about the areas it owns, appended as it works | That profile only |
| [`project-memory.yaml`](project-memory.yaml) / [`PROJECT_MEMORY.md`](PROJECT_MEMORY.md) | Consolidated canonical memory | The DM only, from accepted proposals |
| [`decisions/`](decisions/) | Accepted decision records | The DM, recording a decision made |

Rules that make this work, from `GUILD_MASTER_SPEC.md` section 7:

- Exactly one owner per area. Two owners is a boundary error, not collaboration.
- A profile writes only its own ledger. The DM maintains the index over them and
  never rewrites their content.
- Every entry cites evidence anyone can check. No private reasoning, temporary
  logs, unsupported opinions, secrets or personal data.
- What an owner cannot resolve inside its boundary becomes an open question
  naming who could answer it, rather than a silent gap.
- Canonical memory is reached only through a memory proposal, and the accepted
  entry's id is written back to the ledger entry as `promoted_to`.
- An open question blocked on the human does not stay here: the DM escalates it
  into a decision request under
  [`../planning/decisions/`](../planning/decisions/) with options, a
  recommendation and a default, and the answer comes back as a record in
  [`decisions/`](decisions/). See `GUILD_MASTER_SPEC.md` section 11.2.

Shapes to copy when adding either file:
`.guild/core/templates/ownership-map.template.yaml` and
`.guild/core/templates/profile-knowledge.template.yaml`.
