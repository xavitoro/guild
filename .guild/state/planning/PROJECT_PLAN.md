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

8. **M8 — Nothing found is dropped** (complete)
   - A change a profile finds while doing something else, which blocks nothing
     and which it is not going to make, becomes a technical-debt work item in
     `project-plan.yaml` — with an origin, evidence and the owner of the area it
     was found in — instead of a `TODO` comment or a line in a summary
   - Found work is recorded unscheduled and stays out of milestone progress until
     the Paladin (`product-owner`) gives it a milestone, so recording something
     never commits the project to doing it — see
     `.guild/state/knowledge/decisions/DEC-010-found-work-becomes-a-task.yaml`

## Found work

Technical-debt items live in `project-plan.yaml` beside the planned work items,
with `kind: technical_debt` and ids in the `TD-` series. They carry no milestone
until they are scheduled, which is why they do not distort weighted milestone
progress. The open ones are listed in
[`PROJECT_STATUS.md`](PROJECT_STATUS.md#open-technical-debt).
