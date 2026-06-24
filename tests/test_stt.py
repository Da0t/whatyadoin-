from whatyoudoin import stt

FAKE_DEEPGRAM_RESPONSE = {
    "results": {
        "channels": [
            {"alternatives": [{"transcript": "why does my loop never stop"}]}
        ]
    }
}


def test_parse_transcript_pulls_text():
    assert (
        stt.parse_transcript(FAKE_DEEPGRAM_RESPONSE)
        == "why does my loop never stop"
    )
