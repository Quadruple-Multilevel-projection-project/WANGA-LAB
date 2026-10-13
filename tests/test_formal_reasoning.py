from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from formal_reasoning.evaluation import DEFAULT_THRESHOLDS, evaluate_candidate
from formal_reasoning.propositional import (
    FormalInputError,
    FormulaParser,
    _map_solver_result,
    analyze_claim,
    analyze_claim_batch,
)
from formal_reasoning.benchmark import run_benchmark_suite

HAS_Z3 = importlib.util.find_spec("z3") is not None
FIXTURES = ROOT / "formal_reasoning/examples/benchmark_cases.json"


@unittest.skipUnless(HAS_Z3, "z3-solver is installed by the formal-reasoning CI step")
class PropositionalAdapterTests(unittest.TestCase):
    def test_modus_ponens_is_entailed_within_encoding(self):
        result = analyze_claim({
            "claim_id": "T-MP",
            "variables": ["P", "Q"],
            "premises": ["P -> Q", "P"],
            "conclusion": "Q",
            "source_refs": ["fixture://test/mp"],
            "epistemic_status": "TEST_FIXTURE",
        })
        self.assertEqual(result["premise_consistency"], "SAT")
        self.assertEqual(result["status"], "ENTAILED_WITHIN_ENCODING")
        self.assertEqual(result["entailment"], "ENTAILED_WITHIN_PROPOSITIONAL_ENCODING")
        self.assertEqual(result["verification_status"], "NOT_YET_VERIFIED")
        self.assertEqual(result["epistemic_status_after"], "TEST_FIXTURE")

    def test_non_entailment_returns_countermodel(self):
        result = analyze_claim({
            "claim_id": "T-COUNTERMODEL",
            "variables": ["P", "Q"],
            "premises": ["P -> Q"],
            "conclusion": "P",
            "source_refs": ["fixture://test/countermodel"],
        })
        self.assertEqual(result["status"], "NOT_ENTAILED_BY_ENCODING")
        self.assertEqual(result["entailment"], "COUNTERMODEL_FOUND")
        model = result["countermodel"]
        self.assertFalse(model["P"])

    def test_inconsistent_premises_do_not_get_vacuous_entailment(self):
        result = analyze_claim({
            "claim_id": "T-INCONSISTENT",
            "variables": ["P"],
            "premises": ["P", "not P"],
            "conclusion": "P",
            "source_refs": ["fixture://test/inconsistent"],
        })
        self.assertEqual(result["status"], "INCONSISTENT_PREMISES")
        self.assertEqual(result["entailment"], "NOT_EVALUATED")

    def test_tautology_without_premises_is_entailed(self):
        result = analyze_claim({
            "claim_id": "T-TAUTOLOGY",
            "variables": ["P"],
            "premises": [],
            "conclusion": "P or not P",
            "source_refs": [],
        })
        self.assertEqual(result["status"], "ENTAILED_WITHIN_ENCODING")

    def test_undeclared_variable_rejected(self):
        with self.assertRaises(FormalInputError):
            analyze_claim({
                "claim_id": "T-UNDECLARED",
                "variables": ["P"],
                "premises": ["P"],
                "conclusion": "Q",
                "source_refs": [],
            })

    def test_formula_nesting_limit_is_enforced(self):
        with self.assertRaises(FormalInputError):
            FormulaParser("(" * 33 + "P" + ")" * 33, {"P"}).parse()

    def test_formula_character_limit_is_enforced(self):
        with self.assertRaises(FormalInputError):
            FormulaParser("P" + " " * 4096, {"P"}).parse()

    def test_unsupported_python_like_syntax_rejected(self):
        with self.assertRaises(FormalInputError):
            FormulaParser("__import__(P)", {"P"}).parse()

    def test_operator_precedence_and_parentheses(self):
        ast_a = FormulaParser("P or Q and R", {"P", "Q", "R"}).parse()
        ast_b = FormulaParser("P or (Q and R)", {"P", "Q", "R"}).parse()
        self.assertEqual(ast_a, ast_b)

    def test_unknown_result_is_not_coerced_to_sat(self):
        fake_z3 = SimpleNamespace(sat="sat", unsat="unsat")
        self.assertEqual(_map_solver_result("unknown", fake_z3), "UNKNOWN")

    def test_solver_result_does_not_promote_source_status(self):
        result = analyze_claim({
            "claim_id": "T-STATUS",
            "variables": ["P"],
            "premises": [],
            "conclusion": "P or not P",
            "source_refs": ["fixture://test/only-a-reference"],
            "epistemic_status": "HYPOTHESIS",
        })
        self.assertEqual(result["epistemic_status_after"], "HYPOTHESIS")
        self.assertEqual(result["verification_status"], "NOT_YET_VERIFIED")
        self.assertTrue(result["source_refs_supplied"])

    def test_fixed_benchmark_cases_pass(self):
        report = run_benchmark_suite(FIXTURES)
        self.assertEqual(report["status"], "PASS", report["cases"])
        self.assertEqual(report["case_count"], 5)
        self.assertEqual(report["passed"], 5)
        self.assertFalse(report["natural_language_truth_verified"])
        self.assertEqual(report["verification_status"], "NOT_YET_VERIFIED")


class CandidateEvaluationTests(unittest.TestCase):
    def good_metrics(self):
        return {
            "premises_consistent": True,
            "formal_checks_pass": True,
            "source_coverage": 1.0,
            "evidence_coverage": 1.0,
            "benchmark_accuracy": 0.98,
            "counterexample_rate": 0.0,
            "false_accept_rate": 0.0,
            "counterexample_escape_rate": 0.0,
            "holdout_score": 0.95,
            "replay_stable": True,
            "compute_seconds": 4.0,
        }

    def test_good_candidate_eligible_for_independent_review_only(self):
        result = evaluate_candidate(self.good_metrics())
        self.assertEqual(result["status"], "ELIGIBLE_FOR_INDEPENDENT_REVIEW")
        self.assertEqual(result["verification_status"], "NOT_YET_VERIFIED")
        self.assertFalse(result["weight_update_performed"])
        self.assertEqual(result["epistemic_status_promotion"], "FORBIDDEN")

    def test_hard_gate_cannot_be_offset_by_high_descriptive_score(self):
        metrics = self.good_metrics()
        metrics["source_coverage"] = 0.50
        result = evaluate_candidate(metrics)
        self.assertEqual(result["status"], "BLOCKED_BY_HARD_GATE")
        self.assertFalse(result["hard_gates"]["source_coverage"])

    def test_unknown_or_missing_boolean_is_rejected(self):
        metrics = self.good_metrics()
        metrics["premises_consistent"] = "SAT"
        with self.assertRaises(ValueError):
            evaluate_candidate(metrics)

    def test_non_finite_compute_time_is_rejected(self):
        metrics = self.good_metrics()
        metrics["compute_seconds"] = float("inf")
        with self.assertRaises(ValueError):
            evaluate_candidate(metrics)

    def test_unknown_threshold_key_is_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_candidate(self.good_metrics(), {"trust": 1.0})

    def test_evidence_coverage_is_a_separate_hard_gate(self):
        metrics = self.good_metrics()
        metrics["evidence_coverage"] = 0.50
        result = evaluate_candidate(metrics)
        self.assertEqual(result["status"], "BLOCKED_BY_HARD_GATE")
        self.assertFalse(result["hard_gates"]["evidence_coverage"])

    def test_false_accept_rate_blocks_candidate_even_when_other_metrics_are_high(self):
        metrics = self.good_metrics()
        metrics["false_accept_rate"] = 0.10
        result = evaluate_candidate(metrics)
        self.assertEqual(result["status"], "BLOCKED_BY_HARD_GATE")
        self.assertFalse(result["hard_gates"]["false_accept_rate"])

    def test_counterexample_escape_rate_blocks_candidate(self):
        metrics = self.good_metrics()
        metrics["counterexample_escape_rate"] = 0.05
        result = evaluate_candidate(metrics)
        self.assertEqual(result["status"], "BLOCKED_BY_HARD_GATE")
        self.assertFalse(result["hard_gates"]["counterexample_escape_rate"])

    def test_new_error_rates_are_required_and_never_default_to_zero(self):
        metrics = self.good_metrics()
        del metrics["false_accept_rate"]
        with self.assertRaises(ValueError):
            evaluate_candidate(metrics)

    def test_thresholds_are_recorded_as_uncalibrated(self):
        result = evaluate_candidate(self.good_metrics())
        self.assertEqual(result["threshold_status"], "INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED")
        self.assertEqual(result["thresholds"], DEFAULT_THRESHOLDS)


if __name__ == "__main__":
    unittest.main()
