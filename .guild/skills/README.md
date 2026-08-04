# Skills

The initial reusable skill catalogue. Each skill has a machine-readable
`SKILL.yaml` (validates against `.guild/schemas/skill-manifest.schema.json`)
and a human-readable `SKILL.md`. A skill is a narrow, reusable procedure,
not an identity — several profiles may share a skill, and a profile may use
several skills across different workflow steps.

| Skill | Canonical id | Applicable profiles |
|---|---|---|
| [Triage a request](triage-request/SKILL.md) | `triage-request` | workflow-knowledge-orchestrator |
| [Discover a project](discover-project/SKILL.md) | `discover-project` | workflow-knowledge-orchestrator, product-software-engineer, cloud-devops-engineer |
| [Define or evaluate product vision](define-product-vision/SKILL.md) | `define-product-vision` | product-owner |
| [Define requirements](define-requirements/SKILL.md) | `define-requirements` | business-analyst |
| [Design an experience](design-experience/SKILL.md) | `design-experience` | product-experience-designer |
| [Write interface copy](write-interface-copy/SKILL.md) | `write-interface-copy` | ux-content-designer |
| [Implement a feature](implement-feature/SKILL.md) | `implement-feature` | product-software-engineer, web-experience-engineer |
| [Diagnose a root cause](diagnose-root-cause/SKILL.md) | `diagnose-root-cause` | product-software-engineer, web-experience-engineer, database-engineer, integration-engineer |
| [Implement a fix](implement-fix/SKILL.md) | `implement-fix` | product-software-engineer, web-experience-engineer, database-engineer, integration-engineer |
| [Review a schema change](review-schema-change/SKILL.md) | `review-schema-change` | database-engineer |
| [Implement or review an integration](implement-integration/SKILL.md) | `implement-integration` | integration-engineer |
| [Reproduce a defect](reproduce-defect/SKILL.md) | `reproduce-defect` | quality-assurance-engineer |
| [Run a regression review](run-regression-review/SKILL.md) | `run-regression-review` | quality-assurance-engineer |
| [Create a threat model](create-threat-model/SKILL.md) | `create-threat-model` | product-security-engineer |
| [Instrument analytics](instrument-analytics/SKILL.md) | `instrument-analytics` | data-analytics-engineer |
| [Analyze product data](analyze-product-data/SKILL.md) | `analyze-product-data` | product-data-analyst |
| [Plan and execute a deployment](plan-and-execute-deployment/SKILL.md) | `plan-and-execute-deployment` | cloud-devops-engineer |
| [Roll back a deployment](rollback-deployment/SKILL.md) | `rollback-deployment` | cloud-devops-engineer |
| [Prepare a pull request](prepare-pull-request/SKILL.md) | `prepare-pull-request` | workflow-knowledge-orchestrator, product-software-engineer, web-experience-engineer, database-engineer, integration-engineer, data-analytics-engineer |
| [Review code in a pull request](review-code/SKILL.md) | `review-code` | quality-assurance-engineer |
| [Grant human approval](grant-human-approval/SKILL.md) | `grant-human-approval` | human |
| [Consolidate knowledge](consolidate-knowledge/SKILL.md) | `consolidate-knowledge` | workflow-knowledge-orchestrator |

See `.guild/spec/GUILD_MASTER_SPEC.md` section 5 and
`.guild/templates/skill-manifest.template.yaml` for the manifest shape, and
`.guild/workflows/` for how these skills compose into workflow steps.
