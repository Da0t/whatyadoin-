"""Scanner tests — mistakes.scan is pure, so these run without any API keys."""
from whatyoudoin import db, mistakes


def test_flags_em_dash_overuse():
    code = "x = 1  # a — b — c — d — e\n"
    cats = {f["category"] for f in mistakes.scan(code)}
    assert "em_dash_overuse" in cats


def test_flags_generic_names():
    found = {f["category"]: f for f in mistakes.scan("data = 1\nresult = 2\n")}
    assert found["generic_names"]["count"] == 2


def test_flags_ai_comment_phrases():
    cats = {f["category"] for f in mistakes.scan("y = 2  # Note that this is fine\n")}
    assert "ai_comment_phrases" in cats


def test_clean_code_has_no_findings():
    assert mistakes.scan("total = price * quantity\n") == []


def test_save_mistakes_roundtrips_to_db():
    conn = db.connect(":memory:")
    saved = db.save_mistakes(conn, None, "buggy.py", mistakes.scan("data = 1\nresult = 2\n"))
    assert saved == 1
    row = conn.execute("SELECT category, count FROM mistakes").fetchone()
    assert row["category"] == "generic_names" and row["count"] == 2
