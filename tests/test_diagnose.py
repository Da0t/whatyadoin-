"""Diagnose tests — build_prompt is implemented; the API call test waits on you."""
import pytest

from whatyoudoin import diagnose


def test_build_prompt_includes_code_and_transcript():
    prompt = diagnose.build_prompt("print(x)", "x is not defined")
    assert "print(x)" in prompt
    assert "x is not defined" in prompt


def test_explain_and_fix_prompts_differ():
    explain = diagnose.build_prompt("code", "desc", "explain")
    fix = diagnose.build_prompt("code", "desc", "fix")
    assert explain != fix


@pytest.mark.skip(reason="implement diagnose.run() first")
def test_run_returns_claude_text_via_injected_client():
    """Once run() is wired up, build a fake client whose messages.create(...)
    returns an object with a text content block, pass it via client=, and assert
    run() returns that text — no real network call.
    """
    ...
