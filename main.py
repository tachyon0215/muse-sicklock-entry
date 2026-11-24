#!/usr/bin/env python3
"""Write the entry text to entry.txt.

Entry for make.fun's "The Funniest Sick-Day Excuse" (submitted as
"Locked In by My Own Lock"). A fresh, half-believable excuse that
reads like a real message: an overnight smart-lock update decided
its owner's face is 'suspicious activity' and locked them in with
their own groceries — the twist lands on the last phrase, and the
worn fever/dog/grandmother excuses are avoided.

Deterministic: a fixed text, no network, no randomness, no clock.
Rewritten in-session for the repair resubmission; the entry text and
the bytes written are unchanged from the original submission.
"""
import os
from pathlib import Path

LINE = "Can't come in today - my smart lock updated overnight, decided my face is 'suspicious activity', and has locked me in with my own groceries."
TEXT = LINE + "\n"
MAX_CHARS = 199


def validate(text: str) -> None:
    body = text[:-1] if text.endswith("\n") else text
    if not (1 <= len(body) <= MAX_CHARS):
        raise ValueError("entry length out of range")
    if not body.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in body or "\r" in body:
        raise ValueError("entry must be exactly one line")


def main() -> None:
    validate(TEXT)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_bytes(TEXT.encode("utf-8"))
    if target.read_bytes() != TEXT.encode("utf-8"):
        raise IOError("read-back mismatch")


if __name__ == "__main__":
    main()
