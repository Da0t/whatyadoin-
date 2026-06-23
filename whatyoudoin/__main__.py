"""whatyoudoin — say what's broken out loud; Claude comedically fixes it.

    whatyoudoin fix buggy.py                   # speak the problem -> Claude shows the fix
    whatyoudoin buggy.py                        # 'fix' is the only mode, so this works too
    whatyoudoin fix buggy.py --file clip.wav    # use a recording instead of the mic
"""
from __future__ import annotations

import argparse
import sys

from . import audio, db, diagnose as diagnose_mod, mistakes, stt


def _run(args) -> None:
    """record -> transcribe -> Claude fix -> save session + log vibe-code tells -> print."""
    code = open(args.path).read()

    wav = audio.load(args.file) if args.file else audio.record()
    transcript = stt.transcribe(wav)
    answer = diagnose_mod.run(code, transcript)

    conn = db.connect()
    sid = db.save_session(conn, args.path, transcript, answer)
    findings = mistakes.scan(code)
    db.save_mistakes(conn, sid, args.path, findings)

    print(answer)
    if findings:
        total = sum(f["count"] for f in findings)
        print(f"\n🚩 (Also logged {total} vibe-code tell(s) spotted in {args.path}.)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="whatyoudoin", description="Say what's broken; Claude fixes it.")
    sub = parser.add_subparsers(dest="command")
    fix = sub.add_parser("fix", help="Speak your bug; Claude shows the fix")
    fix.add_argument("path", help="The code file to fix")
    fix.add_argument("--file", help="Use this audio clip instead of the mic (demo fallback)")
    fix.set_defaults(func=_run)
    return parser


def main(argv=None) -> None:
    # Auto-load API keys from a local .env (python-dotenv is a declared dep).
    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ModuleNotFoundError:
        pass

    argv = list(sys.argv[1:] if argv is None else argv)
    # Bare `whatyoudoin <file>` means `fix <file>`.
    if argv and argv[0] not in ("fix", "-h", "--help"):
        argv.insert(0, "fix")
    args = build_parser().parse_args(argv)
    if not getattr(args, "func", None):
        build_parser().error("nothing to do — try: whatyoudoin fix buggy.py")
    args.func(args)


if __name__ == "__main__":
    main()
