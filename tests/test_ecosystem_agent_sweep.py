from __future__ import annotations
import os
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import scan_github_ecosystem as scan


class SummarizationTests(unittest.TestCase):
    def test_readme_summary_extracts_title_and_surface_terms(self):
        result=scan.summarize_readme(
            "# Neural Thinking Machine\nA research architecture for logical agents, evidence and provenance."
        )
        self.assertEqual(result["title"],"Neural Thinking Machine")
        self.assertTrue(result["relevance_candidate"])
        self.assertIn("agent",result["relevance_signals"])
        self.assertEqual(result["semantic_status"],"README_SURFACE_CUES_ONLY")

    def test_readme_summary_bounds_excerpt_length(self):
        result=scan.summarize_readme("# Project\n"+"logic "*500,max_chars=100)
        self.assertLessEqual(len(result["excerpt"]),100)

    def test_batch_selection_rotates_deterministically(self):
        items=[{"full_name":f"org/repo-{n}"} for n in range(25)]
        a,cursor=scan.select_batch(items,limit=10,run_number=1)
        b,_=scan.select_batch(items,limit=10,run_number=2)
        c,_=scan.select_batch(items,limit=10,run_number=3)
        names=[x["full_name"] for x in a+b+c]
        self.assertEqual(len(names),25)
        self.assertEqual(len(set(names)),25)
        self.assertEqual(cursor,10)

    def test_empty_batch_is_valid(self):
        self.assertEqual(scan.select_batch([],limit=10,run_number=1),([],0))

    def test_unknown_visibility_is_redacted(self):
        record=scan._public_record({"full_name":"private-or-unknown/repo","private":None},"unused")
        self.assertEqual(record,{"status":"SKIPPED_PRIVATE_OR_VISIBILITY_UNKNOWN"})

    def test_private_repository_name_is_redacted(self):
        record=scan._public_record({"full_name":"secret-owner/private-repo","private":True},"unused")
        self.assertNotIn("full_name",record)
        self.assertNotIn("secret-owner",str(record))

    def test_doc_path_filter_matches_logic_and_agent_paths(self):
        paths=[
          "README.md","logic_fractal/fragment_composer.py","docs/ARCHITECTURE.md",
          "src/agent_runner.py","tests/test_something.py","src/math_ops.py"
        ]
        selected=[p for p in paths if scan.DOC_PATH.search(p)]
        self.assertIn("README.md",selected)
        self.assertIn("logic_fractal/fragment_composer.py",selected)
        self.assertIn("docs/ARCHITECTURE.md",selected)
        self.assertIn("src/agent_runner.py",selected)

    def test_no_secret_values_are_embedded_in_module(self):
        source=(ROOT/"scripts"/"scan_github_ecosystem.py").read_text(encoding="utf-8")
        self.assertNotRegex(source,r"(ghp_[A-Za-z0-9]{20,}|sk-proj-[A-Za-z0-9_-]{20,})")


if __name__=="__main__":
    unittest.main()
