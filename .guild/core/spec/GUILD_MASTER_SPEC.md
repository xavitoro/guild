# Guild Master Specification

## 1. Definition

Guild is a portable, provider-neutral **Agentic SDLC Framework**: a set of agent profiles, skills, protocols, schemas, policies, tools and workflows for creating, maintaining and improving software.

Guild must be usable:

- in ordinary AI conversations;
- inside existing or new repositories;
- from Codex;
- from Claude Code;
- from JetBrains/Junie-compatible environments;
- from future agent clients;
- with or without native multiagent execution.

Guild defines how agents collaborate. It does not own the target project and does not require a specific language, framework, model provider or IDE.

## 2. Design principles

1. **Provider-neutral core** — canonical definitions cannot depend on Codex, Claude or another client.
2. **Language-neutral** — project technology is discovered from the target repository.
3. **Declarative first** — Markdown, YAML and JSON Schema before custom runtime code.
4. **Structured handoffs** — profiles exchange validated artifacts, not free-form roleplay.
5. **Progressive autonomy** — usable by one assistant switching roles, native subagents or an external runtime.
6. **Independent gates** — implementation cannot self-approve QA or security.
7. **Human authority** — destructive and high-impact actions require human approval.
8. **Evidence-based memory** — stable verified facts enter project memory; guesses do not.
9. **Explicit planning** — project state, dependencies and work items are visible in `.guild/state/planning/`.
10. **Portable adapters** — provider-specific files are generated from canonical sources.
11. **Upgradeable core, persistent state** — `.guild/core/` is the Guild framework itself and can be replaced wholesale when Guild improves; `.guild/state/` is a project's own knowledge, planning and run history and is never overwritten by a core upgrade.

## 3. D&D mnemonic roster

The D&D names are aliases for memorability. Technical identifiers remain professional.

| Alias | Canonical profile ID | Professional profile |
|---|---|---|
| DM | `workflow-knowledge-orchestrator` | AI Workflow & Knowledge Orchestrator |
| Paladin | `product-owner` | Product Manager / Product Owner |
| Fighter | `business-analyst` | Business Analyst |
| Druid | `product-experience-designer` | Product Experience Designer |
| Bard | `ux-content-designer` | UX Writer / Content Designer |
| Ranger | `web-experience-engineer` | Web Experience Engineer |
| Artificer | `product-software-engineer` | Product Software Engineer |
| Wizard | `database-engineer` | Database Engineer |
| Warlock | `integration-engineer` | Integration Engineer |
| Barbarian | `quality-assurance-engineer` | Quality Assurance Engineer |
| Rogue | `product-security-engineer` | Product Security Engineer |
| Cleric | `cloud-devops-engineer` | Cloud & DevOps Engineer |
| Sorcerer | `product-data-analyst` | Product Data Analyst |
| Monk | `data-analytics-engineer` | Data & Analytics Engineer |

## 4. Profile responsibilities

### DM — AI Workflow & Knowledge Orchestrator

Coordinates profiles, selects workflows, decomposes work, distributes context, tracks state, consolidates planning and verified knowledge, validates artifact presence, manages handoffs and requests human approval. It validates the process, not the implementation quality or security itself.

### Paladin — Product Manager / Product Owner

Defines vision, outcomes, priority, roadmap and product acceptance. Protects scope and decides which proposed work belongs in the product. Final strategic priority remains human-controlled.

### Fighter — Business Analyst

Transforms goals into actors, functional requirements, business rules, dependencies, edge cases, stories and testable acceptance criteria. Identifies ambiguities without inventing domain facts.

### Druid — Product Experience Designer

Designs user journeys, information architecture, flows, wireframes, screen states, visual hierarchy and interaction specifications. Maintains coherence of the experience.

### Bard — UX Writer / Content Designer

Defines interface language: labels, buttons, help, onboarding, errors, confirmations, empty states and tone. Produces copy tied to concrete states and actions.

### Ranger — Web Experience Engineer

Implements and reviews the web experience, including components, responsive behavior, semantic HTML, accessibility, frontend performance and technical SEO. It does not own core business rules.

### Artificer — Product Software Engineer

Designs and implements complete product functionality and architecture: domain logic, application flows, APIs, code organization and technical decisions. It may implement data and integrations but specialist profiles review complex cases.

### Wizard — Database Engineer

Designs schemas, migrations, constraints, indexes, transactions and queries. Reviews integrity, concurrency, compatibility and data migration risk.

### Warlock — Integration Engineer

Designs and implements external API contracts, authentication with providers, webhooks, idempotency, retries, failure handling and observability for integrations.

### Barbarian — Quality Assurance Engineer

Derives test plans, reviews code, reproduces defects, runs automated and exploratory checks, verifies acceptance criteria and detects regressions. It may reject a change but does not redefine product scope.

### Rogue — Product Security Engineer

Performs threat modeling, architecture and application security review, authorization analysis, secret and dependency review, and risk classification. It remains independent from implementation.

### Cleric — Cloud & DevOps Engineer

Manages CI/CD, environments, infrastructure, deployment, rollback, operational configuration, logs, metrics, traces and alerts. Production-changing actions require applicable approval gates.

### Sorcerer — Product Data Analyst

Interprets product usage, conversion, drop-off, errors and feedback; forms evidence-backed hypotheses and evaluates outcomes. It does not manipulate evidence to justify product priorities.

### Monk — Data & Analytics Engineer

Defines analytics events and properties, implements instrumentation, pipelines, transformations, synchronizations and analytical models, and verifies data quality.

## 5. Core concepts

### Agent profile

A stable responsibility and perspective. Each profile must declare:

- `id`
- `name`
- `alias`
- `mission`
- `responsibilities`
- `non_responsibilities`
- `required_inputs`
- `produced_outputs`
- `allowed_capabilities`
- `forbidden_capabilities`
- `quality_gates`
- `escalation_conditions`

### Skill

A reusable procedure with a narrow goal. A skill is not an identity. Examples:

- discover a project;
- define requirements;
- reproduce a bug;
- design an experience;
- implement a feature;
- review a migration;
- run a regression review;
- create a threat model;
- prepare a pull request.

### Workflow

An ordered or conditional graph that combines profiles and skills. Every step declares:

- responsible profile;
- invoked skill;
- required input artifacts;
- expected output artifacts;
- preconditions;
- completion criteria;
- gates;
- possible return or escalation paths.

### Artifact

A structured handoff object with a schema, version, provenance and status. Human-readable Markdown views may accompany machine-readable YAML or JSON.

### Gate

A deterministic or agent-reviewed condition required to continue. Examples:

- requirements approved;
- tests passed;
- no critical security finding;
- human production approval.

### Tool

An executable capability such as reading files, running tests or creating a branch. Tools are not agent profiles.

## 6. Canonical repository structure

`.guild/` has exactly two top-level directories, separating the Guild framework
from a project's own state so that upgrading Guild never risks a project's
accumulated knowledge, planning or run history (design principle 11):

```text
.guild/
├── core/               # the Guild framework — replaceable wholesale on upgrade
│   ├── spec/
│   ├── agents/
│   ├── skills/
│   ├── workflows/
│   ├── schemas/
│   ├── templates/
│   ├── policies/
│   ├── adapters/
│   └── evals/
└── state/              # this project's own data — never touched by an upgrade
    ├── knowledge/
    ├── planning/
    ├── runs/
    └── project.yaml
```

Upgrading Guild means replacing `.guild/core/` with a newer version and
re-running the adapter generator; `.guild/state/` is left exactly as it was.
Installing Guild into a new project means copying only `.guild/core/`; the
target's own `.guild/state/` is populated by running the
`onboard-existing-project` or `create-new-project` workflow, not by copying
another project's state.

Provider-specific generated files may exist outside `.guild/`:

```text
AGENTS.md
CLAUDE.md
.agents/skills/
.claude/agents/
.claude/skills/
```

## 7. Project knowledge

The knowledge system distinguishes:

- canonical verified memory;
- accepted decisions;
- unverified discoveries;
- reusable project patterns;
- archived or superseded information;
- per-run execution history.

Canonical files:

```text
.guild/state/knowledge/project-memory.yaml
.guild/state/knowledge/PROJECT_MEMORY.md
.guild/state/knowledge/decisions/
.guild/state/knowledge/discoveries/
.guild/state/knowledge/patterns/
.guild/state/knowledge/archive/
```

Only the DM consolidates canonical memory. Other profiles submit evidence-backed proposals.

Do not store:

- private chain-of-thought;
- temporary logs as permanent knowledge;
- unsupported opinions;
- facts copied from another project without verification;
- secrets or personal sensitive data.

## 8. Project planning

Planning is defined primarily by the DM, Paladin and Fighter.

- Paladin: vision, outcomes, priorities and milestones.
- Fighter: initiatives, work items, requirements and acceptance criteria.
- DM: dependencies, state, workflow links, evidence and status views.

Canonical files:

```text
.guild/state/planning/project-plan.yaml
.guild/state/planning/PROJECT_PLAN.md
.guild/state/planning/PROJECT_STATUS.md
.guild/state/planning/roadmap.yaml
.guild/state/planning/milestones/
.guild/state/planning/backlog/
.guild/state/planning/archive/
```

Common states:

- `proposed`
- `planned`
- `ready`
- `in_progress`
- `blocked`
- `in_review`
- `completed`
- `cancelled`

Progress must be calculated from completed weighted work, not guessed by agents.

Planning hierarchy:

```text
Vision
→ Objectives
→ Milestones
→ Initiatives
→ Work items
→ Workflow runs
→ Workflow steps
```

## 9. Initial workflows

The first release must define:

1. `onboard-existing-project`
2. `create-new-project`
3. `add-feature`
4. `fix-bug`
5. `improve-product`
6. `review-pull-request`

All workflows must be usable in:

- single-assistant sequential mode;
- native subagent mode;
- future external runtime mode.

### Example: fix bug

```text
Intake by DM
→ reproduction by Barbarian
→ root-cause and plan by Artificer
→ specialist review when needed
→ implementation by Artificer/Ranger/Wizard/Warlock
→ regression validation by Barbarian
→ conditional review by Rogue
→ handoff or pull request preparation by DM
```

## 10. Required schemas

Create JSON Schemas for at least:

- agent manifest;
- skill manifest;
- workflow definition;
- workflow step;
- task/work item;
- handoff;
- artifact envelope;
- gate result;
- decision record;
- memory proposal;
- project memory;
- project plan;
- project status;
- run record.

Every artifact envelope should contain:

- `schema`
- `id`
- `type`
- `version`
- `status`
- `project`
- `created_at`
- `created_by`
- `source_artifacts`
- `evidence`
- `content`

## 11. Permissions and human approval

Default capability levels:

### Green

- read repository;
- inspect documentation;
- search code;
- create plans and artifacts;
- run non-destructive checks;
- work in an isolated sandbox.

### Amber

- edit code in a branch;
- add a dependency;
- create a migration;
- modify CI;
- create a pull request;
- run changes in an ephemeral environment.

These require independent review before acceptance.

### Red

Explicit human approval is required for:

- merging protected branches;
- production deployments;
- destructive migrations;
- deleting or modifying production data;
- credentials and secrets;
- permission changes;
- payment or billing behavior;
- external communications;
- infrastructure actions with material cost or blast radius.

## 12. Adapter model

Canonical Guild sources must generate provider-specific files.

### Codex

- root and nested `AGENTS.md` instructions;
- repository skills under `.agents/skills/<skill>/SKILL.md`;
- optional Codex-specific metadata that does not alter canonical meaning.

### Claude Code

- `CLAUDE.md`, importing shared root instructions where appropriate;
- project subagents under `.claude/agents/`;
- project skills under `.claude/skills/<skill>/SKILL.md`;
- optional hooks and settings generated from explicit policies.

### Generic

- a portable `AGENTS.md`;
- canonical skills and workflows readable as Markdown/YAML;
- no assumption of native subagents.

Adapters must be generated or synchronized. Do not hand-maintain diverging copies.

## 13. Initial implementation boundaries

The first implementation must not include:

- a SaaS dashboard;
- a central database;
- a custom multiagent runtime;
- mandatory MCP or ACP servers;
- cloud deployment;
- automatic production access;
- language-specific project generators.

The first implementation must include:

- complete declarative specification;
- 14 profile definitions;
- initial skills;
- six workflows;
- schemas and validation;
- planning and memory templates;
- provider adapters;
- structural tests/evaluations;
- documentation showing how to install Guild into a target repository.

## 14. Definition of done for the declarative foundation

The foundation is complete when:

1. Every profile has a validated manifest and human-readable instructions.
2. Every initial workflow references existing profiles, skills and schemas.
3. Every workflow has failure, return and escalation paths.
4. Planning and memory files validate against schemas.
5. Codex and Claude adapter output can be regenerated.
6. No canonical definition requires a particular language or vendor.
7. Independent QA and security gates are preserved.
8. A fresh target repository can install the generated files using documented steps.
9. A human can understand the current Guild planning state from `PROJECT_STATUS.md`.
10. Automated checks detect broken references, invalid YAML/JSON and duplicate IDs.
