"""SQLite storage for past fix sessions and the vibe-code tells found in them.

Fully implemented and the target of the database unit tests.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".whatyoudoin" / "history.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    file_path  TEXT NOT NULL,
    transcript TEXT NOT NULL,
    response   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS mistakes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    created_at TEXT NOT NULL,
    file_path  TEXT NOT NULL,
    category   TEXT NOT NULL,
    detail     TEXT NOT NULL,
    count      INTEGER NOT NULL
);
"""


def connect(db_path=DEFAULT_DB_PATH):
    """Open a connection and ensure the tables exist. Pass ':memory:' for tests."""
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def save_session(conn, file_path: str, transcript: str, response: str) -> int:
    """Insert one fix session and return its new id."""
    cur = conn.execute(
        "INSERT INTO sessions (created_at, file_path, transcript, response) VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(timespec="seconds"), file_path, transcript, response),
    )
    conn.commit()
    return cur.lastrowid


def save_mistakes(conn, session_id, file_path: str, findings: list[dict]) -> int:
    """Log each vibe-code finding from mistakes.scan(); return how many were saved."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn.executemany(
        "INSERT INTO mistakes (session_id, created_at, file_path, category, detail, count) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        [(session_id, now, file_path, f["category"], f["detail"], f["count"]) for f in findings],
    )
    conn.commit()
    return len(findings)


def get_session(conn, session_id: int) -> dict | None:
    """Return one full session by id, or None if it doesn't exist."""
    row = conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()
    return dict(row) if row else None
