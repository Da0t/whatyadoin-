from whatyoudoin import db


def test_save_then_latest_returns_it():
    conn = db.connect(":memory:")
    db.save_session(conn, "(project)", "what's wrong?", "FILE: a.py\n```\nx = 1\n```")
    last = db.latest_session(conn)
    assert last["transcript"] == "what's wrong?"
    assert "a.py" in last["response"]


def test_all_sessions_returns_every_row_newest_first():
    conn = db.connect(":memory:")
    db.save_session(conn, "(project)", "first", "FILE: a.py\n```\nx = 1\n```")
    db.save_session(conn, "(project)", "second", "FILE: b.py\n```\ny = 2\n```")
    rows = db.all_sessions(conn)
    assert [r["transcript"] for r in rows] == ["second", "first"]
