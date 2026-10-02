# Guild repository instructions

## Mandatory context

Before planning or modifying this repository, read:

1. `.guild/core/spec/GUILD_MASTER_SPEC.md`
2. `.guild/state/planning/PROJECT_STATUS.md`
3. `.guild/state/planning/project-plan.yaml`
4. `.guild/state/knowledge/PROJECT_MEMORY.md`
5. `.guild/state/knowledge/OWNERSHIP.md` — who owns which part of this
   repository, and where each owner's knowledge ledger lives
6. `.guild/core/policies/default-policies.yaml`

## Repository purpose

This repository defines a provider-neutral Agentic SDLC framework composed of:

- agent profiles;
- reusable skills;
- workflows;
- handoff and artifact contracts;
- planning and project-memory conventions;
- policies and human approval gates;
- adapters for Codex, Claude Code and generic agents.

It is not initially a SaaS product, IDE, autonomous coding runtime or language-specific framework.

## Working rules

- Keep the canonical definitions provider-neutral.
- Do not introduce assumptions about a particular programming language or framework.
- Generated Codex and Claude files must derive from canonical Guild sources.
- Do not duplicate canonical content manually across adapters.
- Prefer Markdown, YAML and JSON Schema.
- Validate all YAML and JSON Schema files after changes.
- Keep agents, skills, workflows and tools as separate concepts.
- Every workflow step must declare its inputs, outputs, responsible profile and gates.
- Never let an implementation profile approve its own QA or security result.
- Destructive, production, credential, payment and permission changes require explicit human approval.
- Claim the area you are about to work in before changing it, and record what
  the change verified in that area's owner ledger under
  `.guild/state/knowledge/profiles/`.
- Update `.guild/state/knowledge/` when stable knowledge is verified.
- Update `.guild/state/planning/` when project scope or status changes.
- Do not record private chain-of-thought or unverified opinions as project memory.

## Change protocol

Before implementation:

1. State the requested phase and deliverables.
2. Inspect existing files and avoid overwriting approved content.
3. List material ambiguities; use conservative defaults when they do not block progress.
4. Make changes in a coherent batch.
5. Run structural validation.
6. Summarize created or changed files, validation results and open decisions.

<!-- guild:adapter:start -->
## Guild adapter (generated — do not edit this section by hand)

This project has [Guild](.guild/core/spec/GUILD_MASTER_SPEC.md) installed. `.guild/core/`
is the canonical source of truth; everything below is generated from it. This project's
own knowledge, planning and run history live in `.guild/state/`, untouched by Guild
upgrades.

- Codex skills: `.agents/skills/<skill-id>/SKILL.md` (27 skills)
- Claude Code subagents: `.claude/agents/<profile-id>.md` (14 profiles)
- Claude Code skills: `.claude/skills/<skill-id>/SKILL.md` (27 skills)
- Generic / single-assistant clients: read `.guild/core/agents/`, `.guild/core/skills/`
  and `.guild/core/workflows/` directly — see
  `.guild/core/workflows/EXECUTION_MODES.md` mode 1.

### Addressing the human

Each profile has a human-facing alias and a canonical id. Anything a person reads names
the profile by alias — Artificer, Barbarian, Bard, Cleric, DM, Druid, Fighter, Monk,
Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard — with the canonical id in parentheses
on first mention ("Barbarian (quality-assurance-engineer)"). Artifact fields
(`responsible_profile`, `evaluated_by`, `requested_by`, ...) keep canonical ids only. In
single-assistant mode, announce every role switch by alias before starting that step's
work. Red-tier actions reach the human as an approval request naming who is asking and
who is blocked — see `.guild/core/spec/GUILD_MASTER_SPEC.md` sections 3.1 and 11.

### Languages

Guild uses three human languages in a project, each chosen by the human and recorded
under `languages` in `.guild/state/project.yaml`: `conversation` for whatever a profile
says to a person, `state_prose` for the prose written into `.guild/state/`, and `git`
for commit messages, pull requests and review comments. The orchestrator asks for all
three, as options plus free text, before any other question in the triage of
`onboard-existing-project` and `create-new-project` — and at the next triage of any
project that has none recorded. No profile picks or infers a language. Ids, aliases,
keys, schema fields, file names, recorded answer keys and quoted evidence are never
translated, and `.guild/core/` stays as it is. See
`.guild/core/spec/GUILD_MASTER_SPEC.md` section 3.2.

### Ownership and knowledge

Every part of the project has exactly one owning profile. A profile claims its area
before working (`claim-ownership`) and appends what each interaction verified to its own
ledger at `.guild/state/knowledge/profiles/<profile-id>.yaml` afterwards
(`record-profile-knowledge`) — with evidence, never private reasoning. A profile writes
only its own ledger. The orchestrator maintains `.guild/state/knowledge/ownership.yaml`,
an index of area, owner, ledger location, newest entry and related areas: it routes by
those pointers instead of holding what every owner knows. Handoffs carry ledger entry
ids, not copies. See `.guild/core/spec/GUILD_MASTER_SPEC.md` section 7.

### Pending decisions

A decision no profile can make from the project itself — scope, naming, licensing, an
ambiguity nobody owns — is never resolved by assumption and never left as a note. It
becomes a decision request in `.guild/state/planning/decisions/` stating what it blocks,
at least two options with consequences, a recommendation, and the default that applies
if nobody answers; the orchestrator presents it to a person and records the answer, or
an explicit deferral. A default never applies before the human has been shown it, every
open decision is listed by id in `PROJECT_STATUS.md`, and no run closes with a decision
it needed left unasked. Red-tier actions are approvals, not decision requests: they
block outright and never carry a default. Whatever reaches a person is asked as
enumerated options and always offers an answer in their own words — the options were
written by the profile that could not decide, so they are never the limit of what may be
answered; a free-text answer is recorded verbatim, and on an approval it never counts as
approval. See `.guild/core/spec/GUILD_MASTER_SPEC.md` sections 11.2 and 11.3.

### Found work

A change a profile finds while doing something else — a duplicated helper, a missing
test, a definition that drifted — and which blocks nothing is never a `TODO` comment, a
ledger note or a line in a summary. Before the step closes it becomes a work item in
`.guild/state/planning/project-plan.yaml` with `kind: technical_debt`, an id in the
`TD-` series, an `origin` naming who found it, where, and the evidence, and
`assigned_profile` set to the owner of the area it was found in. It is recorded
unscheduled — `status: proposed`, no milestone — because recording found work never
commits the project to doing it and never enlarges the current step; only the product
owner schedules it, and unscheduled debt is excluded from milestone progress. Every open
item is listed by id in `PROJECT_STATUS.md`, and no run closes with found work left
unrecorded. Work that *blocks* the step is not debt: it is part of the task, an
escalation to the area's owner, or a decision request. See
`.guild/core/spec/GUILD_MASTER_SPEC.md` section 8.1.

Regenerate after any change under `.guild/core/agents/` or `.guild/core/skills/`:

    python3 .guild/core/adapters/generate_adapters.py --target .

Check for drift (fails if generated files no longer match canonical sources):

    python3 .guild/core/adapters/generate_adapters.py --target . --check
<!-- guild:adapter:end -->
