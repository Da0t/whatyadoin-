# whatyoudoin 🎙️

Say what's wrong with your code out loud; Claude tells you. A tiny terminal
tool with **two commands**:

```
whatyoudoin buggy.py        # speak the problem → Claude explains what's broken
whatyoudoin fix buggy.py    # speak the problem → Claude shows the fix
```

You speak when prompted. Under the hood it: records your voice → transcribes it
with **Deepgram** → sends your words + your code to **Claude** → prints the
answer. Two authorized APIs, command line only, no GUI.

## The problem it solves

Beginner developers lose a big chunk of their time stuck on errors they can't
yet put into words well enough to even search. `whatyoudoin` lets you describe
the problem the way you'd say it to a friend, and turns that into a real answer.
*(Add a citable stat here for the slide deck — e.g. a developer survey on time
lost to debugging.)*

## Setup

```bash
cd voicefix              # the project folder
python3 -m venv .venv && source .venv/bin/activate
pip install -e .         # installs deps + the `whatyoudoin` command
cp .env.example .env     # then paste in your two API keys
```

Keys come from [console.anthropic.com](https://console.anthropic.com) and
[console.deepgram.com](https://console.deepgram.com). Load them into your shell
(e.g. `export $(cat .env | xargs)`).

Then just:

```bash
whatyoudoin buggy.py
whatyoudoin fix buggy.py
# (or, without installing: python -m whatyoudoin buggy.py)
```

## Project layout

```
whatyoudoin/
  __init__.py
  __main__.py     # the two commands (explain default + fix) — handlers are stubs
  audio.py        # record() / load()     — STUB
  stt.py          # Deepgram transcribe()  — STUB
  diagnose.py     # build_prompt() done; run() (Claude call) — STUB
  db.py           # SQLite (silent session log) — IMPLEMENTED
tests/            # test_db (3 pass), test_diagnose (2 pass), test_stt (skipped)
pyproject.toml    # makes `whatyoudoin` a real command
requirements.txt
.env.example
```

Every run is quietly saved to a small SQLite database (`~/.whatyoudoin/history.db`)
— no extra command, it just satisfies the "useful database" rubric box.

## What's done vs. stub

**Done:** structure, the SQLite layer, the prompt builder, the CLI, and the
tests (5 pass today). **To implement** — each has a step-by-step TODO in its
docstring:
- `audio.record` / `audio.load` — mic capture + file fallback
- `stt.transcribe` / `stt.parse_transcript` — the Deepgram call + parsing
- `diagnose.run` — the Claude `messages.create` call
- `_run` in `__main__.py` — the glue both commands share
- the two skipped tests (drop the `@pytest.mark.skip` once the code exists)

## Tests

```bash
pip install pytest
pytest -q
```

## Ideas for v2

- Detect the file's language and tailor the prompt.
- Apply the fix to the file with a confirm step.
- Stream Claude's answer token-by-token for a snappier demo.
