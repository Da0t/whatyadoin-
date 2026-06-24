"""Database test — save a session and read it back."""
from whatyoudoin import db


def test_save_and_get_roundtrip():
    conn = db.connect(":memory:")
    sid = db.save_session(conn, "buggy.py", "it crashes sometimes", "fix line 3")
    row = db.get_session(conn, sid)
    assert row["file_path"] == "buggy.py"
    assert row["transcript"] == "it crashes sometimes"
    assert row["response"] == "fix line 3"
