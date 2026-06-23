"""STT tests — parse_transcript is a stub, so this is skipped until you fill it in."""
import pytest

from voicefix import stt

FAKE_DEEPGRAM_RESPONSE = {
    "results": {
        "channels": [
            {"alternatives": [{"transcript": "why does my loop never stop"}]}
        ]
    }
}


@pytest.mark.skip(reason="implement stt.parse_transcript() first")
def test_parse_transcript_pulls_text():
    assert (
        stt.parse_transcript(FAKE_DEEPGRAM_RESPONSE)
        == "why does my loop never stop"
    )
