#!/usr/bin/env python3
from extractor_probe import extract

cases = [
    ("duplicate/out-of-order", "preface\n## 2026-09-13\nA\n## 2026-09-12\nX\n## 2026-09-13\nB\n", b"2026-09-13", True, b"A\nB\n"),
    ("empty match", "## 2026-09-13\n## 2026-09-14\nB\n", b"2026-09-13", True, b""),
    ("absent", "## 2026-09-14\nB\n", b"2026-09-13", False, b""),
    ("strict spacing", "##  2026-09-13\nnot heading\n## 2026-09-13 extra\nalso text\n", b"2026-09-13", False, b""),
    ("invalid heading is content", "## 2026-09-13\nA\n## 2026-02-30\nstill A\n## 2026-09-14\n", b"2026-09-13", True, b"A\n## 2026-02-30\nstill A\n"),
    ("no final newline", "## 2026-09-13\n末尾", b"2026-09-13", True, "末尾".encode()),
    ("CRLF preserved", "## 2026-09-13\r\nA\r\n", b"2026-09-13", True, b"A\r\n"),
]

for name, text, target, expected_found, expected_output in cases:
    found, output = extract(text.encode(), target)
    assert (found, output) == (expected_found, expected_output), (name, found, output)

try:
    extract(b"## 2026-09-13\n\xff", b"2026-09-13")
except UnicodeDecodeError:
    pass
else:
    raise AssertionError("invalid UTF-8 accepted")

print(f"PASS: {len(cases) + 1} cases")
