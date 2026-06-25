from __future__ import annotations

import subprocess
import sys


def run_script(path, timeout: int = 20):
    """Run ``python <path>`` in a subprocess and report how it went.

    Returns ``(returncode, stdout, stderr)``. A crash leaves its traceback in
    ``stderr`` with a non-zero ``returncode``. A timeout (e.g. an infinite loop)
    is reported the same way so callers can treat it like any other failure.
    """
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
