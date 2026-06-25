from whatyoudoin import diagnose

REPLY = "FILE: buggy.py\n```python\nprint('ok')\n```\n## What I changed\nFixed the typo."


def test_extract_filename():
    assert diagnose.extract_filename(REPLY) == "buggy.py"


def test_extract_code():
    assert diagnose.extract_code(REPLY) == "print('ok')\n"


def test_extract_summary_pulls_first_explanation_line():
    assert diagnose.extract_summary(REPLY) == "What I changed"


def test_extract_summary_handles_missing_block():
    assert diagnose.extract_summary("no code here") == "no code here"


def test_build_error_transcript_includes_file_and_error():
    transcript = diagnose.build_error_transcript(
        "buggy.py", "ZeroDivisionError: division by zero"
    )
    assert "buggy.py" in transcript
    assert "ZeroDivisionError" in transcript
    assert "fix it" in transcript.lower()


def test_run_returns_claude_text_via_injected_client():
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

    out = diagnose.run("# === buggy.py ===\nprint(x)", "what's broken?", client=FakeClient())
    assert "buggy.py" in out
