#!/usr/bin/env python3
"""
GHST Agent CLI

Small controller that exposes the GHST daemon capabilities programmatically.
Provides commands to list personas and run the existing daemons (fixer,
auto-commit, cleanup) once or in simple daemon loops.

This is a lightweight integration layer so the assistant abilities can be
invoked from your program or CI.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path


def _env(dry_run: bool = False):
    e = os.environ.copy()
    e.setdefault("PYTHONIOENCODING", "utf-8")
    e.setdefault("PYTHONUTF8", "1")
    if dry_run:
        e["GHST_DRY_RUN"] = "1"
    return e


def run_script(script: str, args: list[str] | None = None, dry_run: bool = False) -> int:
    args = args or []
    cmd = [sys.executable, script] + args
    print(f"Invoking: {' '.join(cmd)}")
    try:
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', env=_env(dry_run))
        if proc.stdout:
            print(proc.stdout)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
        return proc.returncode
    except Exception as e:
        print(f"Failed to run {script}: {e}", file=sys.stderr)
        return 2


def list_personas() -> int:
    # Reuse the fixer daemon persona loader by invoking it in dry-run mode
    # which prints the persona list on startup.
    return run_script("fix_all_errors_daemon.py", ["--once", "--dry-run"], dry_run=True)


def consult_ghsts(topic: str = "general", count: int = 5) -> int:
    """Consult GHST personas and print short, persona-styled advice.

    Tries to import persona loader from `fix_all_errors_daemon.py`. Falls back
    to invoking the daemon to print personas if import fails.
    """
    try:
        # import the persona loaders directly for structured output
        from fix_all_errors_daemon import load_ghost_list, assign_unique_emojis
        personas = load_ghost_list()
        emoji_map = assign_unique_emojis(personas)
    except Exception:
        print("Could not import persona loader; falling back to daemon list output")
        rc = list_personas()
        return rc

    # Limit count
    chosen = personas[:max(1, min(len(personas), count))]

    # Simple templated advice per role (local heuristics)
    role_templates = {
        'Automated Code Cleaner': "Run formatters, then run tests. Prefer small, incremental commits.",
        'Syntax Specialist': "Search for unterminated strings and mismatched quotes; run linters.",
        'Dependency Wrangler': "Pin dependency versions and run a dependency audit.",
        'Style & Lint': "Enforce max-line-length and consistent formatting; add pre-commit hooks.",
        'Repository Steward': "Archive large unused files and document the repo layout.",
        'Test Strategist': "Add focused unit tests for recent changes and CI coverage for critical paths.",
        'Refactorer': "Refactor one module at a time with tests; avoid large sweeping changes.",
        'Merge Whisperer': "Prefer rebasing small feature branches; keep PRs small and reviewable.",
        'Type System Guru': "Add type hints incrementally and run mypy in CI for safety.",
    }

    print(f"Consulting {len(chosen)} GHST(s) on: {topic}\n")
    for p in chosen:
        name = p.get('name')
        role = p.get('role', 'GHST Doctor')
        emoji = emoji_map.get(name, '👻')
        advice = role_templates.get(role, None)
        if advice is None:
            advice = f"(As a {role}) Consider documenting the problem and running targeted tests. Topic: {topic}."
        print(f"{emoji} {name} — {role}\n  ➜ {advice}\n")
    return 0


def run_fixer_once(dry_run: bool = False) -> int:
    # Prefer daemon wrapper, run once
    return run_script("fix_all_errors_daemon.py", ["--once"], dry_run=dry_run)


def run_auto_commit_once(dry_run: bool = False) -> int:
    return run_script("auto_commit_daemon.py", ["--once"], dry_run=dry_run)


def run_cleanup_once(dry_run: bool = True) -> int:
    # default to dry-run for safety
    args = ["--once"]
    if dry_run:
        args += ["--dry-run"]
    return run_script("codebase_cleanup_daemon.py", args, dry_run=dry_run)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ghst_agent", description="GHST Agent CLI")
    sub = parser.add_subparsers(dest="cmd")
    sub.required = True

    sub.add_parser("list-personas", help="Show GHST personas (from ghost generator or fallback)")
    c = sub.add_parser("consult", help="Consult GHST personas on a topic")
    c.add_argument("--topic", type=str, default="general", help="Topic to consult on")
    c.add_argument("--count", type=int, default=5, help="How many GHSTs to consult")

    p = sub.add_parser("fix-once", help="Run fix-all-errors once")
    p.add_argument("--dry-run", action="store_true", help="Do not modify files")

    p2 = sub.add_parser("auto-commit-once", help="Run auto-commit daemon once")
    p2.add_argument("--dry-run", action="store_true", help="Do not push changes")

    p3 = sub.add_parser("cleanup-once", help="Run codebase cleanup once (default dry-run)")
    p3.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="Allow modifications (careful)")
    p3.set_defaults(dry_run=True)

    args = parser.parse_args(argv)

    if args.cmd == "list-personas":
        return list_personas()
    if args.cmd == "fix-once":
        return run_fixer_once(dry_run=getattr(args, "dry_run", False))
    if args.cmd == "auto-commit-once":
        return run_auto_commit_once(dry_run=getattr(args, "dry_run", False))
    if args.cmd == "cleanup-once":
        return run_cleanup_once(dry_run=getattr(args, "dry_run", True))

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
