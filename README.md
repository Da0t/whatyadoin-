# voicefix 🎙️

A tiny command-line tool that lets you **talk** about your broken code and get a
fix back. You point it at a file, say what's going wrong, and it:

1. records your voice (or takes a `--text` description),
2. transcribes it with **Deepgram** (speech-to-text API),
3. sends your words **+ your code** to **Claude** (Anthropic API),
4. prints a diagnosis and a fix, and
5. saves the session to a small **SQLite** database so you can look it up later.

Two authorized APIs (Deepgram + Anthropic), command line only, no GUI.

## The problem it solves

Beginner developers lose a large chunk of their time stuck on errors they can't
yet put into words well enough to search. `voicefix` lets you describe the
problem out loud — the way you'd explain it to a friend — and turns that into a
concrete fix. *(Drop a real citation here for the slide deck, e.g. a developer
survey stat on time spent debugging.)*

## How it works

```
$ voicefix diagnose buggy.py
🎙  Recording... speak now
   [you say: "it throws an index error but only sometimes"]
   → Deepgram transcribes your audio        (API call #1)
   → Claude reads your code + your words     (API call #2)

💡 Diagnosis: line 12 reads nums[i+1] but the loop runs to len(nums)...
✅ Fix: change range(len(nums)) to range(len(nums) - 1)
```

### Commands

| Command | What it does |
|---|---|
| `voicefix diagnose <file>` | Record, transcribe, diagnose, save, print |
| `voicefix diagnose <file> --file clip.wav` | Use an existing audio clip instead of the mic (demo-safe fallback) |
| `voicefix diagnose <file> --text "..."` | Skip voice entirely; type the problem |
| `voicefix history` | List past sessions |
| `voicefix show <id>` | Reprint one past session |

## Setup

```bash
cd voicefix
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env       # then add your two API keys
```

Get keys from [console.anthropic.com](https://console.anthropic.com) and
[console.deepgram.com](https://console.deepgram.com). Load them into your shell
(e.g. `export $(cat .env | xargs)` or use `python-dotenv`).

Run it as a module from the project root:

```bash
python -m voicefix history
```

## Project layout

```
voicefix/
  voicefix/
    __init__.py
    __main__.py     # CLI (argparse) — parser wired up, command handlers are stubs
    audio.py        # record() / load()        — STUB
    stt.py          # Deepgram transcribe()     — STUB
    diagnose.py     # build_prompt() done; diagnose() (Claude call) — STUB
    db.py           # SQLite — IMPLEMENTED
  tests/
    test_db.py        # 3 passing tests
    test_diagnose.py  # build_prompt test passes; diagnose test skipped until wired
    test_stt.py       # parse_transcript test skipped until wired
  requirements.txt
  .env.example
```

## What's a stub vs. done (skeleton status)

**Done:** project structure, the SQLite layer (`db.py`), the prompt builder
(`diagnose.build_prompt`), the CLI argument parser, and the test scaffolding
(3 tests pass today).

**To implement** (each function has a step-by-step TODO in its docstring):
- `audio.record` / `audio.load` — mic capture + file fallback
- `stt.transcribe` / `stt.parse_transcript` — the Deepgram call + response parsing
- `diagnose.diagnose` — the Claude `messages.create` call
- the three CLI handlers in `__main__.py` (`cmd_diagnose`, `cmd_history`, `cmd_show`)
- the two skipped tests (remove the `@pytest.mark.skip` once the code exists)

## Running the tests

```bash
pip install pytest
pytest -q
```

## Ideas for v2 (scaling / expansion)

- Auto-detect the file's language and tailor the prompt.
- `voicefix history --search "<term>"` over saved diagnoses.
- Apply the fix to the file automatically with a confirm step.
- Stream Claude's answer token-by-token for a snappier demo.
