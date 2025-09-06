#!/usr/bin/env python3
"""
GHST Fix-All-Errors Daemon — Dr. TidyCode (PhD GHST)
Consolidated implementation: loads GHST personas, assigns unique emojis,
ensures tooling, and runs the repository fixer once or as a daemon.
"""

from __future__ import annotations

import io
import json
import logging
import os
import random
import subprocess
import sys
import time
from hashlib import sha256
from pathlib import Path
from typing import Dict, List

# UTF-8 safe logging
_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
_file_handler = logging.FileHandler("fix_all_errors_daemon.log", encoding="utf-8")
_stream_handler = logging.StreamHandler(_stdout)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[_file_handler, _stream_handler],
)
logger = logging.getLogger("ghst.fix_all_errors")


def load_ghost_list() -> List[Dict[str, str]]:
    """Load persona list from generator module or common files.

    Returns list of dicts: {'name': str, 'role': str}
    """
    # Try in-repo generator module variants
    mod_paths = (
        "src.ai_collaboration.ghost_generator",
        "ai_collaboration.ghost_generator",
        "ghost_generator",
    )
    accessors = (
        "generate_ghosts",
        "get_ghosts",
        "get_ghost_list",
        "load_ghosts",
        "ghost_list",
        "ghosts",
    )

    for mod_path in mod_paths:
        try:
            mod = __import__(mod_path, fromlist=["*"])
        except Exception:
            continue
        for acc in accessors:
            val = getattr(mod, acc, None)
            if val is None:
                continue
            try:
                data = val() if callable(val) else val
            except Exception:
                data = val
            if not isinstance(data, list) or not data:
                continue
            out: List[Dict[str, str]] = []
            for item in data:
                if isinstance(item, dict) and "name" in item:
                    out.append({"name": item["name"], "role": item.get("role", "GHST Doctor")})
                elif isinstance(item, str):
                    out.append({"name": item, "role": "GHST Doctor"})
            if out:
                logger.info("Loaded %d GHSTs from %s.%s", len(out), mod_path, acc)
                return out

    # Try common files
    possible = (
        Path("ghosts/ghost_list.json"),
        Path("ghosts/ghost_list.txt"),
        Path(".ghost_list.json"),
        Path(".github/ghost_list.txt"),
    )
    for p in possible:
        if not p.exists():
            continue
        try:
            if p.suffix == ".json":
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
                out = []
                for item in data:
                    if isinstance(item, dict) and "name" in item:
                        out.append({"name": item["name"], "role": item.get("role", "GHST Doctor")})
                    elif isinstance(item, str):
                        out.append({"name": item, "role": "GHST Doctor"})
                if out:
                    logger.info("Loaded %d GHSTs from %s", len(out), p)
                    return out
            else:
                out = []
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        out.append({"name": line, "role": "GHST Doctor"})
                if out:
                    logger.info("Loaded %d GHSTs from %s", len(out), p)
                    return out
        except Exception as exc:
            logger.warning("Could not read ghost list %s: %s", p, exc)

    # Fallback synthetic personas
    fields = (
        "Automated Code Cleaner",
        "Syntax Specialist",
        "Dependency Wrangler",
        "Style & Lint",
        "Repository Steward",
        "Test Strategist",
        "Refactorer",
        "Merge Whisperer",
        "Type System Guru",
    )
    base = [
        "Dr. TidyCode",
        "Dr. Syntax",
        "Dr. ImportOrder",
        "Dr. Formatter",
        "Dr. Archivist",
    ]
    out = []
    for n in base:
        out.append({"name": n, "role": random.choice(fields)})
    logger.info("Using fallback GHST list (%d entries)", len(out))
    return out


EMOJI_POOL = [
    # ghostly icons
    "👻",
    "🕯️",
    "🔮",
    "🪄",
    "🪦",
    "🧿",
    "🦴",
    "👁️",
    "👾",
    "👽",
    # utility
    "🛠️",
    "🧹",
    "🧠",
    "🔬",
    "🧪",
    "🕵️",
    "🧩",
    "⚙️",
    "🔧",
    "🧭",
    "📚",
    "📈",
    "🧰",
    "💡",
    "🎯",
    "🪙",
    "🧬",
]


def assign_unique_emojis(personas: List[Dict[str, str]]) -> Dict[str, str]:
    """Deterministically assign an emoji to each persona name.

    Returns mapping name -> emoji.
    """
    pool = EMOJI_POOL.copy()
    used = set()
    mapping: Dict[str, str] = {}
    for p in personas:
        name = p["name"]
        h = int(sha256(name.encode("utf-8")).hexdigest(), 16)
        idx = h % len(pool)
        # find next unused emoji
        for shift in range(len(pool)):
            cand = pool[(idx + shift) % len(pool)]
            if cand not in used:
                mapping[name] = cand
                used.add(cand)
                break
        else:
            mapping[name] = "👻"
    return mapping


def run_fixer_subprocess(dry_run: bool = False) -> int:
    """Run the older fixer script (fix_all_errors.py) as a subprocess.

    Returns subprocess exit code.
    """
    cmd = [sys.executable, "fix_all_errors.py"]
    env = os.environ.copy()
    if dry_run:
        env["GHST_DRY_RUN"] = "1"
    # Force UTF-8 in child Python processes to avoid Windows console encoding issues
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    logger.info("Invoking fixer (dry_run=%s)", dry_run)
    try:
        proc = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            env=env,
            encoding='utf-8',
            errors='replace',
        )
        if proc.stdout:
            logger.info(proc.stdout)
        if proc.stderr:
            logger.warning(proc.stderr)
        return proc.returncode
    except Exception as exc:
        logger.error("Failed to run fixer: %s", exc)
        return 2


def ensure_tools(dry_run: bool = False) -> bool:
    """Ensure autopep8 and isort are installed (install if allowed).

    Returns True if tools are available or were installed.
    """
    ok = True
    try:
        import importlib

        def has(m: str) -> bool:
            try:
                return importlib.util.find_spec(m) is not None
            except Exception:
                return False

        if not has("autopep8"):
            if dry_run:
                logger.info("(dry-run) Would install autopep8")
            else:
                logger.info("Installing autopep8...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "autopep8"])
        else:
            logger.info("autopep8 present")

        if not has("isort"):
            if dry_run:
                logger.info("(dry-run) Would install isort")
            else:
                logger.info("Installing isort...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "isort"])
        else:
            logger.info("isort present")
    except Exception as exc:
        logger.warning("Tool installation check failed: %s", exc)
        ok = False
    return ok


def get_python_files() -> List[Path]:
    """Collect Python files to operate on conservatively."""
    files: List[Path] = []
    # include common top-level candidates
    main_candidates = (
        "ghst_installer_beautiful.py",
        "ghst_installer_enhanced.py",
        "build_beautiful_optimized.py",
        "release_manager.py",
        "install_wizard.py",
    )
    for name in main_candidates:
        p = Path(name)
        if p.exists():
            files.append(p)
    core = Path("core")
    if core.exists():
        files.extend([p for p in core.rglob("*.py") if p.is_file()])
    scripts = Path("scripts")
    if scripts.exists():
        files.extend([p for p in scripts.rglob("*.py") if p.is_file()])
    files.extend([p for p in Path(".").glob("*.py") if p.is_file() and p.name != Path(__file__).name])
    # dedupe
    seen = set()
    ordered: List[Path] = []
    for p in files:
        sp = str(p.resolve())
        if sp not in seen:
            seen.add(sp)
            ordered.append(p)
    return ordered


def fix_file(file_path: Path, dry_run: bool = False) -> bool:
    """Run autopep8 and isort on a file. Returns True if attempted."""
    logger.info("🔧 Fixing %s", file_path)
    autopep8_cmd = [
        sys.executable,
        "-m",
        "autopep8",
        "--in-place",
        "--aggressive",
        "--aggressive",
        "--max-line-length=79",
        str(file_path),
    ]
    isort_cmd = [
        sys.executable,
        "-m",
        "isort",
        "--line-length=79",
        "--multi-line=3",
        "--trailing-comma",
        "--combine-as",
        str(file_path),
    ]
    if dry_run:
        logger.info("(dry-run) Would run: %s", " ".join(autopep8_cmd))
        logger.info("(dry-run) Would run: %s", " ".join(isort_cmd))
        return True
    try:
        try:
            r1 = subprocess.run(autopep8_cmd, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            logger.warning("autopep8 timed out for %s", file_path)
            r1 = None
        if r1 is None:
            logger.warning("autopep8 did not complete for %s", file_path)
        elif r1.returncode == 0:
            logger.info("autopep8 applied")
        else:
            logger.warning("autopep8 stderr: %s", (r1.stderr or "").strip())
        try:
            r2 = subprocess.run(isort_cmd, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            logger.warning("isort timed out for %s", file_path)
            r2 = None
        if r2 is None:
            logger.warning("isort did not complete for %s", file_path)
        elif r2.returncode == 0:
            logger.info("isort applied")
        else:
            logger.warning("isort stderr: %s", (r2.stderr or "").strip())
        return True
    except Exception as exc:
        logger.error("Error fixing %s: %s", file_path, exc)
        return False


def run_cycle(dry_run: bool = False) -> int:
    """Run one fixer cycle and return count of files processed."""
    logger.info("🚀 Dr. TidyCode running fix cycle")
    if not ensure_tools(dry_run=dry_run):
        logger.error("Required tools missing or failed to install")
        return 0
    files = get_python_files()
    logger.info("Found %d Python files to process", len(files))
    count = 0
    for p in files:
        ok = fix_file(p, dry_run=dry_run)
        if ok:
            count += 1
    logger.info("Completed cycle: %d/%d files processed", count, len(files))
    return count


def show_personas(personas: List[Dict[str, str]], emoji_map: Dict[str, str]) -> None:
    logger.info("PhD GHST Think Tank: Active Personas")
    for p in personas:
        name = p["name"]
        role = p.get("role", "GHST Doctor")
        emoji = emoji_map.get(name, "👻")
        logger.info("  %s  %s — %s", emoji, name, role)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="GHST Fix-All-Errors Daemon (Dr. TidyCode)")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuously as daemon")
    parser.add_argument("--interval-hours", type=float, default=24.0, help="Interval between runs when daemonized")
    parser.add_argument("--dry-run", action="store_true", help="Do not modify files; only preview actions")
    args = parser.parse_args()
    personas = load_ghost_list()
    emoji_map = assign_unique_emojis(personas)
    show_personas(personas, emoji_map)
    # If a legacy fixer script exists, prefer running it; otherwise run internal cycle
    legacy = Path("fix_all_errors.py")
    if args.once:
        if legacy.exists():
            return run_fixer_subprocess(dry_run=args.dry_run)
        else:
            run_cycle(dry_run=args.dry_run)
            return 0
    if not args.daemon:
        # default: run once
        if legacy.exists():
            return run_fixer_subprocess(dry_run=args.dry_run)
        run_cycle(dry_run=args.dry_run)
        return 0
    # Daemon mode
    logger.info("Starting Dr. TidyCode daemon (interval_hours=%s)", args.interval_hours)
    try:
        while True:
            if legacy.exists():
                run_fixer_subprocess(dry_run=args.dry_run)
            else:
                run_cycle(dry_run=args.dry_run)
            logger.info("Sleeping for %s hour(s)", args.interval_hours)
            time.sleep(int(args.interval_hours * 3600))
    except KeyboardInterrupt:
        logger.info("Dr. TidyCode shutting down")
        return 0


if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
GHST Fix-All-Errors Daemon — Dr. TidyCode (PhD GHST)
Wraps `fix_all_errors.py` as a GHST persona daemon. Assigns unique ghost emoji
per persona (from a ghost generator or local fallback) and runs the fixer on a
schedule or once. Logging is UTF-8 safe.
"""

import sys
import os
import time
import argparse
import subprocess
import logging
import io
import json
import random
from pathlib import Path
from hashlib import sha256

# UTF-8 safe logging handlers
_stdout_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
file_handler = logging.FileHandler('fix_all_errors_daemon.log', encoding='utf-8')
stream_handler = logging.StreamHandler(_stdout_stream)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger('fix_all_errors_daemon')


def load_ghost_list() -> list:
    """Load ghost/persona names from a generator or local fallback.

    Tries a few common locations. Returns a list of dicts: {'name':..., 'role':...}
    """
    candidates = []

    # First try to import an in-repo ghost generator module (best source)
    for mod_path in ('src.ai_collaboration.ghost_generator', 'ai_collaboration.ghost_generator', 'ghost_generator'):
        try:
            mod = __import__(mod_path, fromlist=['*'])
            # try known accessors
            for accessor in ('generate_ghosts', 'get_ghosts', 'get_ghost_list', 'load_ghosts', 'ghost_list', 'ghosts'):
                val = getattr(mod, accessor, None)
                if callable(val):
                    try:
                        data = val()
                    except TypeError:
                        data = val
                    if isinstance(data, list) and data:
                        candidates = []
                        for item in data:
                            if isinstance(item, dict) and 'name' in item:
                                candidates.append({'name': item['name'], 'role': item.get('role', 'GHST Doctor')})
                            elif isinstance(item, str):
                                candidates.append({'name': item, 'role': 'GHST Doctor'})
                        if candidates:
                            logger.info(f"Loaded {len(candidates)} GHSTs from generator module {mod_path}.{accessor}")
                            return candidates
                elif isinstance(val, list) and val:
                    candidates = []
                    for item in val:
                        if isinstance(item, dict) and 'name' in item:
                            candidates.append({'name': item['name'], 'role': item.get('role', 'GHST Doctor')})
                        elif isinstance(item, str):
                            candidates.append({'name': item, 'role': 'GHST Doctor'})
                    if candidates:
                        logger.info(f"Loaded {len(candidates)} GHSTs from generator module {mod_path}.{accessor}")
                        return candidates
        except Exception:
            pass

    # Try common ghost list files
    possible = [
        Path('ghosts/ghost_list.json'),
        Path('ghosts/ghost_list.txt'),
        Path('.ghost_list.json'),
        Path('.github/ghost_list.txt')
    ]

    for p in possible:
        if p.exists():
            try:
                if p.suffix == '.json':
                    with open(p, 'r', encoding='utf-8', errors='replace') as f:
                        data = json.load(f)
                        for item in data:
                            if isinstance(item, dict) and 'name' in item:
                                candidates.append({'name': item['name'], 'role': item.get('role', 'GHST Doctor')})
                            elif isinstance(item, str):
                                candidates.append({'name': item, 'role': 'GHST Doctor'})
                else:
                    with open(p, 'r', encoding='utf-8', errors='replace') as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            candidates.append({'name': line, 'role': 'GHST Doctor'})
                logger.info(f"Loaded {len(candidates)} GHSTs from {p}")
                return candidates
            except Exception as e:
                logger.warning(f"Could not read ghost list {p}: {e}")

    # Fallback: synthesize a small PhD think-tank of personas with varied fields
    fields = [
        'Automated Code Cleaner', 'Syntax Specialist', 'Dependency Wrangler',
        'Style & Lint', 'Repository Steward', 'Test Strategist', 'Refactorer',
        'Merge Whisperer', 'Type System Guru'
    ]

    fallback = []
    base_names = ['Dr. TidyCode', 'Dr. Syntax', 'Dr. ImportOrder', 'Dr. Formatter', 'Dr. Archivist']
    for i, n in enumerate(base_names):
        fallback.append({'name': n, 'role': random.choice(fields)})

    logger.info(f"Using fallback GHST list ({len(fallback)} entries)")
    return fallback


EMOJI_POOL = [
    # ghostly / spectral / magical icons first
    '👻', '🕯️', '🔮', '🪄', '🪦', '🧿', '🦴', '👁️', '👾', '👽',
    # utility icons
    '🛠️', '🧹', '🧠', '🔬', '🧪', '🕵️', '🧩', '⚙️', '🔧', '🧭',
    '📚', '📈', '🧰', '💡', '🎯', '🪙', '🧬'
]


def assign_unique_emojis(personas: list) -> dict:
    """Deterministically assign a unique emoji to each persona name.

    Returns mapping name -> emoji. If collisions occur, it picks the next free emoji.
    """
    used = set()
    mapping = {}
    pool = EMOJI_POOL.copy()

    for p in personas:
        name = p['name']
        h = int(sha256(name.encode('utf-8')).hexdigest(), 16)
        idx = h % len(pool)
        # find an unused emoji
        for shift in range(len(pool)):
            candidate = pool[(idx + shift) % len(pool)]
            if candidate not in used:
                mapping[name] = candidate
                used.add(candidate)
                break
        else:
            # fallback to a simple marker
            mapping[name] = '👻'

    return mapping


def run_fixer(dry_run: bool = False) -> int:
    """Invoke the fix_all_errors script as a subprocess. Returns exit code."""
    cmd = [sys.executable, 'fix_all_errors.py']
    env = os.environ.copy()
    if dry_run:
        # signal dry-run to the fixer via env var (fixer may ignore it)
        env['GHST_DRY_RUN'] = '1'

    logger.info(f"Invoking fixer (dry_run={dry_run})")
    try:
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
        logger.info(proc.stdout)
        if proc.stderr:
            logger.warning(proc.stderr)
        return proc.returncode
    except Exception as e:
        logger.error(f"Failed to run fixer: {e}")
        return 2


def show_personas(personas: list, emoji_map: dict):
    logger.info("PhD GHST Think Tank: Active Personas")
    for p in personas:
        name = p['name']
        role = p.get('role', 'GHST Doctor')
        emoji = emoji_map.get(name, '👻')
        logger.info(f"  {emoji}  {name} — {role}")


def daemon_loop(interval_minutes: int, dry_run: bool):
    personas = load_ghost_list()
    emoji_map = assign_unique_emojis(personas)
    show_personas(personas, emoji_map)

    logger.info(f"Starting GHST Fix-All-Errors daemon (interval={interval_minutes}m)")
    try:
        while True:
            logger.info("Daemon wake: running fixer cycle")
            code = run_fixer(dry_run=dry_run)
            if code == 0:
                logger.info("Fixer completed successfully")
            else:
                logger.warning(f"Fixer exited with code {code}")
            logger.info(f"Sleeping for {interval_minutes} minute(s)")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        logger.info("Daemon interrupted, exiting")


def main():
    parser = argparse.ArgumentParser(description='GHST Fix-All-Errors Daemon (Dr. TidyCode)')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (do not modify files)')
    parser.add_argument('--interval', type=int, default=60, help='Interval in minutes between runs')

    args = parser.parse_args()

    personas = load_ghost_list()
    emoji_map = assign_unique_emojis(personas)
    show_personas(personas, emoji_map)

    if args.once:
        logger.info('Running one-off fixer invocation')
        rc = run_fixer(dry_run=args.dry_run)
        sys.exit(rc)
    else:
        daemon_loop(args.interval, args.dry_run)


if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
GHST Fix-All-Errors Daemon (GHST Persona)
----------------------------------------

Daemonized GHST persona that periodically runs the repository-wide fixer
(`fix_all_errors` functionality) to apply formatting and import-sort fixes.
Provides a --once mode and a safe --dry-run to preview changes.

Persona: Dr. TidyCode (PhD, Software Hygiene)
 - Focus: Code quality, lint cleanup, import hygiene, consistent formatting
 - Behavior: non-destructive by default; can run once or as a periodic daemon
"""

import sys
import time
import argparse
import logging
import io
import subprocess
from pathlib import Path
from typing import List

# UTF-8 safe logging
_stdout_stream = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
file_handler = logging.FileHandler('fix_all_errors_daemon.log', encoding='utf-8')
stream_handler = logging.StreamHandler(_stdout_stream)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[file_handler, stream_handler]
)
logger = logging.getLogger('ghst.fix_all_errors')


def is_tool_installed(module_name: str) -> bool:
    try:
        import importlib
        return importlib.util.find_spec(module_name) is not None
    except Exception:
        return False


def install_package(package: str) -> bool:
    """Install a Python package via pip"""
    try:
        logger.info(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        logger.info(f"✅ {package} installed")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install {package}: {e}")
        return False


def ensure_tools(dry_run: bool = False) -> bool:
    """Ensure autopep8 and isort are available (install if missing)"""
    tools_ok = True
    if not is_tool_installed('autopep8'):
        if dry_run:
            logger.info("(dry-run) Would install autopep8")
            tools_ok = tools_ok and True
        else:
            tools_ok = tools_ok and install_package('autopep8')
    else:
        logger.info("✅ autopep8 present")

    if not is_tool_installed('isort'):
        if dry_run:
            logger.info("(dry-run) Would install isort")
            tools_ok = tools_ok and True
        else:
            tools_ok = tools_ok and install_package('isort')
    else:
        logger.info("✅ isort present")

    return tools_ok


def get_python_files() -> List[Path]:
    """Collect Python files to fix (non-recursive lists + core/scripts)"""
    files: List[Path] = []

    # A conservative list of top-level installer/manager files
    main_candidates = [
        'ghst_installer_beautiful.py',
        'ghst_installer_enhanced.py',
        'build_beautiful_optimized.py',
        'release_manager.py',
        'install_wizard.py'
    ]

    for name in main_candidates:
        p = Path(name)
        if p.exists():
            files.append(p)

    # core/*.py
    core = Path('core')
    if core.exists():
        files.extend([p for p in core.rglob('*.py') if p.is_file()])

    # scripts/*.py
    scripts = Path('scripts')
    if scripts.exists():
        files.extend([p for p in scripts.rglob('*.py') if p.is_file()])

    # also include top-level python files
    files.extend([p for p in Path('.').glob('*.py') if p.is_file() and p.name not in ('fix_all_errors_daemon.py',)])

    # Deduplicate while preserving order
    seen = set()
    ordered = []
    for p in files:
        sp = str(p.resolve())
        if sp not in seen:
            seen.add(sp)
            ordered.append(p)
    return ordered


def fix_file(file_path: Path, dry_run: bool = False) -> bool:
    """Apply autopep8 and isort to a single file (or show planned commands in dry-run)"""
    logger.info(f"🔧 Fixing {file_path}")

    autopep8_cmd = [
        sys.executable, '-m', 'autopep8',
        '--in-place', '--aggressive', '--aggressive',
        '--max-line-length=79', str(file_path)
    ]

    isort_cmd = [
        sys.executable, '-m', 'isort',
        '--line-length=79', '--multi-line=3', '--trailing-comma',
        '--combine-as', str(file_path)
    ]

    if dry_run:
        logger.info(f"(dry-run) Would run: {' '.join(autopep8_cmd)}")
        logger.info(f"(dry-run) Would run: {' '.join(isort_cmd)}")
        return True

    try:
        # add timeouts to avoid hangs; keep generous but bounded
        try:
            r1 = subprocess.run(autopep8_cmd, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            logger.warning(f"  ⚠️ autopep8 timed out for {file_path}")
            r1 = None

        if r1 is None:
            logger.warning("  ⚠️ autopep8 did not complete")
        elif r1.returncode == 0:
            logger.info("  ✅ autopep8 applied")
        else:
            logger.warning(f"  ⚠️ autopep8 stderr: {r1.stderr.strip()}")

        try:
            r2 = subprocess.run(isort_cmd, capture_output=True, text=True, timeout=60)
        except subprocess.TimeoutExpired:
            logger.warning(f"  ⚠️ isort timed out for {file_path}")
            r2 = None

        if r2 is None:
            logger.warning("  ⚠️ isort did not complete")
        elif r2.returncode == 0:
            logger.info("  ✅ isort applied")
        else:
            logger.warning(f"  ⚠️ isort stderr: {r2.stderr.strip()}")

        return True
    except Exception as e:
        logger.error(f"  ❌ Error fixing {file_path}: {e}")
        return False


def run_cycle(dry_run: bool = False) -> int:
    """Run a single fix cycle. Returns number of files fixed/planned."""
    logger.info("🚀 Dr. TidyCode running fix cycle")

    if not ensure_tools(dry_run=dry_run):
        logger.error("Required tools missing and could not be installed")
        return 0

    files = get_python_files()
    logger.info(f"📁 Found {len(files)} Python files to process")

    count = 0
    for p in files:
        ok = fix_file(p, dry_run=dry_run)
        if ok:
            count += 1
    logger.info(f"✅ Completed cycle: {count}/{len(files)} files processed")
    return count


def main():
    parser = argparse.ArgumentParser(description='GHST Fix-All-Errors Daemon (Dr. TidyCode)')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--daemon', action='store_true', help='Run continuously as daemon')
    parser.add_argument('--interval-hours', type=float, default=24.0, help='Interval between runs when daemonized')
    parser.add_argument('--dry-run', action='store_true', help='Do not modify files; only preview actions')

    args = parser.parse_args()

    if args.once or not args.daemon:
        # Run once
        success_count = run_cycle(dry_run=args.dry_run)
        return 0 if success_count >= 0 else 1

    # Daemon mode
    logger.info("🛡️ Starting Dr. TidyCode daemon")
    try:
        while True:
            run_cycle(dry_run=args.dry_run)
            logger.info(f"⏳ Sleeping for {args.interval_hours} hour(s)")
            time.sleep(int(args.interval_hours * 3600))
    except KeyboardInterrupt:
        logger.info("👋 Dr. TidyCode shutting down")
        return 0


if __name__ == '__main__':
    code = main()
    sys.exit(code)
