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
12. **Distributed ownership, indexed coordination** — every part of a project has exactly one owning profile, which accumulates that part's knowledge in its own ledger. The orchestrator holds an index of who owns what and where their knowledge lives, not the knowledge itself: it connects pieces by pointer, and is never the bottleneck that must know everything.
13. **Nothing stays pending** — a decision no profile can make from the project itself is put to a person, with options, a recommendation and a stated default; it is never resolved by assumption, never applied as a silent default, and never left as an unanswered note. Deferring is an answer a person gives, not something that happens by itself.

## 3. D&D mnemonic roster

Every profile has two names. The D&D alias is the name a person sees and uses; the
canonical profile ID is the name machines use. Both always exist and neither replaces
the other — see section 3.1.

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

### 3.1 Aliases are the human-facing name

The alias is how a profile introduces itself to a person. The canonical ID is how it is
referenced by machines. The two surfaces are strictly separated:

| Surface | Uses |
|---|---|
| Anything a human reads or answers — approval requests, escalations, questions, role announcements, handoff summaries, status reports, workflow diagrams and tables, profile and skill documentation | The alias, first: `Barbarian (quality-assurance-engineer)` on first mention in an exchange or document, plain `Barbarian` afterwards |
| Anything a machine reads — schema fields, `responsible_profile`, `applicable_profiles`, `assigned_profile`, directory and file names, gate and policy keys | The canonical ID only |

Rules:

1. Every message addressed to a human names the alias of the profile that produced it.
2. Every request for a human decision names the alias that is asking and the alias whose
   work is blocked on the answer (section 11, "Approval request format").
3. Every role switch in single-assistant execution is announced by alias before that
   step's work begins — see `workflows/EXECUTION_MODES.md`.
4. An alias is always rendered from the `alias` field of the profile manifest. It is never
   stored as a second identity field in an artifact, and never used as a key, path
   segment or reference.
5. `human` is not a profile and has no alias. It is written as "the human".

A human-facing message that names only a canonical ID is incomplete, and so is an artifact
field that carries an alias instead of an ID.

## 4. Profile responsibilities

### DM — AI Workflow & Knowledge Orchestrator

Coordinates profiles, selects workflows, decomposes work, distributes context, tracks state, consolidates planning and verified knowledge, validates artifact presence, manages handoffs and requests human approval. It validates the process, not the implementation quality or security itself.

It also maintains the ownership map (section 7.1) — the index of which profile owns which part of the project and where that owner's knowledge lives. The DM routes by that index: it needs to know who owns a part and where their ledger is, not what the ledger says.

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

### Ownership area

A named part of the target project with exactly one owning profile: a boundary
saying what is inside it and what is not, the concrete paths it covers, and a
pointer to the owner's knowledge ledger. Areas are recorded in the project's
ownership map (section 7.1). Ownership is claimed explicitly before work starts,
not inferred from who happened to touch a file.

### Knowledge ledger

One profile's own accumulated knowledge about the areas it owns, appended as it
works and as interactions teach it something. A ledger is written by its owner
and read by anyone. It is the working layer beneath canonical project memory:
entries start as one profile's evidence-backed observation and only become
canonical memory when the orchestrator consolidates them (section 7.4).

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
    │   ├── ownership.yaml      # who owns what, and where their knowledge lives
    │   ├── profiles/           # one knowledge ledger per owning profile
    │   ├── project-memory.yaml # consolidated, canonical memory
    │   ├── decisions/
    │   ├── discoveries/
    │   ├── patterns/
    │   └── archive/
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
.guild/state/knowledge/ownership.yaml
.guild/state/knowledge/OWNERSHIP.md
.guild/state/knowledge/profiles/<profile-id>.yaml
.guild/state/knowledge/project-memory.yaml
.guild/state/knowledge/PROJECT_MEMORY.md
.guild/state/knowledge/decisions/
.guild/state/knowledge/discoveries/
.guild/state/knowledge/patterns/
.guild/state/knowledge/archive/
```

Only the DM consolidates canonical memory. Other profiles submit evidence-backed proposals.

### 7.1 Ownership: every part has exactly one owner

Knowledge is not a shared pool that every profile dips into. Each part of the
project is an **ownership area** with exactly one owning profile, recorded in
`.guild/state/knowledge/ownership.yaml` (schema `guild.ownership-map/v1`).

A profile takes ownership **before** it does the work, not after:

1. At the start of its part, the responsible profile claims the area it is about
   to work in — an existing area it already owns, or a new one it proposes.
2. It records the claim in its own ledger's `owned_areas`, then hands the DM the
   claim.
3. The DM records the area in the ownership map: boundary, owner, ledger path,
   `claimed_at`, and the related areas whose owners this owner must coordinate
   with.

Rules:

- Exactly one `owner_profile` per area. Two profiles working the same part is a
  boundary error, resolved by splitting the area or reassigning it — never by
  co-ownership.
- A profile that finds work outside its boundary does not silently absorb it. It
  raises an open question naming the owning area, or asks the DM to route it.
- Ownership does not override the independence rules: the Barbarian
  (`quality-assurance-engineer`) and the Rogue (`product-security-engineer`) own
  their own areas and still evaluate everyone else's — owning an area never means
  approving your own QA or security result (principle 6).
- Only the DM writes the ownership map. It is the index, not a workspace.

### 7.2 Per-profile knowledge ledgers

Each owning profile accumulates what it learns in its own ledger,
`.guild/state/knowledge/profiles/<profile-id>.yaml` (schema
`guild.profile-knowledge/v1`), appended as it works.

- A profile writes **only** its own ledger. No profile edits another's, and the
  DM does not rewrite ledger content — it maintains the index over them.
- An entry records what an interaction actually verified, with evidence anyone
  can check, phrased so another profile could act on it without re-deriving it.
- Entry ids carry their owner: `KN-<profile-id>-<sequence>`. A misfiled entry is
  therefore detectable, not merely discouraged.
- What a profile could not resolve inside its boundary becomes an
  `open_questions` entry (`KNQ-<profile-id>-<sequence>`), optionally
  `blocked_on` another profile or the human — this is how a gap leaves the owner
  and reaches the DM without the DM having to notice it.
- The exclusions in this section apply to ledgers exactly as they do to canonical
  memory: no private chain-of-thought, no temporary logs, no unsupported
  opinions, no secrets.

Each step ends with either a ledger entry or an explicit "nothing new was
verified". Silence is not a valid step exit — it is indistinguishable from an
owner that stopped paying attention.

### 7.3 The DM connects pieces without holding them

The DM routes by **pointer**, not by omniscience. To act on any part of the
project it needs the ownership map alone: area → owner → ledger path → newest
entry id → open questions → related areas. It follows a pointer into a ledger
when a specific decision requires that detail, and otherwise routes the question
to the owner.

- The ownership map holds pointers only. It has no field that can hold a
  knowledge statement, by construction of its schema — copying an owner's
  finding into the index is what turns an index back into a bottleneck.
- Handoffs carry `knowledge_refs` — ids of ledger entries and open questions the
  receiving profile should read (`guild.handoff/v1`) — rather than restating what
  the sending profile knows.
- When two areas interact, the DM connects their **owners**, using
  `related_areas`; it does not attempt to merge their knowledge itself.
- Consequently the DM's context stays bounded as the project grows: what grows is
  the number of areas in the index, not the amount of knowledge the DM must hold.

### 7.4 From ledger entry to canonical memory

The layers are ordered, and only the last one is canonical:

```text
interaction
→ ledger entry (owner, evidence-backed)
→ memory proposal (owner submits)
→ project-memory entry (DM consolidates)
```

A ledger entry that has proved stable and matters beyond its own area is promoted
by its owner as a `guild.memory-proposal/v1`; the DM accepts or rejects it and,
on acceptance, sets `promoted_to` on the ledger entry so both layers stay linked.
Ledger knowledge that is only useful inside its own area stays in the ledger —
canonical memory is deliberately small.

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
.guild/state/planning/decisions/
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
- ownership map;
- profile knowledge ledger;
- decision request;
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

### Approval request format

A Red-tier action reaches the human as an explicit request, never as a silent block. The DM
presents it; the human answers it. Per section 3.1, the request identifies profiles by
alias. It must state:

1. **Who is asking** — the DM, and the profile whose work is blocked, by alias and
   canonical ID.
2. **What action** — the Red-tier key from `policies/default-policies.yaml` plus the
   concrete action in the target project's own terms.
3. **What evidence backs it** — the gate results already recorded and by whom (the
   Barbarian's QA gate, the Rogue's security gate), and the artifacts under review.
4. **What approving causes, and what rejecting causes.**

Canonical shape of the rendered request (the recorded artifact remains a `gate-result`,
which stores canonical IDs, not aliases):

    Guild approval required — merge_protected_branch
    Asked by      DM (workflow-knowledge-orchestrator)
    On behalf of  Artificer (product-software-engineer)
    Action        Merge the change into the protected mainline branch
    Evidence      Barbarian — qa_gate_pass: pass
                  Rogue — security_gate_clean: pass
    On approve    The Artificer's change merges; any deployment still needs the
                  separate deploy_production approval before the Cleric proceeds.
    On reject     The workflow stops at this step and the DM records the rejection.
    Your answer   approve / reject / request changes

A request that does not name the asking and blocked profiles is incomplete: the human
returns it to the DM rather than answering it. The same shape applies to any non-gated
question put to the human — it names the alias asking and what the answer unblocks.

### 11.1 Approvals and decisions are different things

| | Approval | Decision request |
|---|---|---|
| Trigger | A Red-tier action from `policies/default-policies.yaml` | A question no profile can answer from the project itself: scope, naming, licensing, priority, an ambiguity nobody owns |
| Artifact | `guild.gate-result/v1` | `guild.decision-request/v1`, and the `guild.decision/v1` record its answer produces |
| If the human does not answer | The work stops. There is no default, ever. | The stated default applies from the stated moment, and the question comes back |
| Who may answer | The human only | The human, or whoever the human delegates it to on the record |

Conflating them is what produces both failure modes: a Red-tier action quietly
proceeding on a default, and an ordinary decision blocking a project forever because
nobody was ever actually asked.

### 11.2 Nothing stays pending

A profile that cannot decide something inside its own boundary raises an open question
in its ledger (section 7.2). If that question is `blocked_on: human`, it does not stay
there:

1. The DM turns it into a decision request in `.guild/state/planning/decisions/`.
2. The request states the question in the project's own terms, what it blocks, at least
   two options with their consequences, the asking profile's **recommendation**, and the
   **default that applies if nobody answers** — with when that default takes effect and
   what brings the question back.
3. The DM presents it to the human, by alias, in the format below, and marks it
   `presented`.
4. The human answers, or explicitly defers. A deferral is recorded as an answer, with
   the default now in force; silence is not a deferral.
5. An answer becomes a decision record, linked both ways
   (`resolves_decision_request` / `resulting_decision`), and the request leaves
   `open_decisions` in the project status.

Rules:

- **A default never applies before the human has been shown it.** Applying an unshown
  default is indistinguishable from a profile deciding by assumption.
- **Every open decision appears by id in `PROJECT_STATUS.md`**, so the pending set is
  something a person can read in one place rather than something scattered across
  ledgers.
- **A workflow run does not close with a decision it needed left unpresented.** The DM
  sweeps open questions before consolidating a run.
- **A decision request with no recommendation is incomplete** — it pushes the analysis
  back onto the person it is asking.
- **Red-tier actions are never decision requests.** They block, per section 11.

Canonical shape of the rendered request:

    Guild decision required — DR-004
    Asked by       DM (workflow-knowledge-orchestrator)
    On behalf of   Artificer (product-software-engineer)
    Question       Does the first public release include a command-line interface?
    Blocks         WI-009, and the Artificer's packaging work
    Options        A  Ship the CLI now       → one more surface to support and document
                   B  Generated files only   → installation stays a copy-and-run step
    Recommendation B, because the generator already covers installation and a CLI
                   adds a maintained surface before anyone has asked for one.
    If unanswered  B applies from the first public release, and the DM asks again the
                   first time a user reports the copy-and-run step as a problem.
    Your answer    A / B / defer / other

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
11. Every human-facing surface names the profile it comes from by alias (section 3.1).
12. Every part of a project has exactly one owning profile, each owner accumulates
    its own evidence-backed knowledge, and the orchestrator can route to any part
    of it from the ownership map alone (section 7.1-7.3).
13. No decision is left pending without an owner, a stated default and a person
    actually asked: every open question blocked on the human is a decision request
    with options, a recommendation and a default, listed by id in the project
    status (section 11.2).
