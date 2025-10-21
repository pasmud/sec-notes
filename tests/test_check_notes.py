"""Exercise the checker on small, synthetic notebook trees."""

import os
import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.check_notes import check

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "tools" / "check_notes.py"


class CheckerTests(unittest.TestCase):
    def setUp(self):
        space = TemporaryDirectory(dir=REPO)
        self.addCleanup(space.cleanup)
        self.root = Path(space.name) / "notebook"
        self.root.mkdir()

    def put(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")
        return file

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_index_reaches_pages_transitively_with_a_cycle(self):
        self.put("README.md", "[Guide](notes/guide.md#start_here) [License](LICENSE)\n")
        self.put("LICENSE", "Synthetic license fixture\n")
        self.put("notes/guide.md", "# Start_here!\n[Report](../examples/report.md)\n")
        self.put("examples/report.md", "[Index](../README.md)\n")
        self.assertEqual(check(self.root), (3, []))

    def test_disconnected_pages_cannot_make_each_other_reachable(self):
        self.put("README.md", "# Index\n")
        self.put("notes/a.md", "[Peer](b.md)\n")
        self.put("notes/b.md", "[Peer](a.md)\n")
        self.assertEqual(check(self.root), (3, [
            "notes/a.md: not reachable from README.md",
            "notes/b.md: not reachable from README.md",
        ]))

    def test_missing_file_and_heading_report_source_lines(self):
        self.put("README.md", "# Index\n[Read](#index)\n[File](absent.md) [Title](#absent)\n")
        self.assertEqual(check(self.root), (1, [
            "README.md:3: 'absent.md': target does not exist",
            "README.md:3: '#absent': heading #absent does not exist",
        ]))

    def test_bad_fragment_does_not_count_toward_reachability(self):
        self.put("README.md", "[Guide](notes/guide.md#absent)\n")
        self.put("notes/guide.md", "# Present\n")
        self.assertEqual(check(self.root), (2, [
            "README.md:1: 'notes/guide.md#absent': heading #absent does not exist",
            "notes/guide.md: not reachable from README.md",
        ]))

    def test_duplicate_normalized_heading_is_ambiguous(self):
        self.put("README.md", "# A heading!\n\n## a heading ##\n")
        self.assertEqual(check(self.root), (1, [
            "README.md:3: duplicate anchor #a-heading (first on line 1)",
        ]))

    def test_literal_examples_images_and_external_urls_are_skipped(self):
        self.put("README.md", (
            "# Index\n````markdown\n```\n# Index\n[example](absent.md)\n````\n"
            "~~~\n[example](absent.md)\n~~~\n`[example](absent.md)`\n"
            "![Image](absent.png) [Web](https://example.invalid/page) "
            "[Web](http://example.invalid) [Mail](mailto:review@example.invalid)\n"
        ))
        self.assertEqual(check(self.root), (1, []))

    def test_unclosed_fence_is_reported(self):
        self.put("README.md", "# Index\n```text\n[example](absent.md)\n~~~\n")
        self.assertEqual(check(self.root), (1, ["README.md:2: unclosed code fence"]))

    def test_invalid_destinations_are_reported(self):
        self.put("README.md", (
            "[a]() [b](#) [c](/README.md) [d](//example.invalid/path) "
            "[e](two words.md) [f](README.md?x) [g](notes/../README.md) "
            "[h](%2e%2e/file.md)\n"
        ))
        count, issues = check(self.root)
        self.assertEqual(count, 1)
        self.assertEqual(len(issues), 8)
        self.assertIn("empty link destination", issues[0])
        self.assertIn("nonempty heading fragment", issues[1])
        self.assertTrue(all("relative file path" in issue for issue in issues[2:]))

    def test_links_cannot_traverse_above_root_even_to_existing_file(self):
        self.put("../outside.md", "# Outside\n")
        self.put("README.md", "[Outside](../outside.md) [Guide](notes/guide.md)\n")
        self.put("notes/guide.md", "[Outside](../../outside.md)\n")
        self.assertEqual(check(self.root), (2, [
            "README.md:1: '../outside.md': path leaves the notebook root",
            "notes/guide.md:1: '../../outside.md': path leaves the notebook root",
        ]))

    def test_directory_and_non_notebook_fragment_are_rejected(self):
        self.put("README.md", "[Dir](notes) [Title](other.md#name)\n")
        self.put("other.md", "# Name\n")
        (self.root / "notes").mkdir()
        self.assertEqual(check(self.root), (1, [
            "README.md:1: 'notes': expected a regular file",
            "README.md:1: 'other.md#name': fragments require a readable notebook page",
        ]))

    @unittest.skipUnless(os.name == "posix", "fixture requires symbolic links")
    def test_symlink_pages_and_intermediate_directories_are_rejected(self):
        self.put("README.md", "[File](notes/alias.md) [Dir](examples/other.md)\n")
        outside = self.put("../external/other.md", "# Outside\n")
        notes = self.root / "notes"
        notes.mkdir()
        (notes / "alias.md").symlink_to(outside)
        (self.root / "examples").symlink_to(outside.parent, target_is_directory=True)
        self.assertEqual(check(self.root), (1, [
            "examples: symlinks are not supported",
            "notes/alias.md: symlinks are not supported",
            "README.md:1: 'notes/alias.md': symlinks are not supported",
            "README.md:1: 'examples/other.md': symlinks are not supported",
        ]))

    def test_invalid_utf8_is_reported_without_a_traceback(self):
        self.put("README.md", "[Guide](notes/guide.md)\n")
        bad = self.put("notes/guide.md", "")
        bad.write_bytes(b"\xff")
        self.assertEqual(check(self.root), (1, ["notes/guide.md: expected UTF-8 text"]))

    def test_missing_index_is_reported(self):
        self.put("notes/guide.md", "# Guide\n")
        self.assertEqual(check(self.root), (1, ["README.md: cannot read notebook page"]))

    def test_cli_default_root_and_success_exit(self):
        self.put("README.md", "# Index\n")
        result = self.run_cli()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Checked 1 notebook page(s); no issues.\n")
        self.assertEqual(result.stderr, "")

    def test_cli_issue_exit_for_invalid_root(self):
        file = self.put("README.md", "# Index\n")
        result = self.run_cli(str(file))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("root: expected a directory", result.stderr)

    def test_cli_usage_exit_for_extra_argument(self):
        result = self.run_cli("one", "two")
        self.assertEqual(result.returncode, 2)
        self.assertIn("usage:", result.stderr)


if __name__ == "__main__":
    unittest.main()
