#!/usr/bin/env python3
"""Fixture: the first real-project pilot installation (definition-of-done
item 8: "a fresh target repository can install the generated files using
documented steps"), automated so it's repeatable rather than a one-off
manual check.

Follows .guild/core/adapters/INSTALL.md's "into an empty repository" steps
literally, against an isolated temporary directory that has nothing else
from this bootstrap pack (no AGENTS.md, CLAUDE.md, bootstrap-prompts/, and
crucially no .guild/state/ — installing Guild copies only the framework,
never another project's own knowledge/planning/runs):

  1. Copy .guild/core/ into a fresh temp directory, as .guild/core/ there —
     deliberately *not* .guild/state/, since that's this project's own data,
     not part of what gets installed elsewhere.
  2. Run the copied generate_adapters.py against that directory.
  3. Confirm AGENTS.md/CLAUDE.md were created fresh with the managed block,
     and that all Codex/Claude Code adapter files were produced.
  4. Re-run every other .guild/core/evals/check_*.py and validate_guild.py
     *from the copy* (proving .guild/core/ is self-contained and doesn't
     secretly depend on anything else in this bootstrap-pack repository —
     including .guild/state/).
  5. Run the adapter drift check from the copy.

Usage:
    python3 .guild/core/evals/pilot_install_check.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CORE_ROOT = Path(__file__).resolve().parents[1]  # .guild/core/
REPO_ROOT = Path(__file__).resolve().parents[3]

EXPECTED_AGENT_COUNT = 14
EXPECTED_SKILL_COUNT = 22

OTHER_CHECKS = [
    "validate_guild.py",
    "check_agent_profiles.py",
    "check_workflow_refs.py",
    "check_independent_gates.py",
    "check_language_neutrality.py",
]


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def main() -> int:
    errors: list[str] = []

    with tempfile.TemporaryDirectory(prefix="guild-pilot-") as tmp:
        target = Path(tmp) / "pilot-empty-repo"
        target.mkdir()
        shutil.copytree(CORE_ROOT, target / ".guild" / "core")
        print(f"Pilot target: {target} (isolated; contains only a copy of .guild/core/, no .guild/state/)")

        gen = run([sys.executable, str(target / ".guild" / "core" / "adapters" / "generate_adapters.py"),
                   "--target", str(target)], cwd=target)
        print(gen.stdout.strip())
        if gen.returncode != 0:
            errors.append(f"[generate-failed] generate_adapters.py exited {gen.returncode}: {gen.stderr}")

        agents_md = target / "AGENTS.md"
        claude_md = target / "CLAUDE.md"
        if not agents_md.exists() or "guild:adapter:start" not in agents_md.read_text(encoding="utf-8"):
            errors.append("[agents-md] AGENTS.md was not created fresh with the Guild adapter block")
        if not claude_md.exists() or "guild:adapter:start" not in claude_md.read_text(encoding="utf-8"):
            errors.append("[claude-md] CLAUDE.md was not created fresh with the Guild adapter block")

        agent_files = list((target / ".claude" / "agents").glob("*.md")) if (target / ".claude" / "agents").exists() else []
        claude_skills = list((target / ".claude" / "skills").iterdir()) if (target / ".claude" / "skills").exists() else []
        codex_skills = list((target / ".agents" / "skills").iterdir()) if (target / ".agents" / "skills").exists() else []
        if len(agent_files) != EXPECTED_AGENT_COUNT:
            errors.append(f"[agent-count] expected {EXPECTED_AGENT_COUNT} .claude/agents/*.md, found {len(agent_files)}")
        if len(claude_skills) != EXPECTED_SKILL_COUNT:
            errors.append(f"[claude-skill-count] expected {EXPECTED_SKILL_COUNT} .claude/skills/*, found {len(claude_skills)}")
        if len(codex_skills) != EXPECTED_SKILL_COUNT:
            errors.append(f"[codex-skill-count] expected {EXPECTED_SKILL_COUNT} .agents/skills/*, found {len(codex_skills)}")

        for script in OTHER_CHECKS:
            result = run([sys.executable, str(target / ".guild" / "core" / "evals" / script)], cwd=target)
            status = "OK" if result.returncode == 0 else "FAILED"
            print(f"  [{status}] {script} (from the pilot copy)")
            if result.returncode != 0:
                errors.append(f"[{script}-failed] {result.stdout.strip()}\n{result.stderr.strip()}")

        drift = run([sys.executable, str(target / ".guild" / "core" / "adapters" / "generate_adapters.py"),
                     "--target", str(target), "--check"], cwd=target)
        print(f"  [{'OK' if drift.returncode == 0 else 'FAILED'}] adapter drift check (from the pilot copy)")
        if drift.returncode != 0:
            errors.append(f"[drift-failed] {drift.stdout.strip()}\n{drift.stderr.strip()}")

    print()
    for error in errors:
        print(f"ERROR   {error}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s). Fresh installation is not sound.")
        return 1

    print("OK: a fresh, isolated copy of .guild/core/ (no .guild/state/) installs and validates cleanly end to end.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
