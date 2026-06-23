"""Send code + a spoken problem description to Claude.

Two modes:
  - "explain": describe what's wrong and why (no rewrite)
  - "fix":     return the corrected code

`build_prompt` is implemented and unit-tested. `run` is a stub for you to wire
up — its docstring has the exact recipe.
"""
from __future__ import annotations

# Anthropic's current flagship model. Do NOT add a date suffix.
MODEL = "claude-opus-4-8"

SYSTEM_PROMPTS = {
    "explain": (
        "You are a senior engineer helping a beginner understand a bug. Given "
        "their code and a spoken description of the problem, explain what is "
        "wrong and why — point to specific line(s). Keep it short and friendly. "
        "Do NOT rewrite the whole file; the goal is understanding, not a patch."
    ),
    "fix": (
        "You are a senior engineer fixing a beginner's bug. Given their code and "
        "a spoken description of the problem, return the corrected code in a code "
        "block, followed by one or two lines on exactly what you changed."
    ),
}


def build_prompt(code: str, transcript: str, mode: str = "explain") -> str:
    """Combine the spoken description and the code into one user prompt.

    Pure function — this is what the prompt-builder unit test checks.
    """
    ask = (
        "What's broken and why?"
        if mode == "explain"
        else "Fix it and show me the corrected code."
    )
    return (
        f"Here is what I said is going wrong:\n{transcript}\n\n"
        f"Here is my code:\n```\n{code}\n```\n\n{ask}"
    )


def run(code: str, transcript: str, mode: str = "explain", *, client=None) -> str:
    """Call Claude in 'explain' or 'fix' mode and return the response text.

    The optional ``client`` lets unit tests inject a fake (no network).

    TODO — implement:
        import anthropic
        client = client or anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from env
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=SYSTEM_PROMPTS[mode],
            thinking={"type": "adaptive"},   # optional: deeper reasoning for hard bugs
            messages=[
                {"role": "user", "content": build_prompt(code, transcript, mode)},
            ],
        )
        # response.content is a list of blocks; return the first text block.
        return next(b.text for b in response.content if b.type == "text")
    """
    raise NotImplementedError("Wire up the Anthropic call — see the docstring.")
