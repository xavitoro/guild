# Discover a project

*Canonical skill id: `discover-project`*

Source of truth: [`SKILL.yaml`](SKILL.yaml) (schema `guild.skill-manifest/v1`).

## Goal

Produce an evidence-based picture of a repository's stack, structure, conventions and operational setup.

## Applicable profiles

workflow-knowledge-orchestrator, product-software-engineer, cloud-devops-engineer

## Inputs

- Repository read access

## Outputs

- Project discovery report

## Steps

- Inventory languages, frameworks and package manifests.
- Identify existing conventions, tests and CI configuration.
- Note anything undocumented or ambiguous rather than guessing.
- Summarize findings as evidence-backed statements with file references.
