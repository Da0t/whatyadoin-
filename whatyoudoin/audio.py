"""Record your voice from the mic, or load an existing clip (--file fallback).

Both are stubs. `record` is the live-mic path; `load` is the foolproof fallback
so a mic hiccup can't kill the live demo.
"""
from __future__ import annotations

DEFAULT_SECONDS = 6
SAMPLE_RATE = 16_000


def record(seconds: int = DEFAULT_SECONDS, sample_rate: int = SAMPLE_RATE) -> str:
    """Record from the default microphone and return the path to a temp .wav.

    TODO — implement with sounddevice + soundfile:
        import sounddevice as sd
        import soundfile as sf
        import tempfile
        print(f"Recording for {seconds}s... speak now")
        frames = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1)
        sd.wait()
        path = tempfile.mktemp(suffix=".wav")
        sf.write(path, frames, sample_rate)
        return path
    (macOS will ask for microphone permission the first time you run this.)
    """
    raise NotImplementedError("Wire up mic recording — see the docstring.")


def load(path: str) -> str:
    """Return the path to an existing audio file, for the --file fallback.

    TODO — check the file exists; raise FileNotFoundError with a friendly
    message otherwise, then return the path unchanged.
    """
    raise NotImplementedError
