"""Real CLI regressions for quoted references, containers, and code examples."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).resolve().parents[1] / 'check-plan-links.py'


class QuotedReferences(unittest.TestCase):
    def check_document(self, text, code, target=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text(text, encoding='utf-8')
            if target:
                (root / 'evidence.md').write_text('# 根拠\n', encoding='utf-8')
            result = subprocess.run([sys.executable, str(CHECKER), str(root)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, code, result.stdout + result.stderr)
            return json.loads(result.stdout)

    def test_quoted_missing_definition_target(self):
        result = self.check_document('> [根拠]: missing.md\n>\n> この判断は[根拠]に依る。\n', 2)
        self.assertEqual(result['local_links'], 1)
        self.assertEqual([(x['line'], x['kind']) for x in result['issues']], [(1, 'missing-target')])

    def test_quoted_valid_target_and_anchor(self):
        self.assertTrue(self.check_document('> [根拠]: evidence.md#根拠\n> [根拠]\n', 0, True)['ok'])

    def test_unquoted_missing(self):
        self.assertFalse(self.check_document('[根拠]: missing.md\n[根拠]\n', 2)['ok'])

    def test_nested_quote_forward_reference(self):
        self.assertEqual(self.check_document('> > [詳しく][根拠]\n> >\n> > [根拠]: missing.md\n', 2)['local_links'], 1)

    def test_quoted_fence_is_not_a_link(self):
        result = self.check_document('> ```md\n> [根拠]: missing.md\n> [根拠]\n> ```\n', 0)
        self.assertEqual(result['local_links'], 0)

    def test_quoted_fence_does_not_hide_following_parent(self):
        self.assertEqual(self.check_document('> ```md\n> [例]: ignored.md\n\n[根拠]: missing.md\n', 2)['local_links'], 1)

    def test_nested_fence_ends_at_parent_quote(self):
        self.assertEqual(self.check_document('> > ~~~md\n> > [例]: ignored.md\n> [根拠]: missing.md\n', 2)['local_links'], 1)

    def test_root_fence_keeps_quoted_examples_as_code(self):
        self.assertEqual(self.check_document('```md\n> [例]: ignored.md\n```\n', 0)['local_links'], 0)

    def test_quote_marker_cannot_close_root_code(self):
        self.assertEqual(self.check_document('```md\n> ```\n[例]: ignored.md\n```\n', 0)['local_links'], 0)

    def test_nested_marker_cannot_close_parent_quoted_code(self):
        self.assertEqual(self.check_document('> ```md\n> > ```\n> [例]: ignored.md\n> ```\n', 0)['local_links'], 0)

    def test_quoted_comment_is_not_a_link(self):
        self.assertEqual(self.check_document('> <!--\n> [例]: ignored.md\n> -->\n', 0)['local_links'], 0)

    def test_quote_link_to_heading(self):
        self.assertTrue(self.check_document('> # 根拠\n\n[参照](#根拠)\n', 0)['ok'])


if __name__ == '__main__':
    unittest.main()
