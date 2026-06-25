from __future__ import annotations

import re

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = (
    "You are a sharp, witty senior engineer helping a beginner — funny and a little "
    "cheeky, but always on their side (roast the bug, never the person). You're given "
    "all the .py files in their small project and a spoken question. Find the bug, then "
    "reply in EXACTLY this shape:\n"
    "FILE: <the filename to fix>\n"
    "```\n<the complete corrected file>\n```\n"
    "then 2-3 punchy lines on what was wrong and what you changed."
)


def build_prompt(code: str, transcript: str) -> str:
    return (
        f"Here's what I said:\n{transcript}\n\n"
        f"Here are my project files:\n{code}\n\n"
        "What's wrong, and what's the fix?"
    )


def build_error_transcript(filename: str, stderr: str) -> str:
    # Stand in for the spoken question when a script crashes: feed Claude the
    # real traceback so the `fix <file>` flow needs no voice input.
    return (
        f"I ran `{filename}` and it crashed with this error:\n"
        f"{stderr.strip()}\n\n"
        "Find the bug and fix it."
    )


def extract_filename(reply: str) -> str | None:
    m = re.search(r"^FILE:\s*(\S+)", reply, re.MULTILINE)
    return m.group(1) if m else None


def extract_code(reply: str) -> str | None:
    m = re.search(r"```(?:\w+)?\n(.*?)```", reply, re.DOTALL)
    return m.group(1).rstrip() + "\n" if m else None


def extract_summary(reply: str) -> str:
    # The explanation lines come after the fenced code block.
    segments = reply.split("```")
    tail = segments[-1] if len(segments) >= 3 else reply
    for line in tail.strip().splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped
    return "(no summary)"


def run(code: str, transcript: str, *, client=None) -> str:
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
