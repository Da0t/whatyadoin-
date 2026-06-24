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
"""


def connect(db_path=DEFAULT_DB_PATH):
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def save_session(conn, file_path: str, transcript: str, response: str) -> int:
    cur = conn.execute(
        "INSERT INTO sessions (created_at, file_path, transcript, response) VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(timespec="seconds"), file_path, transcript, response),
    )
    conn.commit()
    return cur.lastrowid


def latest_session(conn) -> dict | None:
    row = conn.execute("SELECT * FROM sessions ORDER BY id DESC LIMIT 1").fetchone()
    return dict(row) if row else None
