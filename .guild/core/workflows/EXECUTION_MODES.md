# Execution modes

Every workflow in this directory is a declarative graph of steps, each naming a
responsible profile, an invoked skill, its artifacts, preconditions, completion
criteria and gates. That declarative shape is deliberately execution-mode-neutral —
see `GUILD_MASTER_SPEC.md` principle 5, "Progressive autonomy." The same
`workflow.yaml` supports three ways of actually running it:

## 1. One assistant switching roles sequentially

A single AI assistant (e.g. one Claude Code or Codex session) walks the `steps`
array in order. For each step, it adopts the instructions in the responsible
profile's `.guild/core/agents/<id>/AGENT.md` and manifest, performs the invoked skill,
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
`run-record` artifacts per `.guild/core/schemas/`. No change to the canonical
definitions is required to support this mode — it is the reason the workflow and
step schemas are declarative rather than expressed as code.

## Ownership and knowledge in each mode

Every workflow declares a `step_protocol`: each step is bracketed by
`claim-ownership` before its own work and `record-profile-knowledge` after it
(`GUILD_MASTER_SPEC.md` section 7). It is declared once per workflow rather than
as extra steps precisely so it survives every execution mode:

- **Mode 1** — the single assistant claims the area at each role switch, works as
  that profile, then appends what the step verified to *that profile's* ledger
  before switching again. The ledgers are what stop one assistant's roles from
  collapsing into one undifferentiated memory: the Barbarian's ledger holds what
  QA verified, not what the Artificer assumed while implementing.
- **Mode 2** — each subagent claims its area, reads its own ledger for that area
  as its starting context, and returns ledger entry ids to the DM. This is what
  keeps the DM's own context bounded: a subagent hands back pointers, so the
  orchestrator never has to absorb every subagent's reasoning to coordinate the
  next step.
- **Mode 3** — the runtime enforces the same bracket around each dispatched job,
  and persists ownership-map and ledger updates alongside `gate-result` and
  `run-record` artifacts per `.guild/core/schemas/`.

In all three, the ownership map is the only thing the orchestrator needs to route
any part of the project to its owner, and no profile writes another profile's
ledger.

## Speaking to the human

Whichever mode is running, the person watching sees one thing: profiles, by alias.
`GUILD_MASTER_SPEC.md` section 3.1 makes the alias the human-facing name and the
canonical id the machine one, and each mode renders that differently:

- **Mode 1** — the assistant announces every role switch before doing the step's work:
  `Fighter (business-analyst) — Define requirements`, then speaks as the Fighter until
  the next switch. Without the announcement the human cannot tell which profile is
  talking, since there is only one assistant.
- **Mode 2** — the DM names the subagent it dispatched and the one it is relaying:
  "the Barbarian's regression review passed; handing the change to the Rogue". Subagent
  output reaches the human attributed, never anonymous.
- **Mode 3** — the runtime renders the alias from the `alias` field of the responsible
  profile's manifest whenever it surfaces a step, a gate or a request to a person.

In all three, the alias is presentation only. `responsible_profile`, `from_profile`,
`to_profile`, `evaluated_by` and `requested_by` keep canonical ids; no artifact field
ever stores an alias.

## Human approval steps

Steps with `responsible_profile: human` and `invoked_skill: grant-human-approval`
are gates, not agent work: in every execution mode, the workflow blocks at that
step until an explicit approval is recorded, per
`.guild/core/policies/default-policies.yaml`.

The block is never silent. The DM presents the request in the format defined in
`GUILD_MASTER_SPEC.md` section 11 — the Red-tier policy key, who is asking, which
profile is blocked on the answer (both by alias), the evidence, and what approving and
rejecting each cause. A request that arrives without those fields is returned to the DM
rather than answered, and the resulting `gate-result` records the asking profile's
canonical id in `requested_by`.
