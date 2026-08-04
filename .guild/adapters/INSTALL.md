# Installing Guild

Guild has one canonical source — the `.guild/` directory — and one
generator that turns it into provider-specific adapter files:
`.guild/adapters/generate_adapters.py`. Installing Guild always means:
copy `.guild/` into the target, then run the generator there.

## Into an empty repository

1. Copy the `.guild/` directory tree into the new repository's root.
2. From the new repository's root, run:
   ```
   python3 .guild/adapters/generate_adapters.py --target .
   ```
   This creates `.agents/skills/`, `.claude/agents/`, `.claude/skills/`,
   `.claude/settings.json`, and a root `AGENTS.md`/`CLAUDE.md` (created
   fresh, since none exist yet).
3. Commit the result, including the generated files — they are meant to be
   checked in, not regenerated on every clone. Regenerate only after
   changing something under `.guild/agents/` or `.guild/skills/`.

## Into an existing repository

Same two steps, with one difference: if the repository already has an
`AGENTS.md` and/or `CLAUDE.md`, the generator **appends** a clearly marked
`<!-- guild:adapter:start -->` … `<!-- guild:adapter:end -->` block rather
than overwriting the file. Everything above and below that block —
including this repository's own hand-written project instructions — is
left exactly as it was. Re-running the generator later updates only the
content between those markers.

If the repository already has `.claude/agents/`, `.claude/skills/` or
`.agents/skills/` entries that aren't Guild-generated, they're left alone:
the generator only ever touches files it can identify as its own via the
`GENERATED FILE — DO NOT EDIT BY HAND` header, and only removes a
previously generated file once its canonical id is actually gone from
`.guild/`.

## Into a user-level / global configuration

Where a client supports a global, cross-project configuration directory —
for example Claude Code's `~/.claude/agents/` and `~/.claude/skills/` —
point `--target` at that directory instead of a repository root:

```
python3 .guild/adapters/generate_adapters.py --target ~
```

Consult that client's own documentation for the exact global paths it
honors and how global configuration interacts with project-level
configuration; these vary by client and by version, so this repository
does not assume specifics beyond the `--target` mechanism itself. Installing
all fourteen profiles and every skill globally is rarely what you want —
most users installing Guild globally will want a curated subset; edit the
generated output's containing directory afterward, or maintain a reduced
copy of `.guild/agents/` / `.guild/skills/` for that purpose.

## Verifying an installation

After generating, two checks confirm the installation is sound:

```
python3 .guild/evals/validate_guild.py          # schemas, syntax, ids, refs
python3 .guild/adapters/generate_adapters.py --target . --check   # adapter drift
```

Both should report success with no errors.
