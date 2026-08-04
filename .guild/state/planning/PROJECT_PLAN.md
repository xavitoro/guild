# Guild Project Plan

## Vision

Create a portable framework that gives AI agents consistent roles, workflows, artifacts and safeguards for creating, maintaining and improving software.

## Milestones

1. **M1 — Declarative foundation** (complete)
   - Canonical structure
   - Fourteen profile definitions
   - Skills, workflows and schemas
   - Planning and project-memory conventions

2. **M2 — Provider adapters** (complete)
   - Codex
   - Claude Code
   - Generic `AGENTS.md`

3. **M3 — Evaluation and pilot** (complete)
   - Structural validation
   - Workflow fixtures
   - Installation into a real repository (automated pilot against an
     isolated fresh copy; a genuine external-project pilot remains
     human-owned future work)

4. **M4 — Repository layout hardening** (complete)
   - Split `.guild/` into `core/` (the Guild framework, replaceable
     wholesale on upgrade) and `state/` (this project's own knowledge,
     planning and run history, never touched by an upgrade) — see
     `.guild/state/knowledge/decisions/DEC-001-core-state-split.yaml`
