from __future__ import annotations

import select
import sys

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

    print(f"🎙️  Recording (up to {seconds}s)... press Enter to stop early")
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=_callback):
        # Stop on Enter, but never record longer than `seconds`.
        ready, _, _ = select.select([sys.stdin], [], [], seconds)
        if ready:
            sys.stdin.readline()

    if not frames:
        sys.exit("🎙️  Didn't catch any audio — try again.")

    audio = np.concatenate(frames, axis=0)
    path = tempfile.mktemp(suffix=".wav")
    sf.write(path, audio, sample_rate)
    return path


def load(path: str) -> str:
    from pathlib import Path

    if not Path(path).is_file():
        raise FileNotFoundError(f"No audio file at {path!r} — check the --file path.")
    return path
