# Execution modes

Every workflow in this directory is a declarative graph of steps, each naming a
responsible profile, an invoked skill, its artifacts, preconditions, completion
criteria and gates. That declarative shape is deliberately execution-mode-neutral —
see `GUILD_MASTER_SPEC.md` principle 5, "Progressive autonomy." The same
`workflow.yaml` supports three ways of actually running it:

## 1. One assistant switching roles sequentially

A single AI assistant (e.g. one Claude Code or Codex session) walks the `steps`
array in order. For each step, it adopts the instructions in the responsible
profile's `.guild/agents/<id>/AGENT.md` and manifest, performs the invoked skill,
and checks the step's `completion_criteria` and `gates` before moving to the next
step. Optional steps are skipped when their `condition` does not apply. This mode
needs no tooling beyond reading files and following the sequence.

## 2. Native subagents

An orchestrator (the DM, `workflow-knowledge-orchestrator`) dispatches each step to
a subagent configured with the responsible profile's manifest, running independently
of the orchestrator's own context. This is how QA and security stay structurally
independent from implementation (`GUILD_MASTER_SPEC.md` principle 6): the Barbarian
and Rogue subagents evaluate a change without inheriting the implementing subagent's
reasoning. Handoffs between steps are the `required_input_artifacts` /
`expected_output_artifacts` pairs already declared on each step.

## 3. Future external runtime

An external orchestration system consumes `workflow.yaml` and `workflow-step`
definitions directly, dispatching each step as a job to whichever system (human,
service, agent) owns the named profile, and persists `gate-result` and
`run-record` artifacts per `.guild/schemas/`. No change to the canonical
definitions is required to support this mode — it is the reason the workflow and
step schemas are declarative rather than expressed as code.

## Human approval steps

Steps with `responsible_profile: human` and `invoked_skill: grant-human-approval`
are gates, not agent work: in every execution mode, the workflow blocks at that
step until an explicit approval is recorded, per
`.guild/policies/default-policies.yaml`.
