# Skills

The initial reusable skill catalogue. Each skill has a machine-readable
`SKILL.yaml` (validates against `.guild/core/schemas/skill-manifest.schema.json`)
and a human-readable `SKILL.md`. A skill is a narrow, reusable procedure,
not an identity — several profiles may share a skill, and a profile may use
several skills across different workflow steps.

| Skill | Canonical id | Applicable profiles |
|---|---|---|
| [Triage a request](triage-request/SKILL.md) | `triage-request` | DM (workflow-knowledge-orchestrator) |
| [Claim ownership of an area](claim-ownership/SKILL.md) | `claim-ownership` | every profile |
| [Record what an interaction taught this profile](record-profile-knowledge/SKILL.md) | `record-profile-knowledge` | every profile |
| [Discover a project](discover-project/SKILL.md) | `discover-project` | DM (workflow-knowledge-orchestrator), Artificer (product-software-engineer), Cleric (cloud-devops-engineer) |
| [Define or evaluate product vision](define-product-vision/SKILL.md) | `define-product-vision` | Paladin (product-owner) |
| [Define requirements](define-requirements/SKILL.md) | `define-requirements` | Fighter (business-analyst) |
| [Design an experience](design-experience/SKILL.md) | `design-experience` | Druid (product-experience-designer) |
| [Write interface copy](write-interface-copy/SKILL.md) | `write-interface-copy` | Bard (ux-content-designer) |
| [Implement a feature](implement-feature/SKILL.md) | `implement-feature` | Artificer (product-software-engineer), Ranger (web-experience-engineer) |
| [Diagnose a root cause](diagnose-root-cause/SKILL.md) | `diagnose-root-cause` | Artificer (product-software-engineer), Ranger (web-experience-engineer), Wizard (database-engineer), Warlock (integration-engineer) |
| [Implement a fix](implement-fix/SKILL.md) | `implement-fix` | Artificer (product-software-engineer), Ranger (web-experience-engineer), Wizard (database-engineer), Warlock (integration-engineer) |
| [Maintain a component catalog](maintain-component-catalog/SKILL.md) | `maintain-component-catalog` | Ranger (web-experience-engineer) |
| [Review a schema change](review-schema-change/SKILL.md) | `review-schema-change` | Wizard (database-engineer) |
| [Implement or review an integration](implement-integration/SKILL.md) | `implement-integration` | Warlock (integration-engineer) |
| [Reproduce a defect](reproduce-defect/SKILL.md) | `reproduce-defect` | Barbarian (quality-assurance-engineer) |
| [Run a regression review](run-regression-review/SKILL.md) | `run-regression-review` | Barbarian (quality-assurance-engineer) |
| [Create a threat model](create-threat-model/SKILL.md) | `create-threat-model` | Rogue (product-security-engineer) |
| [Instrument analytics](instrument-analytics/SKILL.md) | `instrument-analytics` | Monk (data-analytics-engineer) |
| [Analyze product data](analyze-product-data/SKILL.md) | `analyze-product-data` | Sorcerer (product-data-analyst) |
| [Plan and execute a deployment](plan-and-execute-deployment/SKILL.md) | `plan-and-execute-deployment` | Cleric (cloud-devops-engineer) |
| [Roll back a deployment](rollback-deployment/SKILL.md) | `rollback-deployment` | Cleric (cloud-devops-engineer) |
| [Set up automated pull-request review](set-up-pull-request-review-automation/SKILL.md) | `set-up-pull-request-review-automation` | Cleric (cloud-devops-engineer) |
| [Prepare a pull request](prepare-pull-request/SKILL.md) | `prepare-pull-request` | DM (workflow-knowledge-orchestrator), Artificer (product-software-engineer), Ranger (web-experience-engineer), Wizard (database-engineer), Warlock (integration-engineer), Monk (data-analytics-engineer) |
| [Review code in a pull request](review-code/SKILL.md) | `review-code` | Barbarian (quality-assurance-engineer) |
| [Grant human approval](grant-human-approval/SKILL.md) | `grant-human-approval` | the human |
| [Put a pending decision to the human](request-human-decision/SKILL.md) | `request-human-decision` | DM (workflow-knowledge-orchestrator), the human |
| [Consolidate knowledge](consolidate-knowledge/SKILL.md) | `consolidate-knowledge` | DM (workflow-knowledge-orchestrator) |
| [Record found work as technical debt](record-technical-debt/SKILL.md) | `record-technical-debt` | DM (workflow-knowledge-orchestrator), Paladin (product-owner), Fighter (business-analyst), Druid (product-experience-designer), Bard (ux-content-designer), Ranger (web-experience-engineer), Artificer (product-software-engineer), Wizard (database-engineer), Warlock (integration-engineer), Barbarian (quality-assurance-engineer), Rogue (product-security-engineer), Cleric (cloud-devops-engineer), Sorcerer (product-data-analyst), Monk (data-analytics-engineer) |

`claim-ownership` and `record-profile-knowledge` are the two protocol skills every
profile runs, and they are not numbered workflow steps: each workflow declares them
once as its `step_protocol`, and every step is bracketed by them — the responsible
profile claims the area it is about to work in, does the step's own skill, then
records what that interaction verified in its own ledger. The same `step_protocol`
names `request-human-decision` as the route for a step blocked on something no
profile can decide from the project itself, and `record-technical-debt` as the route
for the opposite case: a change the step found, which blocks nothing and which it is
not going to make, and which becomes a technical-debt work item in the plan instead
of a note. See `GUILD_MASTER_SPEC.md` sections 7, 8.1 and 11.2.

See `.guild/core/spec/GUILD_MASTER_SPEC.md` section 5 and
`.guild/core/templates/skill-manifest.template.yaml` for the manifest shape, and
`.guild/core/workflows/` for how these skills compose into workflow steps.
