from __future__ import annotations

DEFAULT_SECONDS = 2
SAMPLE_RATE = 16_000


def record(seconds: int = DEFAULT_SECONDS, sample_rate: int = SAMPLE_RATE) -> str:
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
    from pathlib import Path

    if not Path(path).is_file():
        raise FileNotFoundError(f"No audio file at {path!r} — check the --file path.")
    return path
