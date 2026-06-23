"""Database tests — db.py is fully implemented, so these pass as-is."""
from whatyoudoin import db


def test_save_and_get_roundtrip():
    conn = db.connect(":memory:")
    sid = db.save_session(conn, "explain", "buggy.py", "it crashes sometimes", "fix line 3")
    row = db.get_session(conn, sid)
    assert row["mode"] == "explain"
    assert row["file_path"] == "buggy.py"
    assert row["transcript"] == "it crashes sometimes"
    assert row["response"] == "fix line 3"


def test_list_returns_newest_first():
    conn = db.connect(":memory:")
    db.save_session(conn, "explain", "a.py", "t1", "r1")
    second = db.save_session(conn, "fix", "b.py", "t2", "r2")
    rows = db.list_sessions(conn)
    assert rows[0]["id"] == second


def test_get_missing_returns_none():
    conn = db.connect(":memory:")
    assert db.get_session(conn, 999) is None
