"""Scan code for 'vibe code' tells — signs it was AI-generated.

Pure and dependency-free, so it's unit-testable. Add a tell: write a small rule
function (return a finding dict or None) and drop it into RULES.
"""
from __future__ import annotations

import re

EM_DASH_THRESHOLD = 3
GENERIC_NAMES = {"data", "result", "temp", "foo", "thing", "stuff", "obj", "val"}
AI_PHRASES = ("note that", "it's worth noting", "here's the", "certainly,")


def em_dash_overuse(code: str):
    """Text peppered with em-dashes — the headline tell."""
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
    lines = [i for i, line in enumerate(code.splitlines(), 1)
             if "#" in line and any(p in line.split("#", 1)[1].lower() for p in AI_PHRASES)]
    if lines:
        return {"category": "ai_comment_phrases", "count": len(lines),
                "lines": lines, "detail": "comment phrasing that smells AI-written"}


RULES = (em_dash_overuse, generic_names, ai_comment_phrases)


def scan(code: str) -> list[dict]:
    """Return a list of findings — one dict per rule that fired (empty if clean)."""
    return [finding for rule in RULES if (finding := rule(code))]
