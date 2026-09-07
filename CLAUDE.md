@AGENTS.md

## Claude Code adapter note

Treat `.guild/core/` as the canonical Guild framework source (replaceable wholesale on a Guild upgrade) and `.guild/state/` as this project's own knowledge, planning and run history (never touched by an upgrade). Project-specific Claude subagents and skills may be generated under `.claude/`, but they must retain a source reference to the canonical Guild definition.

Use separate subagents for independent QA and security review once those project subagents exist.

<!-- guild:adapter:start -->
## Guild adapter (generated — do not edit this section by hand)

Claude Code subagents are generated under `.claude/agents/<profile-id>.md` and Claude
Code skills under `.claude/skills/<skill-id>/SKILL.md`, both derived from the canonical
manifests under `.guild/core/agents/` and `.guild/core/skills/`. Quality assurance
(`quality-assurance-engineer` / Barbarian) and security (`product-security-engineer` /
Rogue) are separate subagents, independent from every implementation subagent, per
`.guild/core/spec/GUILD_MASTER_SPEC.md` principle 6.

Every subagent introduces itself to the human by its Guild alias (DM, Paladin, Fighter,
Druid, Bard, Ranger, Artificer, Wizard, Warlock, Barbarian, Rogue, Cleric, Sorcerer,
Monk) with its canonical id in parentheses on first mention, and names the other profiles
the same way; canonical ids alone stay in artifact fields, per
`.guild/core/spec/GUILD_MASTER_SPEC.md` section 3.1.

Each subagent owns a declared part of the project and keeps its own knowledge ledger
under `.guild/state/knowledge/profiles/<profile-id>.yaml`, claiming its area before a
step and recording what the step verified afterwards. The DM
(`workflow-knowledge-orchestrator`) maintains `.guild/state/knowledge/ownership.yaml`
as an index of area, owner and ledger location, and routes by those pointers — which
is what lets a subagent hand back entry ids instead of its whole reasoning, and keeps
the orchestrator's context bounded as the project grows.

Nothing is left pending by default: what a subagent cannot decide from the project
itself becomes a decision request under `.guild/state/planning/decisions/` — options,
a recommendation and the default that applies if nobody answers — which the DM puts to
a person and records. A default never applies before the human has seen it, and
Red-tier actions remain approvals that block outright.

Whatever is put to a person is asked as enumerated options and always offers an answer
in their own words (`other`), because the options are only what the asking subagent could
enumerate: without a way out of them, a person whose answer is not listed can only stay
silent, and silence just re-runs the default. A free-text answer is recorded verbatim and
closes a decision request; on a Red-tier approval it is recorded but never approves. The DM
presents a decision request with the `AskUserQuestion` tool — one option per stated option
plus `defer`, and its automatic "Other" choice as the free-text answer. Red-tier approvals
stay explicit approval requests. See `.guild/core/spec/GUILD_MASTER_SPEC.md` section 11.3.

No subagent is granted unrestricted tool access; each gets only the tools its
`allowed_capabilities` imply (see `.guild/core/adapters/generate_adapters.py`).
`.claude/settings.json` additionally denies one deterministic, policy-derived pattern
(force-push) as a concrete instance of "optional policy-derived hooks only when
deterministic enforcement is appropriate" — the rest of
`.guild/core/policies/default-policies.yaml`'s Red-tier actions cannot be reliably
pattern-matched from arbitrary shell commands and still rely on the explicit
human-approval workflow steps instead.

Regenerate after any change under `.guild/core/agents/` or `.guild/core/skills/`:

    python3 .guild/core/adapters/generate_adapters.py --target .
<!-- guild:adapter:end -->
