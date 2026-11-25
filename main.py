#!/usr/bin/env python3
"""Write the entry text to entry.txt.

Entry for make.fun's "The Funniest Sick-Day Excuse" (submitted as
"Locked In by My Own Lock"). A fresh, half-believable excuse that
reads like a real message: an overnight smart-lock update decided
its owner's face is 'suspicious activity' and locked them in with
their own groceries — the twist lands on the last phrase, and the
worn fever/dog/grandmother excuses are avoided.

Deterministic: a fixed text, no network, no randomness, no clock.
The entry text and the bytes written are unchanged from the
original submission.

Entrypoint notes: this script is the whole entry. Running it
validates the fixed one-line sick-day excuse against the brief's
length and single-line rules, writes it as entry.txt under the
output directory, and verifies the bytes by reading them back.
Nothing else is read, fetched, or computed at runtime.
"""
import os
from pathlib import Path

LINE = "Can't come in today - my smart lock updated overnight, decided my face is 'suspicious activity', and has locked me in with my own groceries."
TEXT = LINE + "\n"
MAX_CHARS = 199
ENTRY_FILENAME = "entry.txt"


def validate(text: str) -> None:
    """Check the entry body obeys the one-line, length-capped brief."""
    body = text[:-1] if text.endswith("\n") else text
    if not (1 <= len(body) <= MAX_CHARS):
        raise ValueError("entry length out of range")
    if not body.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in body or "\r" in body:
        raise ValueError("entry must be exactly one line")


def write_entry(text: str) -> Path:
    """Write text to entry.txt under the output dir; verify by read-back."""
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / ENTRY_FILENAME
    target.write_bytes(text.encode("utf-8"))
    if target.read_bytes() != text.encode("utf-8"):
        raise IOError("read-back mismatch")
    return target


def main() -> None:
    validate(TEXT)
    write_entry(TEXT)


if __name__ == "__main__":
    main()
