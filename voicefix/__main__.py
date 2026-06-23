"""voicefix CLI entry point.

    python -m voicefix diagnose path/to/file.py
    python -m voicefix diagnose path/to/file.py --file clip.wav
    python -m voicefix diagnose path/to/file.py --text "why does this crash"
    python -m voicefix history
    python -m voicefix show <id>

The argument parser is wired up. The three command handlers are stubs for you
to fill — each docstring lists the steps and the helpers to call.
"""
from __future__ import annotations

import argparse

from . import audio, db, diagnose as diagnose_mod, stt


def cmd_diagnose(args) -> None:
    """Get the problem description, read the code, ask Claude, save + print.

    TODO — implement:
        if args.text:
            transcript = args.text
        else:
            wav = audio.load(args.file) if args.file else audio.record()
            transcript = stt.transcribe(wav)
        code = open(args.path).read()
        answer = diagnose_mod.diagnose(code, transcript)
        conn = db.connect()
        db.save_session(conn, args.path, transcript, answer)
        print(answer)
    """
    raise NotImplementedError


def cmd_history(args) -> None:
    """List past sessions.

    TODO — conn = db.connect(); rows = db.list_sessions(conn); print id,
    created_at, file_path (and a snippet of the transcript) per row.
    """
    raise NotImplementedError


def cmd_show(args) -> None:
    """Show one past session by id.

    TODO — conn = db.connect(); row = db.get_session(conn, args.id);
    print the transcript and the full response, or a not-found message.
    """
    raise NotImplementedError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voicefix",
        description="Talk to Claude about your broken code.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    d = sub.add_parser("diagnose", help="Diagnose a code file from a spoken (or typed) description")
    d.add_argument("path", help="Path to the code file to diagnose")
    d.add_argument("--file", help="Transcribe this audio file instead of recording from the mic")
    d.add_argument("--text", help="Skip voice entirely; use this text as the problem description")
    d.set_defaults(func=cmd_diagnose)

    h = sub.add_parser("history", help="List past diagnosis sessions")
    h.set_defaults(func=cmd_history)

    s = sub.add_parser("show", help="Show one past session by id")
    s.add_argument("id", type=int, help="Session id (from `voicefix history`)")
    s.set_defaults(func=cmd_show)

    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
