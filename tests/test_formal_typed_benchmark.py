from __future__ import annotations

import unittest
from pathlib import Path

from formal_reasoning.typed_benchmark import run_typed_benchmark_suite

ROOT = Path(__file__).resolve().parents[1]


class TypedFormalLogicBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import z3  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("optional dependency z3-solver is not installed") from exc

    def test_synthetic_fixture_suite_passes_without_claiming_semantic_verification(self):
        report = run_typed_benchmark_suite(ROOT / "formal_reasoning/examples/typed_formal_cases.json")
        self.assertEqual(report["status"], "PASS", report["results"])
        self.assertEqual(report["case_count"], 7)
        self.assertEqual(report["passed_cases"], 7)
        self.assertEqual(report["failed_cases"], 0)
        self.assertEqual(report["semantic_status"], "NOT_YET_VERIFIED")
        self.assertTrue("not_source_grounded" in report["fixture_status"].lower())

    def test_benchmark_ids_are_unique(self):
        report = run_typed_benchmark_suite(ROOT / "formal_reasoning/examples/typed_formal_cases.json")
        ids = [result["case_id"] for result in report["results"]]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
