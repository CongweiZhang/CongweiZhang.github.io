#!/usr/bin/env python3
"""Fast checks for the BibTeX ingestion pipeline."""
import tempfile
import unittest
from pathlib import Path
from build_publications import BibError, generate, parse_bibtex


class PublicationTests(unittest.TestCase):
    def test_nested_braces(self):
        _, key, values = parse_bibtex(
            '@article{test2026,title={A {MoE} System},author={One and Two},year={2026},url="https://example.org"}'
        )
        self.assertEqual(key, "test2026")
        self.assertEqual(values["title"], "A {MoE} System")
        self.assertEqual(values["url"], "https://example.org")

    def test_reject_multiple_entries(self):
        with self.assertRaises(BibError):
            parse_bibtex("@article{a,title={A},author={X},year=2026}\n@article{b,title={B},author={Y},year=2026}")

    def test_generates_site_data(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            paper = root / "content/publications/sample"
            paper.mkdir(parents=True)
            (paper / "paper.bib").write_text("@misc{sample2026,title={Sample},author={Author One and Author Two},year=2026}", encoding="utf-8")
            (paper / "metadata.yaml").write_text("featured: true\norder: 3\n", encoding="utf-8")
            result = generate(root)
            self.assertEqual(len(result), 1)
            self.assertTrue(result[0]["featured"])
            self.assertTrue((root / "static/publications.bib").exists())
            self.assertTrue((root / "static/bib/sample2026.bib").exists())


if __name__ == "__main__":
    unittest.main()
