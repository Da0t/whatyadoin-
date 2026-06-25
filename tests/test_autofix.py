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


def test_autofix_runs_diagnoses_and_applies(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "buggy.py"
    target.write_text("x = 1 / 0\n")

    def fake_run_script(path, timeout=20):
        return (1, "", "ZeroDivisionError: division by zero")

    conn = db.connect(":memory:")
    cli._autofix_from_crash(
        str(target), run_script=fake_run_script, client=_fake_client(), conn=conn
    )

    assert target.read_text() == "x = 1\n"
    assert (tmp_path / "buggy.py.bak").read_text() == "x = 1 / 0\n"
    last = db.latest_session(conn)
    assert last["file_path"] == "(crash)"
    assert "ZeroDivisionError" in last["transcript"]
