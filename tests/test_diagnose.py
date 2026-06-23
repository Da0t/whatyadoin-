"""Diagnose tests — build_prompt is implemented; the API test waits on you."""
import pytest

from voicefix import diagnose


def test_build_prompt_includes_code_and_transcript():
    prompt = diagnose.build_prompt("print(x)", "x is not defined")
    assert "print(x)" in prompt
    assert "x is not defined" in prompt


@pytest.mark.skip(reason="implement diagnose.diagnose() first")
def test_diagnose_returns_claude_text_via_injected_client():
    """Once diagnose() is wired up, build a fake client whose
    messages.create(...) returns an object with a text content block, pass it
    via client=, and assert diagnose() returns that text — no real network call.
    """
    ...
