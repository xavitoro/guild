# Guild structural validation

Run all required checks from the repository root:

```
python3 .guild/evals/validate_guild.py
python3 .guild/evals/check_agent_profiles.py
python3 .guild/evals/check_workflow_refs.py
python3 .guild/evals/check_independent_gates.py
python3 .guild/evals/check_language_neutrality.py
python3 .guild/adapters/generate_adapters.py --target . --check
```

Two are demonstrations rather than part of the required gate, but worth
running after any change to agents, skills or workflows:

```
python3 .guild/evals/smoke_test_add_feature.py
python3 .guild/evals/pilot_install_check.py
```

## validate_guild.py

Requires `pyyaml` and `jsonschema` (draft 2020-12 support). Checks YAML/JSON
syntax, schema validity, instance-to-schema validation (including
cross-schema `$ref`), global `id:` uniqueness, and `depends_on:` reference
resolution across the whole `.guild/` tree.

Exit code `0` means no errors. Unresolved `depends_on` references are
reported as warnings rather than errors, since profiles, skills and
workflows are introduced in later phases and may be referenced by id ahead
of their own definition landing. Files under `.guild/templates/` are
illustrative placeholders (e.g. `id: replace-with-...`) and are exempt from
schema and reference checks; they are still parsed for YAML validity.

## check_agent_profiles.py

Proves the fourteen canonical agent profiles are all present under
`.guild/agents/`, each validates against `agent-manifest.schema.json`, and
no id is missing, extra, or duplicated relative to the roster in
`GUILD_MASTER_SPEC.md` section 3.

## check_workflow_refs.py

Validates the semantic references plain JSON Schema can't express: every
workflow step's `responsible_profile` and `invoked_skill` resolve to a real
profile/skill (or the `human` sentinel), every skill's
`applicable_profiles` resolve to real profiles, and every run record's
`workflow_id`/`step_id`s resolve to a real workflow and its steps.

## check_independent_gates.py

Proves "independent QA and security gates" (`GUILD_MASTER_SPEC.md`
principle 6) holds structurally, not just by convention: every agent
manifest forbids every Red-tier action from
`.guild/policies/default-policies.yaml`; every profile that can edit code
forbids approving its own QA/security result; the QA and security profiles
specifically cannot edit code and cannot approve each other's gate; and
every workflow step whose gates include a Red-tier action has
`responsible_profile: human`.

## check_language_neutrality.py

A heuristic deny-list scan of `.guild/agents/`, `.guild/skills/`,
`.guild/workflows/`, `.guild/templates/` and `.guild/spec/` for
language/framework/cloud-vendor names, guarding definition-of-done item 6
("no canonical definition requires a particular language or vendor").
Deliberately excludes `.guild/adapters/` (which legitimately names Codex
and Claude Code) and `.guild/evals/` (tooling, necessarily Python).

## generate_adapters.py --check

Drift detection for the generated Codex/Claude Code adapters (see
`.guild/adapters/README.md`): fails if a generated file no longer matches
its canonical source, hasn't been generated yet, was hand-edited, or is
orphaned (its canonical id was removed).

## smoke_test_add_feature.py

Demonstrates that the generated adapters give complete coverage for one
real workflow (`add-feature`): every step's responsible profile has a
generated Claude Code subagent and every step's invoked skill has generated
Codex and Claude Code skill files, all pointing back at their canonical
source and passing the drift check.

## pilot_install_check.py

The automated first real-project pilot (definition-of-done item 8): copies
`.guild/` into an isolated temp directory containing nothing else from this
repository, runs the adapter generator there exactly as
`.guild/adapters/INSTALL.md`'s "into an empty repository" steps describe,
and re-runs every other check above *from that copy* — proving `.guild/` is
genuinely self-contained and that the documented install steps work for a
fresh target, not just in place in this repository.
