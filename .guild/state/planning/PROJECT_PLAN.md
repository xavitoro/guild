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

5. **M5 — Distributed ownership and knowledge** (complete)
   - One owning profile per part of the project
   - A knowledge ledger per profile, indexed by the DM as pointers
     — see `.guild/state/knowledge/decisions/DEC-002-distributed-ownership.yaml`

6. **M6 — Nothing stays pending** (complete)
   - Approvals and decisions separated
   - Every decision the roster cannot make becomes a decision request with
     options, a recommendation and a default, presented to a person — see
     `.guild/state/knowledge/decisions/DEC-004-decision-requests.yaml`

7. **M7 — Every question is answerable** (complete)
   - Whatever is left for a person to resolve is asked as enumerated options
     and always carries a free-text answer, so an answer nobody enumerated is
     still an answer rather than silence — see
     `.guild/state/knowledge/decisions/DEC-009-options-plus-free-text.yaml`

