"""Send code + a spoken problem to Claude and get the fix back — comedically.

`build_prompt` is the pure, unit-tested piece; `run` makes the API call.
"""
from __future__ import annotations

# Anthropic's current flagship model. Do NOT add a date suffix.
MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = (
    "You are a sharp, witty senior engineer fixing a beginner's bug — funny and "
    "a little cheeky, but always on their side (roast the bug, never the person). "
    "Given their code and a spoken description of the problem, return the "
    "corrected code in a code block, followed by one or two lines — with "
    "personality — on exactly what you changed and why."
)


def build_prompt(code: str, transcript: str) -> str:
    """Combine the spoken description and the code into one user prompt (pure)."""
    return (
        f"Here is what I said is going wrong:\n{transcript}\n\n"
        f"Here is my code:\n```\n{code}\n```\n\nFix it and show me the corrected code."
    )


def run(code: str, transcript: str, *, client=None) -> str:
    """Call Claude and return its reply text. Inject ``client`` in tests (no network)."""
    if client is None:
        import anthropic

        client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from env
    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_prompt(code, transcript)}],
    )
    return next(b.text for b in response.content if b.type == "text")
