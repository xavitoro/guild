# Adapters

Provider-specific files generated from the canonical `.guild/agents/` and
`.guild/skills/` definitions. `.guild/` remains the source of truth —
nothing under `.agents/`, `.claude/`, or the generated sections of root
`AGENTS.md`/`CLAUDE.md` is hand-maintained.

## The generator

[`generate_adapters.py`](generate_adapters.py) is the deterministic
sync/generation command. It reads every `.guild/agents/*/manifest.yaml` and
`.guild/skills/*/SKILL.yaml`, and produces:

| Output | Client | Content |
|---|---|---|
| `.agents/skills/<skill-id>/SKILL.md` | Codex | One file per canonical skill |
| `.claude/agents/<profile-id>.md` | Claude Code | One subagent per canonical profile |
| `.claude/skills/<skill-id>/SKILL.md` | Claude Code | One skill per canonical skill |
| `.claude/settings.json` | Claude Code | One deterministic, policy-derived `permissions.deny` rule |
| A managed block in root `AGENTS.md` | Codex / generic | Appended, existing content untouched |
| A managed block in root `CLAUDE.md` | Claude Code | Appended, existing content untouched |

Every generated file carries a `GENERATED FILE — DO NOT EDIT BY HAND` header
naming its canonical source. Generic clients that support neither native
skills nor subagents read `.guild/agents/`, `.guild/skills/` and
`.guild/workflows/` directly — see
[`../workflows/EXECUTION_MODES.md`](../workflows/EXECUTION_MODES.md) mode 1.

## Commands

Regenerate (safe to run any time; writes only what changed, and removes any
generated file whose canonical id no longer exists):

```
python3 .guild/adapters/generate_adapters.py --target .
```

Check for drift without writing anything (fails if a generated file no
longer matches its canonical source, if a canonical addition hasn't been
generated yet, or if a generated file was hand-edited):

```
python3 .guild/adapters/generate_adapters.py --target . --check
```

Run this as part of `.guild/evals/` validation — see
[`../evals/README.md`](../evals/README.md).

## Tool permissions

Claude Code subagent `tools:` lists are derived mechanically from each
profile's `allowed_capabilities` (see `CAP_TOOLS` in
`generate_adapters.py`). No profile is ever granted unrestricted tool
access; profiles that cannot edit product code (e.g. `quality-assurance-engineer`,
`product-security-engineer`) mechanically receive no `Edit`/`Write` grant.

## Policy-derived hooks

`.claude/settings.json` gets exactly one generated `permissions.deny` rule:
blocking `git push --force`/`-f`. This is the one Red-tier action from
`.guild/policies/default-policies.yaml` (`merge_protected_branch`, in
spirit) that can be matched deterministically from a shell command
regardless of the target repository's language, branch names or deploy
tooling. The rest of the Red-tier list (`deploy_production`,
`modify_production_data`, `access_or_change_secrets`, ...) cannot be
reliably pattern-matched without guessing project-specific tooling, so they
stay enforced by the explicit `grant-human-approval` workflow steps instead
(see `.guild/workflows/`).

## Installation

See [`INSTALL.md`](INSTALL.md).
