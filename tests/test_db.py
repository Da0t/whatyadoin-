from whatyoudoin import db


def test_save_then_latest_returns_it():
    conn = db.connect(":memory:")
    db.save_session(conn, "(project)", "what's wrong?", "FILE: a.py\n```\nx = 1\n```")
    last = db.latest_session(conn)
    assert last["transcript"] == "what's wrong?"
    assert "a.py" in last["response"]
