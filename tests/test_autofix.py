from whatyoudoin import __main__ as cli, db

REPLY = "FILE: buggy.py\n```\nx = 1\n```\nGuarded the division so it stops dividing by zero."


def _fake_client():
    class Block:
        type = "text"
        text = REPLY

    class Response:
        content = [Block()]

    class FakeClient:
        class messages:
            @staticmethod
            def create(**kwargs):
                return Response()

    return FakeClient()


def test_autofix_runs_diagnoses_applies_and_verifies(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "buggy.py"
    target.write_text("x = 1 / 0\n")

    # First run crashes; the post-fix re-run is clean.
    runs = iter([(1, "", "ZeroDivisionError: division by zero"), (0, "", "")])

    def fake_run_script(path, timeout=20):
        return next(runs)

    conn = db.connect(":memory:")
    cli._autofix_from_crash(
        str(target), run_script=fake_run_script, client=_fake_client(), conn=conn
    )

    assert target.read_text() == "x = 1\n"
    assert (tmp_path / "buggy.py.bak").read_text() == "x = 1 / 0\n"
    last = db.latest_session(conn)
    assert last["file_path"] == "(crash)"
    assert "ZeroDivisionError" in last["transcript"]


def test_autofix_does_nothing_when_script_runs_clean(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "fine.py"
    target.write_text("print('ok')\n")

    def fake_run_script(path, timeout=20):
        return (0, "ok\n", "")

    conn = db.connect(":memory:")
    cli._autofix_from_crash(
        str(target), run_script=fake_run_script, client=_fake_client(), conn=conn
    )

    # Untouched, no backup written, nothing recorded.
    assert target.read_text() == "print('ok')\n"
    assert not (tmp_path / "fine.py.bak").exists()
    assert db.latest_session(conn) is None
