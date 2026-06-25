from __future__ import annotations

import subprocess
import sys


def run_script(path, timeout: int = 20):
    """Run ``python <path>`` and return ``(returncode, stdout, stderr)``."""
    try:
        proc = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return 1, "", f"Timed out after {timeout}s (possible infinite loop)."
    return proc.returncode, proc.stdout, proc.stderr
