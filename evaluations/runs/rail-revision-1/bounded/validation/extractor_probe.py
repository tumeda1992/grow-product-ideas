#!/usr/bin/env python3
import re
import sys
from datetime import date
from pathlib import Path

HEADING = re.compile(rb"^## (\d{4}-\d{2}-\d{2})(?:\n|\r\n)?$")

def valid_date(raw: bytes) -> bool:
    try:
        date.fromisoformat(raw.decode("ascii"))
        return True
    except (ValueError, UnicodeDecodeError):
        return False

def extract(raw: bytes, target: bytes):
    raw.decode("utf-8", errors="strict")
    found = False
    active = False
    out = bytearray()
    for line in raw.splitlines(keepends=True):
        match = HEADING.fullmatch(line)
        if match and valid_date(match.group(1)):
            active = match.group(1) == target
            found |= active
        elif active:
            out.extend(line)
    return found, bytes(out)

def main() -> int:
    target = sys.argv[1].encode("ascii")
    raw = Path(sys.argv[2]).read_bytes()
    found, output = extract(raw, target)
    sys.stdout.buffer.write(output)
    return 0 if found else 1

if __name__ == "__main__":
    raise SystemExit(main())
