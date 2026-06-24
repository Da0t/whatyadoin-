from __future__ import annotations

import os

import httpx

DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"


def transcribe(audio_path) -> str:
    with open(audio_path, "rb") as f:
        audio = f.read()
    resp = httpx.post(
        DEEPGRAM_URL,
        params={"model": "nova-3", "smart_format": "true"},
        headers={
            "Authorization": f"Token {os.environ['DEEPGRAM_API_KEY']}",
            "Content-Type": "audio/wav",
        },
        content=audio,
        timeout=60,
    )
    resp.raise_for_status()
    return parse_transcript(resp.json())


def parse_transcript(response: dict) -> str:
    return response["results"]["channels"][0]["alternatives"][0]["transcript"]
