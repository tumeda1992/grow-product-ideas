import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from memo_day import extract


SCRIPT = Path(__file__).with_name("memo_day.py")


class ReceiverTest(unittest.TestCase):
    def run_cli(self, date, raw):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory, "memo.txt")
            path.write_bytes(raw)
            before = (path.read_bytes(), path.stat().st_mtime_ns)
            result = subprocess.run(
                [sys.executable, SCRIPT, date, path], capture_output=True
            )
            after = (path.read_bytes(), path.stat().st_mtime_ns)
            self.assertEqual(before, after)
            return result

    def test_duplicate_unordered_and_preamble(self):
        raw = b"pre\n## 2026-09-13\na\n## 2026-09-12\nb\n## 2026-09-13\nc"
        self.assertEqual(extract(raw, "2026-09-13"), (True, b"a\nc"))

    def test_non_headings_remain_body(self):
        raw = b"## 2026-09-13\n##  2026-09-14\n## 2026-02-30\n## 2026-09-14 suffix\n"
        expected = b"##  2026-09-14\n## 2026-02-30\n## 2026-09-14 suffix\n"
        self.assertEqual(extract(raw, "2026-09-13"), (True, expected))

    def test_empty_found_and_missing_differ(self):
        found = self.run_cli("2026-09-13", b"## 2026-09-13\n## 2026-09-14\nx\n")
        missing = self.run_cli("2026-09-12", b"## 2026-09-13\n")
        self.assertEqual((found.returncode, found.stdout), (0, b""))
        self.assertEqual((missing.returncode, missing.stdout), (1, b""))

    def test_crlf_and_missing_final_newline_preserved(self):
        result = self.run_cli("2026-09-13", b"## 2026-09-13\r\na\r\nb")
        self.assertEqual((result.returncode, result.stdout), (0, b"a\r\nb"))

    def test_invalid_utf8_has_no_partial_output(self):
        result = self.run_cli("2026-09-13", b"## 2026-09-13\nok\n\xff")
        self.assertEqual((result.returncode, result.stdout), (2, b""))

    def test_invalid_target(self):
        result = self.run_cli("2026-02-30", b"## 2026-02-28\nx\n")
        self.assertEqual((result.returncode, result.stdout), (2, b""))

    def test_directory_and_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            for path in (Path(directory), Path(directory, "absent")):
                result = subprocess.run(
                    [sys.executable, SCRIPT, "2026-09-13", path],
                    capture_output=True,
                )
                self.assertEqual((result.returncode, result.stdout), (2, b""))


if __name__ == "__main__":
    unittest.main()
