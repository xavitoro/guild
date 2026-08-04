# Prompt 04 — Generate Codex and Claude Code adapters

Read and validate the canonical Guild definitions. The `.guild/` directory must remain the source of truth.

Implement adapter generation or synchronization for:

## Codex

- Root `AGENTS.md` integration without destroying repository-specific instructions.
- Repository skills under `.agents/skills/<skill-name>/SKILL.md`.
- Clear source headers pointing back to canonical Guild files.

## Claude Code

- Root `CLAUDE.md` that imports shared instructions appropriately.
- Project subagents under `.claude/agents/`.
- Project skills under `.claude/skills/<skill-name>/SKILL.md`.
- Optional policy-derived hooks only when deterministic enforcement is appropriate.
- No unrestricted tool permissions by default.

## Generic

- Portable `AGENTS.md`.
- Documentation for clients that support neither native skills nor subagents.

Requirements:

- Do not maintain duplicate canonical definitions manually.
- Provide a deterministic sync/generation command.
- Generated files must carry a warning and source path.
- Add drift detection: validation must fail when generated adapters no longer match canonical inputs.
- Document installation into:
  - an empty repository;
  - an existing repository;
  - a user-level global configuration where supported.
- Add a smoke test demonstrating use with one feature workflow.
- Update planning, memory and status after completion.
