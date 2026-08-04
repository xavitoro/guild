# Agent profiles

The fourteen canonical Guild profiles. Each has a machine-readable
`manifest.yaml` (validates against
`.guild/core/schemas/agent-manifest.schema.json`) and a human-readable
`AGENT.md`. The manifest is canonical; `AGENT.md` is a view over it.

| Alias | Professional profile | Canonical id |
|---|---|---|
| DM | [AI Workflow & Knowledge Orchestrator](workflow-knowledge-orchestrator/AGENT.md) | `workflow-knowledge-orchestrator` |
| Paladin | [Product Manager / Product Owner](product-owner/AGENT.md) | `product-owner` |
| Fighter | [Business Analyst](business-analyst/AGENT.md) | `business-analyst` |
| Druid | [Product Experience Designer](product-experience-designer/AGENT.md) | `product-experience-designer` |
| Bard | [UX Writer / Content Designer](ux-content-designer/AGENT.md) | `ux-content-designer` |
| Ranger | [Web Experience Engineer](web-experience-engineer/AGENT.md) | `web-experience-engineer` |
| Artificer | [Product Software Engineer](product-software-engineer/AGENT.md) | `product-software-engineer` |
| Wizard | [Database Engineer](database-engineer/AGENT.md) | `database-engineer` |
| Warlock | [Integration Engineer](integration-engineer/AGENT.md) | `integration-engineer` |
| Barbarian | [Quality Assurance Engineer](quality-assurance-engineer/AGENT.md) | `quality-assurance-engineer` |
| Rogue | [Product Security Engineer](product-security-engineer/AGENT.md) | `product-security-engineer` |
| Cleric | [Cloud & DevOps Engineer](cloud-devops-engineer/AGENT.md) | `cloud-devops-engineer` |
| Sorcerer | [Product Data Analyst](product-data-analyst/AGENT.md) | `product-data-analyst` |
| Monk | [Data & Analytics Engineer](data-analytics-engineer/AGENT.md) | `data-analytics-engineer` |

See `.guild/core/spec/GUILD_MASTER_SPEC.md` section 4 for the source definitions
and `.guild/core/templates/agent-manifest.template.yaml` for the manifest shape.
