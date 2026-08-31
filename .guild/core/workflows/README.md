# Workflows

The six canonical initial workflows. Each has a machine-readable `workflow.yaml`
(validates against `.guild/core/schemas/workflow.schema.json`, with each step validating
against `.guild/core/schemas/workflow-step.schema.json`) and a human-readable `workflow.md`
with a Mermaid diagram.

| Workflow | Canonical id | Steps |
|---|---|---|
| [Onboard an existing project](onboard-existing-project/workflow.md) | `onboard-existing-project` | 5 |
| [Create a new project](create-new-project/workflow.md) | `create-new-project` | 15 |
| [Add a feature](add-feature/workflow.md) | `add-feature` | 17 |
| [Fix a bug](fix-bug/workflow.md) | `fix-bug` | 13 |
| [Improve the product](improve-product/workflow.md) | `improve-product` | 19 |
| [Review a pull request](review-pull-request/workflow.md) | `review-pull-request` | 7 |

See [`EXECUTION_MODES.md`](EXECUTION_MODES.md) for how these definitions run as a single
assistant, as native subagents, or under a future external runtime, and
`.guild/core/spec/GUILD_MASTER_SPEC.md` section 9 for the source requirement.
