@AGENTS.md

## Claude Code adapter note

Treat `.guild/` as the canonical source. Project-specific Claude subagents and skills may be generated under `.claude/`, but they must retain a source reference to the canonical Guild definition.

Use separate subagents for independent QA and security review once those project subagents exist.
