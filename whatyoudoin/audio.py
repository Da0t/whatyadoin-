"""Capture the user's voice: record from the mic, or load a clip (--file fallback).

This is the voice half of the tool — `record` grabs mic audio, `load` reuses a
saved clip so a mic hiccup can't kill a live demo.
"""
from __future__ import annotations

DEFAULT_SECONDS = 6
SAMPLE_RATE = 16_000


def record(seconds: int = DEFAULT_SECONDS, sample_rate: int = SAMPLE_RATE) -> str:
    """Record from the default mic and return a temp .wav path (macOS asks permission)."""
    import tempfile

    import sounddevice as sd
    import soundfile as sf

    print(f"🎙️  Recording for {seconds}s... speak now")
    frames = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    path = tempfile.mktemp(suffix=".wav")
    sf.write(path, frames, sample_rate)
    return path


def load(path: str) -> str:
    """Return the path to an existing audio file, for the --file fallback."""
    from pathlib import Path

    if not Path(path).is_file():
        raise FileNotFoundError(f"No audio file at {path!r} — check the --file path.")
    return path
