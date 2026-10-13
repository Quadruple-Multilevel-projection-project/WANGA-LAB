from __future__ import annotations

import json
import unittest
from unittest.mock import patch
from pathlib import Path

from formal_reasoning.typed_fragment import (
    FormalSpecError,
    check_consistency,
    check_entailment,
    validate_formal_spec,
)
from formal_reasoning.evaluation import evaluate_candidate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "formal_reasoning/examples/typed_formal_cases.json"


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

    def test_premises_require_sources_or_explicit_assumptions(self):
        from copy import deepcopy
        spec = deepcopy(self.cases[0]["spec"])
        spec["premises"][0]["source_refs"] = []
        spec["premises"][0]["assumption"] = False
        with self.assertRaises(FormalSpecError):
            check_entailment(spec)

    def test_shape_validator_runs_without_semantic_promotion(self):
        status = validate_formal_spec(self.cases[0]["spec"])
        self.assertEqual(status["status"], "VALID_FORMAL_FRAGMENT_SHAPE")
        self.assertEqual(status["semantic_status"], "NOT_YET_VERIFIED")

    def test_unknown_is_preserved_as_unresolved(self):
        import z3
        from formal_reasoning import typed_fragment as z3_adapter

        class UnknownSolver:
            def set(self, **kwargs):
                return None

            def add(self, *args):
                return None

            def check(self):
                return z3.unknown

            def reason_unknown(self):
                return "test timeout"

        with patch.object(z3_adapter.z3, "Solver", return_value=UnknownSolver()):
            result = check_entailment(self.cases[0]["spec"])
        self.assertEqual(result["premise_consistency"], "UNKNOWN")
        self.assertEqual(result["entailment_status"], "UNKNOWN")
        self.assertEqual(result["semantic_status"], "NOT_YET_VERIFIED")
        self.assertIn("not evaluated as proven", result["interpretation"])

    def test_hard_gates_do_not_average_away_failed_proof(self):
        result = evaluate_candidate({
            "source_coverage": 1.0,
            "evidence_coverage": 1.0,
            "benchmark_accuracy": 1.0,
            "counterexample_rate": 0.0,
            "false_accept_rate": 0.0,
            "counterexample_escape_rate": 0.0,
            "holdout_score": 1.0,
            "compute_seconds": 0.1,
            "premises_consistent": True,
            "formal_checks_pass": False,
            "replay_stable": True,
        })
        self.assertEqual(result["status"], "BLOCKED_BY_HARD_GATE")
        self.assertFalse(result["all_hard_gates_pass"])
        self.assertFalse(result["weight_update_performed"])
        self.assertEqual(result["verification_status"], "NOT_YET_VERIFIED")

    def test_evidence_and_error_rate_gates_are_independent(self):
        metrics = {
            "source_coverage": 1.0,
            "evidence_coverage": 0.50,
            "benchmark_accuracy": 1.0,
            "counterexample_rate": 0.0,
            "false_accept_rate": 0.0,
            "counterexample_escape_rate": 0.0,
            "holdout_score": 1.0,
            "compute_seconds": 0.1,
            "premises_consistent": True,
            "formal_checks_pass": True,
            "replay_stable": True,
        }
        result = evaluate_candidate(metrics)
        self.assertFalse(result["hard_gates"]["evidence_coverage"])
        self.assertEqual(result["status"], "BLOCKED_BY_HARD_GATE")

        metrics["evidence_coverage"] = 1.0
        metrics["counterexample_escape_rate"] = 0.1
        result = evaluate_candidate(metrics)
        self.assertFalse(result["hard_gates"]["counterexample_escape_rate"])
        self.assertEqual(result["status"], "BLOCKED_BY_HARD_GATE")

    def test_missing_benchmark_metrics_are_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_candidate({"source_coverage": 1.0})


if __name__ == "__main__":
    unittest.main()
