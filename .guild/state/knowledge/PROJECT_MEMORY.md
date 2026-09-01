# Project Memory

## Product

- Guild is a portable, provider-neutral Agentic SDLC framework.
- It coordinates software work through profiles, skills, workflows, artifacts, gates and policies.
- It must work in conversations, repositories and different agent clients.

## Architecture

- `.guild/core/` is the canonical provider-neutral Guild framework (replaceable
  wholesale on upgrade); `.guild/state/` is this project's own knowledge,
  planning and run history (never touched by an upgrade) — see DEC-001.
- The first implementation is declarative.
- Codex and Claude files are adapters generated from canonical definitions.
- QA and security remain independent from implementation.
- WI-001 is complete: 16 JSON Schemas live under `.guild/core/schemas/`, artifact
  templates under `.guild/core/templates/`, and `.guild/core/evals/validate_guild.py`
  validates syntax, schema conformance, id uniqueness and `depends_on`
  references across the whole `.guild/` tree.
- WI-002 is complete: all fourteen agent profiles exist under
  `.guild/core/agents/<id>/` (manifest + `AGENT.md`), independent QA (Barbarian)
  and security (Rogue) gates are preserved, and no profile has unrestricted
  write/merge/deploy/secret access. `.guild/core/evals/check_agent_profiles.py`
  proves the roster is complete, schema-valid and unique.
- WI-003 is complete, closing milestone M1: 22 reusable skills under
  `.guild/core/skills/`, all six canonical workflows under `.guild/core/workflows/`
  (with conditional db/integration/web/security/cloud/data branches and
  explicit human-approval steps for Red-tier actions), and two example run
  records under `.guild/state/runs/`. `.guild/core/evals/check_workflow_refs.py` proves
  every profile/skill/workflow/run cross-reference resolves.
- WI-004 is complete, closing milestone M2: `.guild/core/adapters/generate_adapters.py`
  deterministically derives Codex skills (`.agents/skills/`), Claude Code
  subagents (`.claude/agents/`, tool grants mechanically derived from
  `allowed_capabilities`, never unrestricted) and skills (`.claude/skills/`),
  one policy-derived `.claude/settings.json` deny rule, and managed sections
  appended (not overwriting) root `AGENTS.md`/`CLAUDE.md`. `--check` gives
  drift detection. `.guild/core/evals/smoke_test_add_feature.py` proves full
  adapter coverage for the `add-feature` workflow.
- WI-005 is complete, closing milestone M3. No dedicated prompt existed for
  it; scope was derived from `GUILD_MASTER_SPEC.md` section 14's
  definition of done. Added `check_independent_gates.py` (structural
  QA/security independence + Red gates owned by `human`),
  `check_language_neutrality.py` (deny-list scan), and
  `pilot_install_check.py` (installs an isolated copy of the framework into
  a fresh temp directory and re-runs every check from there — a real,
  automated fresh-install pilot). A genuine external-project pilot remains
  human-owned future work.
- WI-006 is complete, closing milestone M4 and the full M1–M4 bootstrap
  roadmap: `.guild/` now has exactly two top-level directories,
  `core/` (the framework, replaceable wholesale) and `state/` (this
  project's own data, never touched by an upgrade). See
  `.guild/state/knowledge/decisions/DEC-001-core-state-split.yaml`.
  `pilot_install_check.py` was corrected to copy only `.guild/core/` into
  its isolated target.
- No workflow asked whether a project needs an isolated component catalog
  for UI components. Added the provider-neutral `maintain-component-catalog`
  skill (Ranger) and an optional step invoking it in `create-new-project`
  and `add-feature`.
- The D&D roster existed but was barely used: every surface a human reads
  named profiles by canonical id only. `GUILD_MASTER_SPEC.md` section 3.1
  now makes the alias the human-facing name and the canonical id the machine
  name, section 11 defines the approval-request format (who is asking, who
  is blocked, evidence, effect of approving and of rejecting), and aliases
  are rendered across workflow diagrams and tables, skill and profile docs,
  escalation prose and every generated adapter.
  `check_alias_presence.py` enforces both directions.
- Profiles had no declared ownership of any part of a project and all
  knowledge converged on one consolidated memory, so a profile started each
  step without a boundary or accumulated knowledge of its own, and the DM had
  to hold everything to coordinate. Every part is now an ownership area with
  exactly one owner in `.guild/state/knowledge/ownership.yaml`; each owner
  claims its area before working and appends what it verified, with evidence,
  to its own ledger under `.guild/state/knowledge/profiles/`. The DM keeps
  pointers only — area, owner, ledger, newest entry, open questions, related
  areas — and connects owners rather than merging their knowledge. See DEC-002
  and `check_ownership_model.py`.
- Open questions had no obligation to reach a person: the status file carried
  four open decisions as bullet sentences with no owner, options or default. A
  decision no profile can make from the project itself is now a decision request
  under `.guild/state/planning/decisions/` — what it blocks, options with
  consequences, a recommendation, and the default that applies if nobody answers
  — presented to a person and listed by id in `PROJECT_STATUS.md`. A default
  never applies before it has been shown, deferral is an explicit answer, and
  Red-tier actions stay approvals that block outright. See DEC-004 and
  `check_human_in_the_loop.py`.

## Decisions

- "Guild" is the public product and protocol name (DEC-005).
- Published under MIT, as `LICENSE` already stated; no explicit patent grant
  (DEC-006).
- Adapters are generated in the target at install time, never shipped
  pre-generated — this is what makes drift detection meaningful (DEC-007).
- The first public release is definitions plus the adapter generator, with no
  CLI (DEC-008).
- Each decision keeps the revisit trigger its request declared; none is pending,
  none is sealed.

## Current constraints

- Do not build a SaaS platform yet.
- Do not require a specific programming language.
- Do not grant production access automatically.
