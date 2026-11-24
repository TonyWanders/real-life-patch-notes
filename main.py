#!/usr/bin/env python3
"""Write one real-life patch note to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The entry is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 160 characters, not only white space. Pass -h or
--help as the first argument to print a usage line instead of writing.
A write that fails (missing directory permissions, a full disk) prints
a plain error and exits 1 instead of a traceback.
"""

import os
import sys
from pathlib import Path

ENTRY = "v5.1.0: Fixed bug where the body woke up one minute before the alarm every morning; sleep now ends on schedule, not one minute early."

MIN_CHARS = 1
MAX_CHARS = 160
DEFAULT_PATH = "/output/entry.txt"


USAGE = "usage: python3 main.py [-h | --help] [output-path]"


def resolve_output_path() -> Path:
    """Pick the output path: argv[1], then $OUTPUT_PATH, then the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    env_path = os.environ.get("OUTPUT_PATH")
    if env_path:
        return Path(env_path)
    return Path(DEFAULT_PATH)


def validate(text: str) -> int:
    """Enforce the competition gate: 1 to 160 chars, not only white space.

    Returns the character count. Raises ValueError when the gate fails.
    """
    chars = len(text)
    if not (MIN_CHARS <= chars <= MAX_CHARS):
        raise ValueError(f"entry is {chars} characters, outside 1-160")
    if not text.strip():
        raise ValueError("entry is only white space")
    if "\n" in text:
        raise ValueError("entry must be one line")
    return chars


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(USAGE)
        return 0

    try:
        chars = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    path = resolve_output_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(ENTRY, encoding="utf-8")
    except OSError as exc:
        print(f"cannot write {path}: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
