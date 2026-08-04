# Fix a bug

*Canonical workflow id: `fix-bug`*

Source of truth: [`workflow.yaml`](workflow.yaml) (schema `guild.workflow/v1`).
See [`../EXECUTION_MODES.md`](../EXECUTION_MODES.md) for how this definition maps to a single
assistant switching roles, native subagents, or a future external runtime.

## Description

Intake by the DM, reproduction by QA, root-cause and plan by the Product Software Engineer, specialist review when needed, implementation by the relevant specialist, regression validation by QA, conditional review by security, and pull-request preparation by the DM.

## Diagram

Diamond-shaped nodes are optional/conditional steps; see the step table for their condition.

```mermaid
flowchart TD
    fix-bug-01-triage["Triage the defect report"]
    fix-bug-02-reproduce["Reproduce the defect"]
    fix-bug-03-diagnose-root-cause["Diagnose the root cause"]
    fix-bug-04-review-schema{{"Review a schema-related root cause"}}
    fix-bug-05-review-integration{{"Review an integration-related root cause"}}
    fix-bug-06-implement-fix-backend{{"Implement the backend fix"}}
    fix-bug-07-implement-fix-frontend{{"Implement the frontend fix"}}
    fix-bug-08-implement-fix-database{{"Implement the database fix"}}
    fix-bug-09-implement-fix-integration{{"Implement the integration fix"}}
    fix-bug-10-regression-review["Verify the fix"]
    fix-bug-11-threat-model{{"Review security impact"}}
    fix-bug-12-prepare-pull-request["Prepare the pull request"]
    fix-bug-13-human-approval-merge{{"Approve merge to a protected branch"}}
    fix-bug-01-triage --> fix-bug-02-reproduce
    fix-bug-02-reproduce --> fix-bug-03-diagnose-root-cause
    fix-bug-03-diagnose-root-cause --> fix-bug-04-review-schema
    fix-bug-04-review-schema --> fix-bug-05-review-integration
    fix-bug-05-review-integration --> fix-bug-06-implement-fix-backend
    fix-bug-06-implement-fix-backend --> fix-bug-07-implement-fix-frontend
    fix-bug-07-implement-fix-frontend --> fix-bug-08-implement-fix-database
    fix-bug-08-implement-fix-database --> fix-bug-09-implement-fix-integration
    fix-bug-09-implement-fix-integration --> fix-bug-10-regression-review
    fix-bug-10-regression-review --> fix-bug-11-threat-model
    fix-bug-11-threat-model --> fix-bug-12-prepare-pull-request
    fix-bug-12-prepare-pull-request --> fix-bug-13-human-approval-merge
```

## Steps

| Step id | Name | Responsible profile | Invoked skill | Gates |
|---|---|---|---|---|
| `fix-bug-01-triage` | Triage the defect report | workflow-knowledge-orchestrator | `triage-request` | — |
| `fix-bug-02-reproduce` | Reproduce the defect | quality-assurance-engineer | `reproduce-defect` | — |
| `fix-bug-03-diagnose-root-cause` | Diagnose the root cause | product-software-engineer | `diagnose-root-cause` | — |
| `fix-bug-04-review-schema` | Review a schema-related root cause *(optional — when the root cause is in the database schema or a migration)* | database-engineer | `review-schema-change` | — |
| `fix-bug-05-review-integration` | Review an integration-related root cause *(optional — when the root cause is in an external integration)* | integration-engineer | `implement-integration` | — |
| `fix-bug-06-implement-fix-backend` | Implement the backend fix *(optional — when the root cause is in backend/domain logic)* | product-software-engineer | `implement-fix` | — |
| `fix-bug-07-implement-fix-frontend` | Implement the frontend fix *(optional — when the root cause is in the web-experience/frontend layer)* | web-experience-engineer | `implement-fix` | — |
| `fix-bug-08-implement-fix-database` | Implement the database fix *(optional — when the root cause requires a schema or data fix)* | database-engineer | `implement-fix` | — |
| `fix-bug-09-implement-fix-integration` | Implement the integration fix *(optional — when the root cause requires an integration fix)* | integration-engineer | `implement-fix` | — |
| `fix-bug-10-regression-review` | Verify the fix | quality-assurance-engineer | `run-regression-review` | qa_gate_pass |
| `fix-bug-11-threat-model` | Review security impact *(optional — when the defect is security-relevant (authentication, authorization, injection, data exposure or secret handling))* | product-security-engineer | `create-threat-model` | security_gate_clean |
| `fix-bug-12-prepare-pull-request` | Prepare the pull request | workflow-knowledge-orchestrator | `prepare-pull-request` | — |
| `fix-bug-13-human-approval-merge` | Approve merge to a protected branch *(optional — when the target branch is protected)* | human | `grant-human-approval` | merge_protected_branch |

## Failure paths

- An unreproducible defect halts the workflow at reproduction and escalates to the DM/requester for more information.
- A failing regression review returns to the implementing step rather than proceeding to pull-request preparation.

## Return paths

- An inconclusive root-cause analysis returns to reproduction for a narrower repro.

## Escalation paths

- An open critical/high security finding blocks pull-request preparation until resolved and re-reviewed.
- Merging to a protected branch always escalates to the human before proceeding.
