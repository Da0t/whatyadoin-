"""whatyoudoin — ask what's wrong out loud; Claude finds it; say 'fix' and it fixes.

    whatyoudoin ask   # 🎙️ speak your question -> Claude searches your project, says what's wrong + suggests a fix
    whatyoudoin fix   # applies the fix Claude just suggested (remembered in SQLite)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import audio, db, diagnose as diagnose_mod, stt


def _gather() -> str:
    """Read every .py file in the current folder into one labeled blob (small projects)."""
    files = sorted(Path.cwd().glob("*.py"))
    return "\n\n".join(f"# === {p.name} ===\n{p.read_text()}" for p in files)


def _ask(args) -> None:
    """🎙️ speak -> transcribe -> Claude diagnoses the project -> print + remember in SQLite."""
    wav = audio.load(args.file) if args.file else audio.record()
    transcript = stt.transcribe(wav)
    answer = diagnose_mod.run(_gather(), transcript)
    db.save_session(db.connect(), "(project)", transcript, answer)
    print(answer)
    print("\nSay it's good? Run `whatyoudoin fix` to apply this.")


def _fix(args) -> None:
    """Apply the fix Claude suggested last (read back from SQLite)."""
    last = db.latest_session(db.connect())
    if not last:
        sys.exit("Nothing to fix yet — run `whatyoudoin ask` first.")
    target = diagnose_mod.extract_filename(last["response"])
    fixed = diagnose_mod.extract_code(last["response"])
    if not (target and fixed):
        sys.exit("Couldn't find a suggested fix to apply — try `whatyoudoin ask` again.")
    if Path(target).exists():
        Path(target + ".bak").write_text(Path(target).read_text())
    Path(target).write_text(fixed)
    print(f"✏️  Applied the fix to {target} (original saved as {target}.bak).")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="whatyoudoin",
        description="Ask what's wrong; Claude finds it; say fix and it fixes.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    ask = sub.add_parser("ask", help="Speak your question; Claude diagnoses your project")
    ask.add_argument("--file", help="Use this audio clip instead of the mic (demo fallback)")
    ask.set_defaults(func=_ask)
    fix = sub.add_parser("fix", help="Apply the fix Claude just suggested")
    fix.set_defaults(func=_fix)
    return parser


def main(argv=None) -> None:
    # Auto-load API keys from a local .env in the current dir (or a parent).
    try:
        from dotenv import find_dotenv, load_dotenv

        load_dotenv(find_dotenv(usecwd=True))
    except ModuleNotFoundError:
        pass

    args = build_parser().parse_args(sys.argv[1:] if argv is None else argv)
    args.func(args)


if __name__ == "__main__":
    main()
