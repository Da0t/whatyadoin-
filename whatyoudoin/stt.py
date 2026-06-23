"""Speech-to-text via Deepgram.

`parse_transcript` is the pure, unit-testable piece; `transcribe` wraps it with
the network call (Deepgram imported lazily so the package loads without the SDK).
"""
from __future__ import annotations


def transcribe(audio_path, *, client=None) -> str:
    """Transcribe a .wav/.mp3 to text with Deepgram (surface matches deepgram-sdk v3)."""
    from deepgram import DeepgramClient, PrerecordedOptions

    dg = client or DeepgramClient()          # reads DEEPGRAM_API_KEY from env
    with open(audio_path, "rb") as f:
        source = {"buffer": f.read()}
    options = PrerecordedOptions(model="nova-3", smart_format=True)
    response = dg.listen.rest.v("1").transcribe_file(source, options)
    return parse_transcript(response.to_dict())


def parse_transcript(response: dict) -> str:
    """Pull the transcript out: results -> channels[0] -> alternatives[0] -> transcript."""
    return response["results"]["channels"][0]["alternatives"][0]["transcript"]
