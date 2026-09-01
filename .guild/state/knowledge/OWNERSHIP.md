# Ownership map

Human-readable view of [`ownership.yaml`](ownership.yaml) (schema
`guild.ownership-map/v1`), which is canonical. Every part of this repository has
exactly one owning profile; what that owner knows lives in its own ledger under
[`profiles/`](profiles/), never here. The DM (`workflow-knowledge-orchestrator`)
routes by this index — it needs to know who owns a part and where their ledger
is, not what the ledger says. See `GUILD_MASTER_SPEC.md` section 7.

| Area | Owner | Covers | Knowledge lives in |
|---|---|---|---|
| Guild master specification | DM (`workflow-knowledge-orchestrator`) | `.guild/core/spec/` | [`profiles/workflow-knowledge-orchestrator.yaml`](profiles/workflow-knowledge-orchestrator.yaml) |
| Artifact schemas and templates | DM | `.guild/core/schemas/`, `.guild/core/templates/` | same ledger |
| Agent profile definitions | DM | `.guild/core/agents/` | same ledger |
| Skill catalogue and workflow graphs | Fighter (`business-analyst`) | `.guild/core/skills/`, `.guild/core/workflows/` | [`profiles/business-analyst.yaml`](profiles/business-analyst.yaml) |
| Provider adapters | Artificer (`product-software-engineer`) | `.guild/core/adapters/`, `.agents/`, `.claude/` | [`profiles/product-software-engineer.yaml`](profiles/product-software-engineer.yaml) |
| Structural validation and fixtures | Barbarian (`quality-assurance-engineer`) | `.guild/core/evals/` | [`profiles/quality-assurance-engineer.yaml`](profiles/quality-assurance-engineer.yaml) |
| Policies, permission tiers and approval gates | Rogue (`product-security-engineer`) | `.guild/core/policies/` | [`profiles/product-security-engineer.yaml`](profiles/product-security-engineer.yaml) |
| This project's planning state | DM | `.guild/state/planning/` | same ledger |
| This project's knowledge state | DM | `.guild/state/knowledge/` | same ledger |

## Open questions

Each is a pointer into its owner's ledger, where the question itself is written:

- `KNQ-workflow-knowledge-orchestrator-001` — the four open decisions in
  `PROJECT_STATUS.md`, blocked on the human.
- `KNQ-business-analyst-001` — `rollback-deployment` has no workflow step that
  returns into it, blocked on the DM.

## Why the DM owns five areas here

This repository is unusual: the product *is* the framework, so most of it is
process definition, which is the DM's own discipline. Ownership follows the
`assigned_profile` recorded for each work item in
[`../planning/project-plan.yaml`](../planning/project-plan.yaml). In a target
project the distribution looks nothing like this — the Artificer, Ranger, Wizard
and Warlock own the parts of the product they build, and the DM owns only the
index and the planning state.

## Areas with no owner yet

Nine of the fourteen profiles own nothing here, because this repository contains
nothing in their discipline — no user interface, no schema, no external
integration, no deployment target, no analytics. That is recorded honestly as
absence rather than as a token area: the first profile to work on such a part
claims it then, per `claim-ownership`.
