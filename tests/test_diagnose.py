"""Diagnose tests — build_prompt and run() (via an injected fake client)."""
from whatyoudoin import diagnose


def test_build_prompt_includes_code_and_transcript():
    prompt = diagnose.build_prompt("print(x)", "x is not defined")
    assert "print(x)" in prompt
    assert "x is not defined" in prompt


def test_run_returns_claude_text_via_injected_client():
    """A fake client returns one text block; run() hands back its text — no network."""

    class Block:
        type = "text"
        text = "your loop never updates i — line 3"

    class Response:
        content = [Block()]

    class FakeClient:
        class messages:
            @staticmethod
            def create(**kwargs):
                return Response()

    out = diagnose.run("while True: pass", "it never stops", client=FakeClient())
    assert out == "your loop never updates i — line 3"
