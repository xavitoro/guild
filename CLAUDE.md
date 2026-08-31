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
