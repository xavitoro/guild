#!/usr/bin/env python3
"""Fixture: proves canonical Guild definitions stay language- and
vendor-neutral (GUILD_MASTER_SPEC.md principle 2 / definition-of-done item
6), by scanning for a curated deny-list of programming languages,
frameworks and cloud/database vendor names.

Scoped to the profile, skill, workflow and spec definitions themselves
(.guild/agents/, .guild/skills/, .guild/workflows/, .guild/templates/,
.guild/spec/) — not .guild/adapters/ (which legitimately names Codex and
Claude Code as the providers it generates for) and not .guild/evals/ (whose
tooling is necessarily written in Python).

This is a heuristic regression guard, not a proof of neutrality: it can
only catch what's on the deny-list, and a term appearing as part of a
larger word is excluded via word-boundary matching to keep false positives
down.

Usage:
    python3 .guild/evals/check_language_neutrality.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

GUILD_ROOT = Path(__file__).resolve().parents[1]

SCOPED_DIRS = ["agents", "skills", "workflows", "templates", "spec"]

DENY_TERMS = [
    "python", "javascript", "typescript", r"java(?!script)", "node\\.js", "nodejs",
    "react", "vue\\.js", "angular", "django", "flask", "rails", "golang", "rust",
    r"php", "c#", "\\.net",
    "aws", "amazon web services", "azure", "gcp", "google cloud",
    "postgresql", "postgres", "mysql", "mongodb",
]
DENY_PATTERN = re.compile(r"\b(" + "|".join(DENY_TERMS) + r")\b", re.IGNORECASE)


def main() -> int:
    errors: list[str] = []
    files_scanned = 0

    for dirname in SCOPED_DIRS:
        base = GUILD_ROOT / dirname
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in (".md", ".yaml", ".yml", ".json"):
                continue
            files_scanned += 1
            for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                for match in DENY_PATTERN.finditer(line):
                    rel = path.relative_to(GUILD_ROOT.parent)
                    errors.append(f"[language-specific] {rel}:{lineno}: found '{match.group(0)}'")

    print(f"Language-neutrality scan: {files_scanned} file(s) across {SCOPED_DIRS}.")
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} hit(s) against the deny-list.")
        return 1

    print("\nOK: no language- or vendor-specific terms found in canonical definitions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
