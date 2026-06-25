from whatyoudoin import runner


def test_run_script_reports_a_crash(tmp_path):
    script = tmp_path / "boom.py"
    script.write_text("raise ValueError('boom')\n")
    code, out, err = runner.run_script(str(script))
    assert code != 0
    assert "ValueError" in err


def test_run_script_reports_a_clean_run(tmp_path):
    script = tmp_path / "ok.py"
    script.write_text("print('hello')\n")
    code, out, err = runner.run_script(str(script))
    assert code == 0
    assert "hello" in out
