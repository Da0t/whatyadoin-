"""Scanner tests — pure, no API keys needed."""
from whatyoudoin import db, mistakes


def test_flags_em_dash_overuse():
    code = "x = 1  # a — b — c — d — e\n"
    cats = {f["category"] for f in mistakes.scan(code)}
    assert "em_dash_overuse" in cats


def test_save_mistakes_roundtrips_to_db():
    conn = db.connect(":memory:")
    saved = db.save_mistakes(conn, None, "buggy.py", mistakes.scan("data = 1\nresult = 2\n"))
    assert saved == 1
    row = conn.execute("SELECT category, count FROM mistakes").fetchone()
    assert row["category"] == "generic_names" and row["count"] == 2
