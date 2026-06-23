"""Scan code for 'vibe code' tells — the little signs it was AI-generated.

Pure and dependency-free, so it's unit-testable without any API keys (unlike the
Deepgram/Claude paths). `scan` runs every rule in RULES over the source text and
returns one finding dict per rule that fired. Add a tell by writing a small
function and dropping it into RULES.
"""
from __future__ import annotations

import re

EM_DASH_THRESHOLD = 3
GENERIC_NAMES = {"data", "result", "temp", "foo", "thing", "stuff", "obj", "val"}
AI_PHRASES = ("note that", "it's worth noting", "here's the", "certainly,")


def em_dash_overuse(code: str):
    """The headline tell: text peppered with em-dashes."""
    count = code.count("—")
    if count > EM_DASH_THRESHOLD:
        lines = [i for i, l in enumerate(code.splitlines(), 1) if "—" in l]
        return {"category": "em_dash_overuse", "count": count, "lines": lines,
                "detail": f"{count} em-dashes — a classic AI tell"}


def generic_names(code: str):
    """Variables named `data`, `result`, `temp`... — nobody read this."""
    hits = []
    for i, line in enumerate(code.splitlines(), 1):
        m = re.match(r"\s*([A-Za-z_]\w*)\s*=", line)
        if m and m.group(1) in GENERIC_NAMES:
            hits.append((i, m.group(1)))
    if hits:
        names = ", ".join(sorted({n for _, n in hits}))
        return {"category": "generic_names", "count": len(hits),
                "lines": [i for i, _ in hits], "detail": f"vague names: {names}"}


def ai_comment_phrases(code: str):
    """Comments that talk like a chatbot ('Note that...', 'Certainly,...')."""
    lines = []
    for i, line in enumerate(code.splitlines(), 1):
        if "#" in line:
            comment = line.split("#", 1)[1].lower()
            if any(p in comment for p in AI_PHRASES):
                lines.append(i)
    if lines:
        return {"category": "ai_comment_phrases", "count": len(lines),
                "lines": lines, "detail": "comment phrasing that smells AI-written"}


RULES = (em_dash_overuse, generic_names, ai_comment_phrases)


def scan(code: str) -> list[dict]:
    """Return a list of findings — one dict per rule that fired (empty if clean)."""
    return [finding for rule in RULES if (finding := rule(code))]
