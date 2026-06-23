# whatyoudoin 🎙️

Say what's wrong with your code out loud; Claude comedically fixes it. One
command, voice-driven, command line only:

```
whatyoudoin fix buggy.py    # speak the problem → Claude shows the fix
```

You speak when prompted. Under the hood it: records your voice → transcribes it
with **Deepgram** → sends your words + your code to **Claude** → prints the fix.
Two authorized APIs, no GUI.

## The problem it solves

Beginner developers lose hours stuck on errors they can't yet put into words well
enough to even search. `whatyoudoin` lets you describe the problem the way you'd
say it to a friend, and turns that into a real fix.
_(Add a citable stat here for the slide — look up a developer-survey figure on
time lost to debugging.)_

## Setup

```bash
cd voicefix
python3 -m venv .venv && source .venv/bin/activate
pip install -e .          # installs the SDKs + the `whatyoudoin` command
cp .env.example .env      # paste in your two API keys (they auto-load from .env)
```

Keys come from [console.anthropic.com](https://console.anthropic.com) and
[console.deepgram.com](https://console.deepgram.com).

## Use it

```bash
whatyoudoin fix buggy.py                   # speak your bug (records ~6s)
whatyoudoin buggy.py                        # same — 'fix' is the only mode
whatyoudoin fix buggy.py --file clip.wav    # use a recording instead of the mic
```

Every run is saved to a local SQLite database (`~/.whatyoudoin/history.db`): the
fix session **and** any "vibe code" tells it spots in your file (overused
em-dashes, generic names, chatbot-y comments) — so the database does real work,
not just box-checking.

## Project layout

```
whatyoudoin/
  __main__.py   # the `fix` command + the shared flow
  audio.py      # record() / load()  — the voice capture
  stt.py        # Deepgram transcribe()
  diagnose.py   # build_prompt() + Claude run()
  mistakes.py   # vibe-code tell scanner
  db.py         # SQLite (sessions + mistakes)
tests/          # 11 unit tests
```

## Tests

```bash
pytest -q     # 11 passed
```
