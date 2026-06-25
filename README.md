# whatyoudoin 🎙️

Ask what's wrong with your code out loud; Claude searches your project, tells you
what's broken, and on your say-so fixes it. Voice-driven, command line only:

```
whatyoudoin ask         # 🎙️ "what's wrong?" → Claude finds it + suggests a fix
whatyoudoin fix         # applies that fix
whatyoudoin fix app.py  # ⚡ no voice: runs app.py, catches the crash, fixes it
```

Under the hood: records your question and transcribes it with **Deepgram** → sends
it plus all your project's `.py` files to **Claude** → Claude names the broken file
and suggests the fix → it's remembered in **SQLite** → `fix` reads that back and
writes the corrected file (saving the original as `.bak`). Two authorized APIs, no GUI.

## The problem it solves

Beginner developers lose hours stuck on errors they can't yet put into words well
enough to even search. `whatyoudoin` lets you just ask out loud and have Claude
find and fix it.
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

Run it from inside the project folder you want to debug:

```bash
whatyoudoin ask                  # 🎙️ ask "what's wrong?" → diagnosis + suggested fix
whatyoudoin fix                  # apply the suggested fix
whatyoudoin fix buggy.py         # ⚡ run buggy.py, capture the crash, fix it automatically
whatyoudoin ask --file clip.wav  # use a recording instead of the mic
```

`ask` records until you **press Enter** — talk as long as you need, no fixed timer.
`fix <file>` skips the voice step entirely: it runs the script, feeds the actual
traceback to Claude, applies the fix (original saved as `.bak`), then re-runs the
file to confirm the crash is gone.

The `ask` step saves the diagnosis to a local SQLite database
(`~/.whatyoudoin/history.db`) — that's the "memory" the `fix` step reads back.

## Project layout

```
whatyoudoin/
  __main__.py   # the ask + fix commands
  audio.py      # record() / load()  — the voice capture
  stt.py        # Deepgram transcribe()
  diagnose.py   # build_prompt() + extract_filename/code() + Claude run()
  db.py         # SQLite (memory between ask and fix)
tests/          # 5 unit tests
```

## Tests

```bash
pip install pytest
pytest -q     # 5 passed
```
