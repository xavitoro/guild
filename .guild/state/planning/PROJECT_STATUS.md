# Guild Project Status

Updated: 4 August 2026

## Overall status

Milestones M1 (declarative foundation), M2 (provider adapters), M3
(evaluation and first real-project pilot) and M4 (repository layout
hardening) are all complete. WI-001 through WI-006 are done. `.guild/` now
splits into `core/` (the Guild framework, replaceable wholesale on
upgrade) and `state/` (this project's own knowledge, planning and run
history, never touched by an upgrade) — see
`.guild/state/knowledge/decisions/DEC-001-core-state-split.yaml`.

## Current objective

Remaining work is human-owned: resolve the open decisions below, and pilot
Guild on a genuine external project (the automated pilot in
`.guild/core/evals/pilot_install_check.py` proves the install steps work
against an isolated fresh copy of `.guild/core/`, but is not a substitute
for real usage).

## Ready work

- (none — no work items are currently ready; new work requires scoping a
  new milestone or work item)

## Planned next

- Resolve the open decisions below.
- Install Guild into a real external project and run an actual workflow
  end to end with a human in the loop.

## Open decisions

- Final public product and protocol name.
- License.
- Whether adapters are copied or generated during installation.
- Whether a CLI is included in the first public release.
