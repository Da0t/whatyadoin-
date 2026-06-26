from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# How to run a script, by file extension. Python uses the current interpreter;
# the rest assume the usual toolchain is on PATH.
_RUNNERS = {
    ".py": [sys.executable],
    ".js": ["node"],
    ".mjs": ["node"],
    ".cjs": ["node"],
    ".ts": ["npx", "tsx"],
    ".rb": ["ruby"],
    ".go": ["go", "run"],
    ".php": ["php"],
    ".sh": ["bash"],
}


def _command_for(path):
    base = _RUNNERS.get(Path(path).suffix.lower())
    return base + [str(path)] if base else None


def run_script(path, timeout: int = 20):
    """Run ``<path>`` with the right interpreter for its language and return
    ``(returncode, stdout, stderr)``."""
    cmd = _command_for(path)
    if cmd is None:
        return 1, "", f"Don't know how to run {Path(path).suffix or path!r} files yet."
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return 1, "", f"Timed out after {timeout}s (possible infinite loop)."
    except FileNotFoundError:
        return 1, "", f"Couldn't find {cmd[0]!r} to run {Path(path).suffix} files. Is it installed and on PATH?"
    return proc.returncode, proc.stdout, proc.stderr
