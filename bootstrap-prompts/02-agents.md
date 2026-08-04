# Prompt 02 — Generate the fourteen Guild profiles

Read all canonical Guild specifications and schemas. Confirm Phase 1 validation passes before continuing.

Generate the fourteen canonical agent profiles under `.guild/agents/`:

1. DM — AI Workflow & Knowledge Orchestrator
2. Paladin — Product Manager / Product Owner
3. Fighter — Business Analyst
4. Druid — Product Experience Designer
5. Bard — UX Writer / Content Designer
6. Ranger — Web Experience Engineer
7. Artificer — Product Software Engineer
8. Wizard — Database Engineer
9. Warlock — Integration Engineer
10. Barbarian — Quality Assurance Engineer
11. Rogue — Product Security Engineer
12. Cleric — Cloud & DevOps Engineer
13. Sorcerer — Product Data Analyst
14. Monk — Data & Analytics Engineer

For every profile, create:

- a validated machine-readable manifest;
- a concise human-readable `AGENT.md`;
- mission and success criteria;
- responsibilities and non-responsibilities;
- required inputs and produced artifacts;
- capabilities and forbidden actions;
- quality gates;
- escalation conditions;
- collaboration and handoff rules;
- a memorable D&D description that never replaces the professional identifier.

Constraints:

- Keep profiles provider-neutral and language-neutral.
- Do not give all profiles unrestricted write or shell access.
- Preserve independent QA and security review.
- The DM validates process and knowledge, not implementation quality.
- The Paladin owns product priority; the Fighter owns requirement precision.
- Do not create provider-specific copies yet.
- Add fixtures or tests proving that all manifests validate and IDs are unique.
- Update planning and status after completion.
