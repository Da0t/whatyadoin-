"""Diagnose test — run() returns Claude's text via an injected fake client (no network)."""
from whatyoudoin import diagnose


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
