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

## Current constraints

- Do not build a SaaS platform yet.
- Do not require a specific programming language.
- Do not grant production access automatically.
