from __future__ import annotations

import sys

SAMPLE_RATE = 16_000


def record(sample_rate: int = SAMPLE_RATE) -> str:
    import tempfile

    import numpy as np
    import sounddevice as sd
    import soundfile as sf

    frames: list = []

    def _callback(indata, frame_count, time_info, status):
        frames.append(indata.copy())

    print("🎙️  Recording... press Enter to stop")
    with sd.InputStream(samplerate=sample_rate, channels=1, callback=_callback):
        input()  # block here until the user hits Enter, then close the stream

    if not frames:
        sys.exit("🎙️  Didn't catch any audio — try again and speak before pressing Enter.")

    audio = np.concatenate(frames, axis=0)
    path = tempfile.mktemp(suffix=".wav")
    sf.write(path, audio, sample_rate)
    return path


def load(path: str) -> str:
    from pathlib import Path

    if not Path(path).is_file():
        raise FileNotFoundError(f"No audio file at {path!r} — check the --file path.")
    return path
