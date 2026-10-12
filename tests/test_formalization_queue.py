from __future__ import annotations

import unittest

from formal_reasoning.formalization_queue import queue_candidate_for_formalization


class FormalizationQueueTests(unittest.TestCase):
    def test_source_linked_candidate_is_queued_without_inventing_an_ast(self):
        candidate = {
            "package_id": "LT-0123456789abcdef",
            "version": "0.1",
            "status": "INTERNAL_CANDIDATE_NOT_RELEASED",
            "member_articles": [
                {"id": "logical-fractal", "definition": "A recursive composition pattern.", "source_refs": ["SRC-1"]},
                {"id": "evidence-provenance", "definition": "A source lineage record.", "source_refs": ["SRC-2"]},
            ],
            "sources": [{"id": "SRC-1"}, {"id": "SRC-2"}],
        }
        item = queue_candidate_for_formalization(candidate)
        self.assertEqual(item["status"], "READY_FOR_FORMALIZATION")
        self.assertEqual(item["solver_execution_status"], "NOT_RUN_NO_FORMAL_AST")
        self.assertFalse(item["automatic_semantic_conversion"])
        self.assertEqual(item["semantic_status"], "NOT_YET_VERIFIED")
        self.assertTrue(all(x["formalization_status"] == "NOT_FORMALIZED" for x in item["candidate_claims"]))
        self.assertIn("formal_premises", item["missing_formal_fields"])

    def test_missing_source_blocks_formalization_queue(self):
        candidate = {
            "package_id": "LT-aaaaaaaaaaaaaaaa",
            "member_articles": [{"id": "claim-1", "definition": "No source here.", "source_refs": ["MISSING"]}],
            "sources": [{"id": "SRC-1"}],
        }
        item = queue_candidate_for_formalization(candidate)
        self.assertEqual(item["status"], "BLOCKED_SOURCE_REVIEW")
        self.assertEqual(item["unresolved_sources"][0]["article_id"], "claim-1")

    def test_empty_candidate_is_rejected(self):
        with self.assertRaises(ValueError):
            queue_candidate_for_formalization({"package_id": "LT-X", "member_articles": [], "sources": []})


if __name__ == "__main__":
    unittest.main()
