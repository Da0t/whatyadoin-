"""SQLite storage for past sessions.

Fully implemented — local persistence layer and the target of the database
unit tests. Each explain/fix run is one row.
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
    mode       TEXT NOT NULL,
    file_path  TEXT NOT NULL,
    transcript TEXT NOT NULL,
    response   TEXT NOT NULL
);
"""


def connect(db_path=DEFAULT_DB_PATH):
    """Open a connection and make sure the table exists.

    Pass ":memory:" for a throwaway in-memory database (used by the tests).
    """
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def save_session(conn, mode: str, file_path: str, transcript: str, response: str) -> int:
    """Insert one session ('explain' or 'fix') and return its new id."""
    cur = conn.execute(
        "INSERT INTO sessions (created_at, mode, file_path, transcript, response) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            mode,
            file_path,
            transcript,
            response,
        ),
    )
    conn.commit()
    return cur.lastrowid


def list_sessions(conn, limit: int = 20) -> list[dict]:
    """Return recent sessions, newest first (without the full response text)."""
    rows = conn.execute(
        "SELECT id, created_at, mode, file_path, transcript "
        "FROM sessions ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_session(conn, session_id: int) -> dict | None:
    """Return one full session by id, or None if it doesn't exist."""
    row = conn.execute(
        "SELECT * FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()
    return dict(row) if row else None
