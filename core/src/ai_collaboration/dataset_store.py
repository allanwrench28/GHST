"""Simple SQLite-backed dataset store for MoE examples.

Stores prompt, scrubbed, expert_outputs (as JSON), and timestamp. Lightweight
API: save_example(dict) and load_last(n).
"""

import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, List
import datetime


DB_PATH = Path(__file__).resolve().parents[2] / "data" / "ghst_dataset.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def _get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(
        """CREATE TABLE IF NOT EXISTS examples (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT,
        prompt TEXT,
        scrubbed TEXT,
        expert_outputs TEXT
        )"""
    )
    conn.commit()
    return conn


def save_example(example: Dict[str, Any]) -> None:
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO examples (ts, prompt, scrubbed, expert_outputs) VALUES (?, ?, ?, ?)",
            (
                datetime.datetime.utcnow().isoformat(),
                example.get("prompt"),
                example.get("scrubbed"),
                json.dumps(example.get("expert_outputs", {})),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def load_last(n: int = 10) -> List[Dict[str, Any]]:
    conn = _get_conn()
    try:
        cur = conn.execute(
            "SELECT ts, prompt, scrubbed, expert_outputs FROM examples ORDER BY id DESC LIMIT ?",
            (n,),
        )
        rows = cur.fetchall()
        out = []
        for ts, prompt, scrubbed, expert_outputs in rows:
            out.append(
                {
                    "ts": ts,
                    "prompt": prompt,
                    "scrubbed": scrubbed,
                    "expert_outputs": json.loads(expert_outputs or "{}"),
                }
            )
        return out
    finally:
        conn.close()
