#!/usr/bin/env python3
"""
GHST Feedback Manager
====================
Handles feedback weights, conflict resolution, and SQLite persistence.
"""
import sqlite3
from datetime import datetime

DB_PATH = "ghst_feedback.db"

class FeedbackManager:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT,
            angle TEXT,
            weight REAL,
            timestamp TEXT,
            complexity REAL
        )
        """)
        self.conn.commit()

    def add_feedback(self, project_id, angle, weight, complexity):
        ts = datetime.now().isoformat()
        c = self.conn.cursor()
        c.execute("""
        INSERT INTO feedback (project_id, angle, weight, timestamp, complexity)
        VALUES (?, ?, ?, ?, ?)
        """, (project_id, angle, weight, ts, complexity))
        self.conn.commit()

    def resolve_conflict(self, project_id1, project_id2, angle):
        c = self.conn.cursor()
        c.execute("""
        SELECT weight, timestamp, complexity FROM feedback
        WHERE project_id IN (?, ?) AND angle = ?
        """, (project_id1, project_id2, angle))
        rows = c.fetchall()
        if not rows or len(rows) < 2:
            return None
        # Recency fallback
        w1, t1, c1 = rows[0]
        w2, t2, c2 = rows[1]
        if t1 > t2:
            return w1
        elif t2 > t1:
            return w2
        else:
            return w1 if c1 > c2 else w2

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    fm = FeedbackManager()
    fm.add_feedback("proj1", "cost", 0.75, 0.8)
    fm.add_feedback("proj2", "cost", 0.2, 0.6)
    resolved = fm.resolve_conflict("proj1", "proj2", "cost")
    print(f"Resolved weight: {resolved}")
    fm.close()
