from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_fractal.source_candidate_builder import build_candidate_artifact


class SourceBackedCandidateTests(unittest.TestCase):
    def test_gate13_candidate_is_deterministic_and_provenance_preserving(self) -> None:
        first = build_candidate_artifact()
        second = build_candidate_artifact()

        self.assertEqual(first["artifact_hash"], second["artifact_hash"])
        self.assertEqual(
            first["composition"]["fragment"]["model_hash"],
            second["composition"]["fragment"]["model_hash"],
        )
        self.assertEqual(first["status"], "CANDIDATE_NOT_RELEASED")
        self.assertEqual(first["composition"]["status"], "COMPOSITION_CANDIDATE_READY_FOR_TESTS")
        self.assertEqual(first["composition"]["fragment"]["status"], "CANDIDATE")
        self.assertEqual(first["invariants"]["semantic_equivalence"], "NOT_ESTABLISHED")
        self.assertTrue(first["invariants"]["source_lineage_preserved"])
        self.assertTrue(first["invariants"]["parent_ids_preserved"])
        self.assertEqual(first["test_outcomes"]["semantic_ground_truth"], "NOT_RUN")
        self.assertEqual(first["test_outcomes"]["holdout"], "NOT_CREATED")
        self.assertEqual(first["readiness_contribution"]["source_grounded_counterexamples_counted"], 0)
        self.assertEqual(first["readiness_contribution"]["semantic_benchmark_cases_counted"], 0)

    def test_composition_rule_is_registered_and_active(self) -> None:
        rules = json.loads((ROOT / "logic_fractal" / "data" / "composition_rules.json").read_text(encoding="utf-8"))
        rule = next(item for item in rules["rules"] if item["id"] == "COMPOSE-INTERFACE-SEQUENTIAL-V1")
        self.assertEqual(rule["status"], "ACTIVE_SPECIFIED")

    def test_unresolved_source_count_mismatch_remains_unadjudicated(self) -> None:
        artifact = build_candidate_artifact()
        mismatch = next(item for item in artifact["counterexample_candidates"] if item["id"] == "CE-G13-COUNT-001")
        self.assertEqual(mismatch["status"], "REQUIRES_REVIEW_NOT_COUNTED")
        self.assertEqual(mismatch["stated_count"], 18)
        self.assertEqual(mismatch["enumerated_item_count"], 17)


if __name__ == "__main__":
    unittest.main()
