from __future__ import annotations

import os
import select
import sys
import termios
import tty

DEFAULT_SECONDS = 4
SAMPLE_RATE = 16_000


def record(seconds: int = DEFAULT_SECONDS, sample_rate: int = SAMPLE_RATE) -> str:
    import tempfile

    import numpy as np
    import sounddevice as sd
    import soundfile as sf

    frames: list = []

    def _callback(indata, frame_count, time_info, status):
        frames.append(indata.copy())

    print(f"🎙️  Recording (up to {seconds}s)... tap 's' to stop")
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=_callback):
        _wait_for_stop(seconds)

    if not frames:
        sys.exit("🎙️  Didn't catch any audio — try again.")

    audio = np.concatenate(frames, axis=0)
    path = tempfile.mktemp(suffix=".wav")
    sf.write(path, audio, sample_rate)
    return path


def _wait_for_stop(seconds: int) -> None:
    """Return when 's' is pressed or `seconds` elapse — whichever comes first."""
    import time

    if not sys.stdin.isatty():
        time.sleep(seconds)  # no keyboard to read (piped/non-interactive)
        return

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)  # deliver keystrokes immediately — no Enter needed
        deadline = time.monotonic() + seconds
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return
            ready, _, _ = select.select([fd], [], [], remaining)
            if ready and os.read(fd, 1) in (b"s", b"S"):
                return
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def load(path: str) -> str:
    from pathlib import Path

    if not Path(path).is_file():
        raise FileNotFoundError(f"No audio file at {path!r} — check the --file path.")
    return path
