from whatyoudoin import runner


def test_run_script_reports_a_crash(tmp_path):
    script = tmp_path / "boom.py"
    script.write_text("raise ValueError('boom')\n")
    code, out, err = runner.run_script(str(script))
    assert code != 0
    assert "ValueError" in err


def test_command_for_picks_interpreter_by_extension():
    assert runner._command_for("app.js") == ["node", "app.js"]
    assert runner._command_for("main.go") == ["go", "run", "main.go"]
    assert runner._command_for("mystery.zig") is None


def test_run_script_runs_a_non_python_language(tmp_path):
    script = tmp_path / "boom.sh"
    script.write_text("echo oops >&2\nexit 7\n")
    code, out, err = runner.run_script(str(script))
    assert code == 7
    assert "oops" in err


def test_run_script_rejects_unknown_language(tmp_path):
    script = tmp_path / "mystery.zig"
    script.write_text("// who knows\n")
    code, out, err = runner.run_script(str(script))
    assert code != 0
    assert "zig" in err.lower()
