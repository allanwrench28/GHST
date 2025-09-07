"""Small .env loader used by GHST (optional).

This utility reads a simple KEY=VALUE `.env` file and sets environment
variables for the current process. It's intentionally tiny to avoid adding
external deps. It will not override existing environment values unless
force=True.

Usage:
    from core.src.ai_collaboration.env_loader import load_dotenv
    load_dotenv('.env')

"""
from __future__ import annotations

from pathlib import Path
import os
from typing import Optional


def load_dotenv(path: Optional[str] = None, force: bool = False) -> None:
    """Load environment variables from a file at `path`.

    The file should contain lines like `KEY=VALUE`. Lines starting with `#`
    are ignored.
    """
    p = Path(path or Path.cwd() / '.env')
    if not p.exists():
        return

    for raw in p.read_text(encoding='utf8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        key, val = line.split('=', 1)
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        if not force and key in os.environ:
            continue
        os.environ[key] = val
