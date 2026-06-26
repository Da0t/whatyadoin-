from whatyoudoin import __main__ as cli


def test_gather_collects_multiple_languages(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "app.py").write_text("print('hi')\n")
    (tmp_path / "server.js").write_text("console.log('hi')\n")
    (tmp_path / "main.go").write_text("package main\n")
    (tmp_path / "notes.txt").write_text("ignore me\n")
    skipped = tmp_path / "node_modules"
    skipped.mkdir()
    (skipped / "dep.js").write_text("module.exports = {}\n")

    bundle = cli._gather()

    assert "app.py" in bundle
    assert "server.js" in bundle
    assert "main.go" in bundle
    assert "notes.txt" not in bundle   # not a source file
    assert "dep.js" not in bundle      # inside node_modules, skipped
