# Prompt 03 — Generate skills and workflows

Read and validate the canonical Guild profiles and schemas.

Create a focused initial catalogue of reusable skills and the following workflows:

1. `onboard-existing-project`
2. `create-new-project`
3. `add-feature`
4. `fix-bug`
5. `improve-product`
6. `review-pull-request`

Requirements:

- Keep agent profiles, skills and tools separate.
- Every workflow step must declare profile, skill, inputs, outputs, preconditions, completion criteria and gates.
- Include branches for optional database, integration, web, security, cloud and data involvement.
- Include rejection and return paths.
- Include explicit human approval points for red-level actions.
- Support three execution modes:
  1. one assistant switching roles sequentially;
  2. native subagents;
  3. future external runtime.
- Produce human-readable diagrams or Markdown views alongside machine-readable definitions.
- Create example run fixtures for at least `add-feature` and `fix-bug`.
- Validate all references between workflows, profiles, skills and artifact schemas.
- Update planning and status after completion.
