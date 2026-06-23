"""Send code + a spoken problem description to Claude and get a diagnosis.

`build_prompt` is implemented (it's pure and unit-tested). `diagnose` is a
stub for you to wire up — the docstring has the exact recipe.
"""
from __future__ import annotations

# Anthropic's current flagship model. Do NOT add a date suffix.
MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You are a senior engineer helping a beginner debug their code. "
    "Given the code and the developer's spoken description of the problem, "
    "explain what is broken and how to fix it. Be concise and concrete: "
    "point to specific lines, show the corrected code, and keep a friendly tone."
)


def build_prompt(code: str, transcript: str) -> str:
    """Combine the spoken problem description and the code into one user prompt.

    Pure function — this is what the prompt-builder unit test checks.
    """
    return (
        f"Here is what I said is going wrong:\n{transcript}\n\n"
        f"Here is my code:\n```\n{code}\n```\n\n"
        "What's broken and how do I fix it?"
    )


def diagnose(code: str, transcript: str, *, client=None) -> str:
    """Call Claude with the code + transcript and return the diagnosis text.

    The optional ``client`` lets unit tests inject a fake (no network).

    TODO — implement:
        import anthropic
        client = client or anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from env
        response = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            thinking={"type": "adaptive"},   # optional: deeper reasoning for hard bugs
            messages=[
                {"role": "user", "content": build_prompt(code, transcript)},
            ],
        )
        # response.content is a list of blocks; return the first text block.
        return next(b.text for b in response.content if b.type == "text")
    """
    raise NotImplementedError("Wire up the Anthropic call — see the docstring.")
