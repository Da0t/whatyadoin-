"""whatyoudoin — say what's wrong with your code; Claude tells you.

Two commands, voice-driven:

    whatyoudoin <file>        # speak the problem -> Claude explains what's broken
    whatyoudoin fix <file>    # speak the problem -> Claude shows the fix

You speak when prompted. (--file clip.wav plays a recording instead of using the
mic — a safety net so a mic hiccup can't break a live demo.)

The two command handlers share one flow (`_run`) and are stubs for you to wire
up; the docstring has the recipe.
"""
from __future__ import annotations

import argparse
import sys

from . import audio, db, diagnose as diagnose_mod, stt


def _run(mode: str, args) -> None:
    """explain/fix share this: record -> transcribe -> Claude -> save -> print.

    TODO — implement:
        wav = audio.load(args.file) if args.file else audio.record()
        transcript = stt.transcribe(wav)
        code = open(args.path).read()
        answer = diagnose_mod.run(code, transcript, mode)
        db.save_session(db.connect(), mode, args.path, transcript, answer)
        print(answer)
    """
    raise NotImplementedError


def cmd_explain(args):
    _run("explain", args)


def cmd_fix(args):
    _run("fix", args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="whatyoudoin",
        description="Say what's wrong with your code; Claude tells you.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_target(p):
        p.add_argument("path", help="The code file to look at")
        p.add_argument("--file", help="Use this audio clip instead of the mic (demo fallback)")

    explain = sub.add_parser("explain", help="Explain what's broken (this is the default)")
    add_target(explain)
    explain.set_defaults(func=cmd_explain)

    fix = sub.add_parser("fix", help="Show the fix")
    add_target(fix)
    fix.set_defaults(func=cmd_fix)

    return parser


def main(argv=None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    # Bare `whatyoudoin <file>` (no subcommand) means: explain.
    if argv and argv[0] not in ("explain", "fix", "-h", "--help"):
        argv.insert(0, "explain")
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
