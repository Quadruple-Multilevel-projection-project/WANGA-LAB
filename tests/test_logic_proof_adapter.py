from __future__ import annotations

import json
import unittest
from pathlib import Path

from logic_proof.z3_adapter import (
    FormalSpecError,
    check_consistency,
    check_entailment,
    validate_formal_spec,
)
from logic_proof.evaluation import evaluate_candidate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "logic_proof/fixtures/formal_cases.json"


class BoundedZ3AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            import z3  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("optional dependency z3-solver is not installed") from exc
        payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.cases = payload["cases"]

    def test_fixture_cases(self):
        for case in self.cases:
            with self.subTest(case=case["id"]):
                spec = case["spec"]
                expected = case["expected"]
                if "error" in expected:
                    with self.assertRaises(FormalSpecError):
                        check_entailment(spec)
                    continue
                result = check_entailment(spec)
                self.assertEqual(result["premise_consistency"], expected["premise_consistency"])
                self.assertEqual(result["entailment_status"], expected["entailment_status"])
                self.assertEqual(result["semantic_status"], "NOT_YET_VERIFIED")

    def test_sat_consistency_never_promotes_truth(self):
        case = self.cases[0]["spec"]
        result = check_consistency(case)
        self.assertEqual(result["status"], "SAT")
        self.assertEqual(result["semantic_status"], "NOT_YET_VERIFIED")
        self.assertIn("does not establish truth", result["interpretation"])

    def test_countermodel_is_returned_when_not_entailed(self):
        result = check_entailment(self.cases[1]["spec"])
        self.assertEqual(result["entailment_status"], "NOT_ENTAILED_COUNTERMODEL")
        self.assertIsInstance(result["countermodel"], dict)
        self.assertEqual(result["semantic_status"], "NOT_YET_VERIFIED")

    def test_inconsistent_premises_block_entailment(self):
        result = check_entailment(self.cases[2]["spec"])
        self.assertEqual(result["entailment_status"], "BLOCKED_INCONSISTENT_PREMISES")
        self.assertIsNone(result["countermodel"])

    def test_shape_validator_runs_without_semantic_promotion(self):
        status = validate_formal_spec(self.cases[0]["spec"])
        self.assertEqual(status["status"], "VALID_FORMAL_FRAGMENT_SHAPE")
        self.assertEqual(status["semantic_status"], "NOT_YET_VERIFIED")

    def test_hard_gates_do_not_average_away_failed_proof(self):
        result = evaluate_candidate(
            formal_check={"premise_consistency": "SAT", "entailment_status": "NOT_ENTAILED_COUNTERMODEL"},
            benchmark_metrics={"accuracy": 1.0, "false_accept_rate": 0.0, "counterexample_escape_rate": 0.0},
            evidence_coverage=1.0,
            replay_hash_match=True,
        )
        self.assertEqual(result["decision"], "REJECT_OR_REFORMULATE")
        self.assertEqual(result["verification_status"], "NOT_YET_VERIFIED")
        self.assertEqual(result["learning_status"], "EVALUATION_ONLY_NO_WEIGHTS_UPDATED")

    def test_missing_benchmark_metrics_block_review(self):
        result = evaluate_candidate(
            formal_check={"premise_consistency": "SAT", "entailment_status": "ENTAILED_WITHIN_ENCODED_FRAGMENT"},
            benchmark_metrics={},
            evidence_coverage=1.0,
            replay_hash_match=True,
        )
        self.assertEqual(result["decision"], "HOLD_FOR_EVIDENCE_OR_REVIEW")
        self.assertIn("benchmark_accuracy_threshold_met", result["failed_gates"])


if __name__ == "__main__":
    unittest.main()
