# Guild Project Status

Updated: 17 September 2026

## Overall status

Milestones M1 (declarative foundation), M2 (provider adapters), M3
(evaluation and first real-project pilot), M4 (repository layout
hardening), M5 (distributed ownership and knowledge), M6 (nothing stays
pending), M7 (every question is answerable) and M8 (nothing found is dropped)
are all complete. WI-001 through WI-010 are done. `.guild/` splits into `core/` (the Guild
framework, replaceable wholesale on upgrade) and `state/` (this project's
own knowledge, planning and run history, never touched by an upgrade) —
see `.guild/state/knowledge/decisions/DEC-001-core-state-split.yaml`. Every
part of the project now has exactly one owning profile that accumulates its
own evidence-backed knowledge, and the DM routes by the index at
`.guild/state/knowledge/ownership.yaml` rather than by holding what every
owner knows — see
`.guild/state/knowledge/decisions/DEC-002-distributed-ownership.yaml` and
`.guild/state/knowledge/OWNERSHIP.md`. Every decision no profile can make from
the project itself is now a decision request with options, a recommendation and
a stated default, presented to a person and listed by id below — see
`.guild/state/knowledge/decisions/DEC-004-decision-requests.yaml`. And whatever
is left for a person to resolve now reaches them in a fixed answerable shape:
enumerated options, always plus a free-text answer, because the option set is
written by the profile that could not decide and is never the limit of what may
be answered — see
`.guild/state/knowledge/decisions/DEC-009-options-plus-free-text.yaml`. And a
change a profile finds while doing something else, which blocks nothing and
which it is not going to make, is now a technical-debt work item in the plan —
with an origin, evidence and the owner of the area it was found in, unscheduled
until the Paladin (`product-owner`) prioritizes it — instead of a `TODO` comment
or a line in a summary; see
`.guild/state/knowledge/decisions/DEC-010-found-work-becomes-a-task.yaml`.

## Current objective

No decision is pending, and nothing found is unrecorded. `DR-001` to `DR-004`
were answered on 1 September 2026 and recorded as `DEC-005` to `DEC-008`; the
four technical-debt items below are recorded and unscheduled, and none of them
blocks anything. The only remaining planned work is piloting Guild
on a genuine external project — now unblocked, since the licensing question that
held it is answered. The automated pilot in
`.guild/core/evals/pilot_install_check.py` proves the install steps work against
an isolated fresh copy of `.guild/core/`, but is not a substitute for real
usage.

## Ready work

- (none — no work items are currently ready; new work requires scoping a
  new milestone or work item)

## Planned next

- Install Guild into a real external project and run an actual workflow
  end to end with a human in the loop.

## Open technical debt

Found while building M8, all outside the scope of the step that found them and
blocking nothing. Each is recorded unscheduled: the Paladin (`product-owner`)
decides whether and when any of them is worth a milestone.

| Item | What was found | Owner |
|---|---|---|
| [`TD-001`](project-plan.yaml) | `GUILD_MASTER_SPEC.md` sections 7 and 8 promise `roadmap.yaml`, `milestones/`, `backlog/`, `archive/`, `discoveries/` and `patterns/` under `.guild/state/`; none of them exists | DM (`workflow-knowledge-orchestrator`) |
| [`TD-002`](project-plan.yaml) | `PROJECT_PLAN.md` and this file restate their canonical YAML by hand, and nothing compares the two | DM (`workflow-knowledge-orchestrator`) |
| [`TD-003`](project-plan.yaml) | A run record names its workflow and steps but no work item, so progress cannot be derived from run history | DM (`workflow-knowledge-orchestrator`) |
| [`TD-004`](project-plan.yaml) | The required-check list lives both in `evals/README.md` and in `pilot_install_check.py`, so a future check can drop out of the pilot silently | Barbarian (`quality-assurance-engineer`) |

## Open decisions

None. Every decision request raised in this project has been answered.

## Decisions closed on 1 September 2026

| Request | Question | Answer | Record |
|---|---|---|---|
| [`DR-001`](decisions/DR-001-public-name.yaml) | Is "Guild" the public product and protocol name? | Yes — keep "Guild" (the DM's recommendation) | [`DEC-005`](../knowledge/decisions/DEC-005-public-name.yaml) |
| [`DR-002`](decisions/DR-002-license.yaml) | Under what license is this published? | MIT, as the existing `LICENSE` already states — the human chose the short permissive form over the DM's recommendation of one with a patent grant | [`DEC-006`](../knowledge/decisions/DEC-006-license.yaml) |
| [`DR-003`](decisions/DR-003-adapter-distribution.yaml) | Are adapters generated at install or shipped pre-generated? | Generated at install (the Artificer's recommendation) | [`DEC-007`](../knowledge/decisions/DEC-007-adapter-distribution.yaml) |
| [`DR-004`](decisions/DR-004-cli-in-first-release.yaml) | Does the first public release include a CLI? | No — definitions and generator only (the DM's recommendation) | [`DEC-008`](../knowledge/decisions/DEC-008-no-cli-in-first-release.yaml) |

- `DEC-003` — a failed deployment now routes into `rollback-deployment` through
  the deploy step's return path in the three workflows that deploy. Raised by the
  Fighter (`business-analyst`) as `KNQ-business-analyst-001`, answered by the DM
  rather than escalated, because it was answerable from the repository itself.

Each `DR-*` file keeps its revisit trigger: none of these is sealed, but none of
them is pending either. Each also now records `answer_kind`, which distinguishes
an answer chosen from the options from one given in the human's own words; all
four were option answers.
