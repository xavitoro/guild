# Guild repository instructions

## Mandatory context

Before planning or modifying this repository, read:

1. `.guild/spec/GUILD_MASTER_SPEC.md`
2. `.guild/planning/PROJECT_STATUS.md`
3. `.guild/planning/project-plan.yaml`
4. `.guild/knowledge/PROJECT_MEMORY.md`
5. `.guild/policies/default-policies.yaml`

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
- Update `.guild/knowledge/` when stable knowledge is verified.
- Update `.guild/planning/` when project scope or status changes.
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

This project has [Guild](.guild/spec/GUILD_MASTER_SPEC.md) installed. `.guild/` is the
canonical source of truth; everything below is generated from it.

- Codex skills: `.agents/skills/<skill-id>/SKILL.md` (22 skills)
- Claude Code subagents: `.claude/agents/<profile-id>.md` (14 profiles)
- Claude Code skills: `.claude/skills/<skill-id>/SKILL.md` (22 skills)
- Generic / single-assistant clients: read `.guild/agents/`, `.guild/skills/` and
  `.guild/workflows/` directly — see `.guild/workflows/EXECUTION_MODES.md` mode 1.

Regenerate after any change under `.guild/agents/` or `.guild/skills/`:

    python3 .guild/adapters/generate_adapters.py --target .

Check for drift (fails if generated files no longer match canonical sources):

    python3 .guild/adapters/generate_adapters.py --target . --check
<!-- guild:adapter:end -->
