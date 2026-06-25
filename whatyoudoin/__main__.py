from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import audio, db, diagnose as diagnose_mod, stt


_SKIP = {".venv", "venv", "__pycache__", ".git", "node_modules", "site-packages", ".pytest_cache", "build", "dist"}


def _gather() -> str:
    root = Path.cwd()
    files = [
        p for p in sorted(root.rglob("*.py"))
        if not any(part in _SKIP or part.startswith(".") for part in p.relative_to(root).parts)
    ]
    return "\n\n".join(f"# === {p.relative_to(root)} ===\n{p.read_text()}" for p in files)


def _ask(args) -> None:
    wav = audio.load(args.file) if args.file else audio.record()
    print("Transcribing...", flush=True)
    transcript = stt.transcribe(wav)
    print("Asking Claude...", flush=True)
    answer = diagnose_mod.run(_gather(), transcript)
    db.save_session(db.connect(), "(project)", transcript, answer)
    print(answer)
    print("\nSay it's good? Run `whatyoudoin fix` to apply this.")


def _apply_fix(target: str, fixed: str) -> None:
    bak = Path(target + ".bak")
    # Keep the first/pristine original — never let a re-run clobber it with an
    # already-modified version.
    if Path(target).exists() and not bak.exists():
        bak.write_text(Path(target).read_text())
    Path(target).write_text(fixed)
    print(f"✏️  Applied the fix to {target} (original saved as {target}.bak).")


def _fix(args) -> None:
    if args.file:
        _autofix_from_crash(args.file)
        return
    last = db.latest_session(db.connect())
    if not last:
        sys.exit("Nothing to fix yet — run `whatyoudoin ask` first, or `whatyoudoin fix <file>`.")
    target = diagnose_mod.extract_filename(last["response"])
    fixed = diagnose_mod.extract_code(last["response"])
    if not (target and fixed):
        sys.exit("Couldn't find a suggested fix to apply — try `whatyoudoin ask` again.")
    _apply_fix(target, fixed)


def _autofix_from_crash(file, *, run_script=None, client=None, conn=None) -> None:
    from . import runner

    run_script = run_script or runner.run_script
    conn = conn or db.connect()

    print(f"▶️  Running {file} ...")
    code, _out, err = run_script(file)
    if code == 0:
        print(f"✅ {file} ran fine — nothing to fix.")
        return

    print("💥 It crashed. Asking Claude for the fix...")
    transcript = f"I ran `{file}` and it crashed:\n{err.strip()}\n\nFind the bug and fix it."
    answer = diagnose_mod.run(_gather(), transcript, client=client)
    db.save_session(conn, "(crash)", transcript, answer)

    target = diagnose_mod.extract_filename(answer)
    fixed = diagnose_mod.extract_code(answer)
    if not (target and fixed):
        print(answer)
        sys.exit("Couldn't parse a fix from Claude's reply.")
    _apply_fix(target, fixed)


def _mistakes(args) -> None:
    from collections import Counter

    sessions = db.all_sessions(db.connect())
    if not sessions:
        print("No mistakes recorded yet — run `whatyoudoin ask` first.")
        return

    counts: Counter = Counter()
    latest_summary: dict[str, str] = {}
    for s in sessions:  # newest first, so setdefault keeps the most recent summary
        culprit = diagnose_mod.extract_filename(s["response"]) or "(no file identified)"
        counts[culprit] += 1
        latest_summary.setdefault(culprit, diagnose_mod.extract_summary(s["response"]))

    print(f"🐛 Your mistakes so far ({len(sessions)} sessions):\n")
    for culprit, n in counts.most_common():
        print(f"  {n}×  {culprit}  — {latest_summary[culprit]}")
    print("\n(grouped by the file Claude flagged)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="whatyoudoin",
        description="Ask what's wrong; Claude finds it; say fix and it fixes.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    ask = sub.add_parser("ask", help="Speak your question; Claude diagnoses your project")
    ask.add_argument("--file", help="Use this audio clip instead of the mic (demo fallback)")
    ask.set_defaults(func=_ask)
    fix = sub.add_parser("fix", help="Apply the last suggested fix, or pass a file to run-and-fix it")
    fix.add_argument("file", nargs="?", help="Run this script, capture the crash, and fix it automatically")
    fix.set_defaults(func=_fix)
    mistakes = sub.add_parser("mistakes", help="Tally past bugs from your history database")
    mistakes.set_defaults(func=_mistakes)
    return parser


def main(argv=None) -> None:
    try:
        from dotenv import load_dotenv

        load_dotenv(Path(__file__).resolve().parent.parent / ".env")  # project .env, from any folder
    except ModuleNotFoundError:
        pass

    args = build_parser().parse_args(sys.argv[1:] if argv is None else argv)
    args.func(args)


if __name__ == "__main__":
    main()
