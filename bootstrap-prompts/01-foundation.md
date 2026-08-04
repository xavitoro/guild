# Prompt 01 — Build the declarative foundation

Read `AGENTS.md`, `.guild/core/spec/GUILD_MASTER_SPEC.md`, `.guild/state/planning/PROJECT_STATUS.md` and the other existing `.guild/` files before changing anything.

Implement **only Phase 1: the declarative Guild foundation**.

Required work:

1. Create the complete canonical `.guild/` directory structure described by the master specification.
2. Create JSON Schemas for:
   - agent manifest;
   - skill manifest;
   - workflow;
   - workflow step;
   - artifact envelope;
   - handoff;
   - gate result;
   - decision;
   - memory proposal;
   - project memory;
   - project plan;
   - project status;
   - run record.
3. Create reusable templates for every major artifact.
4. Add a lightweight validation setup that checks JSON, YAML, JSON Schema validity, unique IDs and broken internal references.
5. Do not generate all fourteen agents yet.
6. Do not generate provider adapters yet.
7. Do not build a UI, SaaS backend, MCP server, agent runtime or cloud infrastructure.
8. Preserve the current planning and memory content, updating their schema references if necessary.
9. Update `PROJECT_STATUS.md` and `project-plan.yaml` when the phase is complete.

Before implementation, briefly state:
- the files you intend to create;
- the validation approach;
- any conservative assumptions.

Then implement the phase, run validation and report:
- files created or changed;
- commands executed;
- validation results;
- unresolved decisions.
