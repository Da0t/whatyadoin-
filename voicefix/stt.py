"""Speech-to-text via the Deepgram API.

Both functions are stubs. `parse_transcript` is the pure, unit-testable piece;
`transcribe` is the network call that wraps it.
"""
from __future__ import annotations


def transcribe(audio_path, *, client=None) -> str:
    """Transcribe a .wav/.mp3 file to text with Deepgram. Returns the transcript.

    The optional ``client`` lets tests inject a fake Deepgram client.

    TODO — implement (verify the exact call against your installed deepgram-sdk
    version; the surface below matches deepgram-sdk v3):
        from deepgram import DeepgramClient, PrerecordedOptions
        dg = client or DeepgramClient()          # reads DEEPGRAM_API_KEY from env
        with open(audio_path, "rb") as f:
            source = {"buffer": f.read()}
        options = PrerecordedOptions(model="nova-3", smart_format=True)
        response = dg.listen.rest.v("1").transcribe_file(source, options)
        return parse_transcript(response.to_dict())
    """
    raise NotImplementedError("Wire up Deepgram — see the docstring.")


def parse_transcript(response: dict) -> str:
    """Pull the transcript string out of a Deepgram response dict.

    Deepgram nests it at: results -> channels[0] -> alternatives[0] -> transcript
    Keeping this separate from the network call makes it easy to unit-test with
    a fake payload (see tests/test_stt.py).

    TODO — implement and return that nested string.
    """
    raise NotImplementedError
