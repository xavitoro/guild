# Guild structural validation

Run all required checks from the repository root:

```
python3 .guild/core/evals/validate_guild.py
python3 .guild/core/evals/check_agent_profiles.py
python3 .guild/core/evals/check_workflow_refs.py
python3 .guild/core/evals/check_independent_gates.py
python3 .guild/core/evals/check_language_neutrality.py
python3 .guild/core/evals/check_alias_presence.py
python3 .guild/core/evals/check_ownership_model.py
python3 .guild/core/evals/check_human_in_the_loop.py
python3 .guild/core/adapters/generate_adapters.py --target . --check
```

Two are demonstrations rather than part of the required gate, but worth
running after any change to agents, skills or workflows:

```
python3 .guild/core/evals/smoke_test_add_feature.py
python3 .guild/core/evals/pilot_install_check.py
```

## validate_guild.py

Requires `pyyaml` and `jsonschema` (draft 2020-12 support). Checks YAML/JSON
syntax, schema validity, instance-to-schema validation (including
cross-schema `$ref`), global `id:` uniqueness, and `depends_on:` reference
resolution across the whole `.guild/` tree (both `core/` and `state/`).

Exit code `0` means no errors. Unresolved `depends_on` references are
reported as warnings rather than errors, since profiles, skills and
workflows are introduced in later phases and may be referenced by id ahead
of their own definition landing. Files under `.guild/core/templates/` are
illustrative placeholders (e.g. `id: replace-with-...`) and are exempt from
schema and reference checks; they are still parsed for YAML validity.

## check_agent_profiles.py

Proves the fourteen canonical agent profiles are all present under
`.guild/core/agents/`, each validates against `agent-manifest.schema.json`,
and no id is missing, extra, or duplicated relative to the roster in
`GUILD_MASTER_SPEC.md` section 3.

## check_workflow_refs.py

Validates the semantic references plain JSON Schema can't express: every
workflow step's `responsible_profile` and `invoked_skill` resolve to a real
profile/skill (or the `human` sentinel), every skill's
`applicable_profiles` resolve to real profiles, and every run record's
(under `.guild/state/runs/`) `workflow_id`/`step_id`s resolve to a real
workflow and its steps.

## check_independent_gates.py

Proves "independent QA and security gates" (`GUILD_MASTER_SPEC.md`
principle 6) holds structurally, not just by convention: every agent
manifest forbids every Red-tier action from
`.guild/core/policies/default-policies.yaml`; every profile that can edit
code forbids approving its own QA/security result; the QA and security
profiles specifically cannot edit code and cannot approve each other's
gate; and every workflow step whose gates include a Red-tier action has
`responsible_profile: human`.

## check_language_neutrality.py

A heuristic deny-list scan of `.guild/core/agents/`, `.guild/core/skills/`,
`.guild/core/workflows/`, `.guild/core/templates/` and `.guild/core/spec/`
for language/framework/cloud-vendor names, guarding definition-of-done item
6 ("no canonical definition requires a particular language or vendor").
Deliberately excludes `.guild/core/adapters/` (which legitimately names
Codex and Claude Code) and `.guild/core/evals/` (tooling, necessarily
Python).

## check_alias_presence.py

Proves the D&D roster is actually used where a person can see it
(`GUILD_MASTER_SPEC.md` section 3.1): the alias-first principle is declared in
`default-policies.yaml`, every `AGENT.md` introduces its own alias, every
`workflow.md` step-table row and Mermaid node names the responsible profile's
alias, every core `SKILL.md` renders its applicable profiles as
`Alias (canonical-id)`, and `grant-human-approval` requires the request to
identify profiles by alias. It also checks the complementary direction — that
no `responsible_profile` or `applicable_profiles` entry stores an alias where a
canonical id belongs.

## check_ownership_model.py

Proves the distributed-ownership model (`GUILD_MASTER_SPEC.md` principle 12
and section 7) is structural rather than prose. The canonical half always
runs: `default-policies.yaml` declares the knowledge protocol; every profile
can record its own knowledge, forbids writing another profile's ledger and
carries the step-entry/step-exit quality gate; only the orchestrator may
maintain the ownership map or consolidate canonical memory; the two protocol
skills apply to all fourteen profiles; and every workflow declares a
`step_protocol` whose skills resolve. The state half runs only when
`.guild/state/knowledge/ownership.yaml` exists — so a fresh `.guild/core/`-only
installation still passes — and then checks that every area has exactly one
real owner, that each ledger is written only by its own profile with entry ids
carrying that profile's id, that the map and the ledgers agree on ownership in
both directions, and that every pointer (`last_entry`, `open_questions`,
`related_areas`, `promoted_to`) resolves.

## check_human_in_the_loop.py

Proves that nothing is left pending by default (`GUILD_MASTER_SPEC.md`
principle 13 and sections 11.1-11.2). The canonical half always runs:
`default-policies.yaml` declares the decision protocol and the fields a
request must state; `request-human-decision` exists and is answerable by the
human; the decision-request schema makes an incomplete request unwritable
(at least two options, a recommendation, and a default with an effective
moment and a revisit trigger); `project-status.schema.json` accepts only
decision-request ids, so an open decision can never be a bare sentence; every
workflow declares `step_protocol.on_blocked_decision`; every profile escalates
what it cannot decide as a decision request, and only the orchestrator may
present one. The state half runs when `.guild/state/planning/decisions/`
exists and checks that open requests are listed in the status file *and*
named in `PROJECT_STATUS.md`, that recommended and default options actually
exist, that an answered or deferred request records who answered and what,
that no request reached `presented`/`answered`/`deferred` without a
`presented_at` — a default may not apply before it was shown — and that no
ledger question blocked on the human was left un-escalated.

## generate_adapters.py --check

Drift detection for the generated Codex/Claude Code adapters (see
`.guild/core/adapters/README.md`): fails if a generated file no longer
matches its canonical source, hasn't been generated yet, was hand-edited,
or is orphaned (its canonical id was removed).

## smoke_test_add_feature.py

Demonstrates that the generated adapters give complete coverage for one
real workflow (`add-feature`): every step's responsible profile has a
generated Claude Code subagent and every step's invoked skill has generated
Codex and Claude Code skill files, all pointing back at their canonical
source and passing the drift check.

## pilot_install_check.py

The automated first real-project pilot (definition-of-done item 8): copies
`.guild/core/` (deliberately never `.guild/state/`, which is this
project's own data) into an isolated temp directory containing nothing else
from this repository, runs the adapter generator there exactly as
`.guild/core/adapters/INSTALL.md`'s "into an empty repository" steps
describe, and re-runs every other check above *from that copy* — proving
`.guild/core/` is genuinely self-contained and that the documented install
steps work for a fresh target, not just in place in this repository.
