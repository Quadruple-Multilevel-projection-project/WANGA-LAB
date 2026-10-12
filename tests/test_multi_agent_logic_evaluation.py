from __future__ import annotations
import unittest
from scripts.evaluate_logic_agent_bundle import AGENTS, run_evaluation


class MultiAgentLogicEvaluationTests(unittest.TestCase):
    def test_six_deterministic_agent_roles_are_exercised(self):
        report = run_evaluation()
        self.assertEqual(report["agent_count"], 6)
        self.assertEqual(report["passed_agents"], 6, report["agent_results"])
        self.assertEqual(report["failed_agents"], 0)

    def test_no_role_claims_neural_model_execution(self):
        report = run_evaluation()
        self.assertIn("not separate neural models", report["model_claim_boundary"])

    def test_each_agent_has_checkable_result(self):
        for name, execute in AGENTS:
            result = execute()
            self.assertTrue(result.get("checks"), name)
            self.assertTrue(result.get("passed"), {name: result})

    def test_recursive_composition_does_not_claim_semantic_equivalence(self):
        report = run_evaluation()
        fractal = next(a for a in report["agent_results"] if a["agent"] == "recursive-fractal-composer")
        self.assertEqual(fractal["result"]["semantic_equivalence"], "NOT_ESTABLISHED")

    def test_derived_claims_remain_not_verified(self):
        report = run_evaluation()
        evidence = next(a for a in report["agent_results"] if a["agent"] == "evidence-gatekeeper")
        self.assertTrue(evidence["result"]["checks"]["derived_claim_not_verified"])
        builder = next(a for a in report["agent_results"] if a["agent"] == "lnl-model-builder-runtime")
        self.assertTrue(builder["result"]["checks"]["derived_claim_not_verified"])


if __name__ == "__main__":
    unittest.main()
