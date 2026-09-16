#!/usr/bin/env python3
import datetime
import re
import sys
from pathlib import Path


DATE_RE = re.compile(r"\A\d{4}-\d{2}-\d{2}\Z", re.ASCII)
HEADING_RE = re.compile(rb"^## (\d{4}-\d{2}-\d{2})(?:\n|\r\n)?$")


def parse_target(value):
    if not DATE_RE.fullmatch(value):
        raise ValueError("invalid date format")
    datetime.date.fromisoformat(value)
    return value


def _valid_heading(line):
    match = HEADING_RE.fullmatch(line)
    if not match:
        return None
    value = match.group(1).decode("ascii")
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return None
    return value


def extract(raw, target):
    raw.decode("utf-8", errors="strict")
    found = False
    selected = False
    output = []
    for line in raw.splitlines(keepends=True):
        heading = _valid_heading(line)
        if heading is not None:
            selected = heading == target
            found = found or selected
        elif selected:
            output.append(line)
    return found, b"".join(output)


def main(argv):
    if len(argv) != 2:
        print("usage: memo_day.py DATE FILE", file=sys.stderr)
        return 2
    date_arg, file_arg = argv
    try:
        target = parse_target(date_arg)
        path = Path(file_arg)
        if not path.is_file():
            raise OSError(f"not a regular file: {path}")
        raw = path.read_bytes()
        found, result = extract(raw, target)
    except (ValueError, UnicodeDecodeError, OSError) as exc:
        print(f"error: {file_arg}: {exc}", file=sys.stderr)
        return 2
    if not found:
        print(f"not found: {target}: {file_arg}", file=sys.stderr)
        return 1
    sys.stdout.buffer.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
