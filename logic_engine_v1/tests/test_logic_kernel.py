from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
REPO_ROOT = PROJECT.parent
sys.path.insert(0, str(PROJECT))

from logic_kernel import (  # noqa: E402
    combinatorial_counts,
    compare_thresholds,
    gate_action,
    load_corpus_context,
    run_bundle,
    sample_bundle,
    validate_corpus,
)


class CombinatoricsTests(unittest.TestCase):
    def test_exact_counts(self):
        result = combinatorial_counts()
        self.assertEqual(result["letters"], 22)
        self.assertEqual(result["undirected_pairs"], 231)
        self.assertEqual(result["directed_distinct_pairs"], 462)
        self.assertEqual(result["unordered_distinct_triples"], 1540)
        self.assertEqual(result["ordered_distinct_triples"], 9240)
        self.assertEqual(result["ordered_triples_with_repetition"], 10648)

    def test_requires_exactly_22_unique_symbols(self):
        with self.assertRaises(ValueError):
            combinatorial_counts(["A", "A"])


class EvidenceAndRuleTests(unittest.TestCase):
    def test_sample_derives_candidate_but_never_marks_it_verified(self):
        result = run_bundle(sample_bundle())
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["summary"]["eligible_input_claims"], 3)
        self.assertEqual(result["summary"]["unsupported_or_ineligible_claims"], 1)
        derived = [x for x in result["derived_claims"] if x["atom"]["object"] == "typo_fix"]
        self.assertEqual(len(derived), 1)
        self.assertEqual(derived[0]["status"], "DERIVED_NOT_VERIFIED")
        unsupported = next(x for x in result["input_claims"] if x["claim_id"] == "C-UNSUPPORTED-PUBLISH")
        self.assertEqual(unsupported["engine_status"], "UNSUPPORTED_NO_EVIDENCE")

    def test_missing_evidence_reference_is_not_eligible(self):
        bundle = sample_bundle()
        bundle["claims"][0]["evidence_refs"] = ["MISSING-ID"]
        result = run_bundle(bundle)
        record = next(x for x in result["input_claims"] if x["claim_id"] == "C-REQUEST")
        self.assertEqual(record["engine_status"], "MISSING_EVIDENCE_REFERENCE")
        self.assertFalse(any(x["atom"]["object"] == "typo_fix" for x in result["derived_claims"]))

    def test_hypothesis_does_not_seed_rules_even_with_reference(self):
        bundle = sample_bundle()
        bundle["claims"][0]["epistemic_status"] = "HYPOTHESIS"
        result = run_bundle(bundle)
        record = next(x for x in result["input_claims"] if x["claim_id"] == "C-REQUEST")
        self.assertEqual(record["engine_status"], "NOT_ELIGIBLE_EPISTEMIC_STATUS")
        self.assertFalse(any(x["atom"]["object"] == "typo_fix" for x in result["derived_claims"]))

    def test_opposite_polarity_is_reported_as_contradiction(self):
        bundle = sample_bundle()
        bundle["claims"].append({
            "id": "C-CONTRADICTS-REQUEST",
            "atom": {"subject": "request", "predicate": "action", "object": "typo_fix", "polarity": False},
            "epistemic_status": "TEST_FIXTURE",
            "evidence_refs": ["E-REQUEST"],
        })
        result = run_bundle(bundle)
        self.assertEqual(result["status"], "REVIEW")
        self.assertGreaterEqual(len(result["contradictions"]), 1)
        self.assertIn("CONTRADICTED_REQUIRES_REVIEW", {x["status"] for x in result["facts"]})

    def test_duplicate_ids_are_rejected(self):
        bundle = sample_bundle()
        bundle["claims"].append(copy.deepcopy(bundle["claims"][0]))
        with self.assertRaises(ValueError):
            run_bundle(bundle)

    def test_inactive_rule_is_skipped(self):
        bundle = sample_bundle()
        for rule in bundle["rules"]:
            rule["status"] = "DISABLED"
        result = run_bundle(bundle)
        self.assertEqual(result["summary"]["rule_firings"], 0)
        self.assertEqual(len(result["skipped_rules"]), len(bundle["rules"]))


class ActionGateTests(unittest.TestCase):
    def allowed_request(self):
        return {
            "action": "typo_fix",
            "target": "approved-page-1",
            "allowed_actions": ["typo_fix"],
            "allowed_targets": ["approved-page-1"],
            "permission_granted": True,
            "publish": False,
            "publish_permission_granted": False,
            "evidence_complete": True,
        }

    def test_allowed_in_scope_action(self):
        self.assertEqual(gate_action(self.allowed_request())["decision"], "ALLOW_WITHIN_DECLARED_SCOPE")

    def test_action_outside_scope_is_denied(self):
        request = self.allowed_request()
        request["action"] = "change_price"
        self.assertEqual(gate_action(request)["decision"], "DENY")

    def test_publish_requires_explicit_publish_permission(self):
        request = self.allowed_request()
        request["publish"] = True
        self.assertEqual(gate_action(request)["decision"], "DENY")
        request["publish_permission_granted"] = True
        self.assertEqual(gate_action(request)["decision"], "ALLOW_WITHIN_DECLARED_SCOPE")

    def test_incomplete_evidence_routes_to_review(self):
        request = self.allowed_request()
        request["evidence_complete"] = False
        self.assertEqual(gate_action(request)["decision"], "REVIEW")


class DriftTests(unittest.TestCase):
    def test_same_score_can_change_decision_when_threshold_changes(self):
        result = compare_thresholds(0.75, 0.80, 0.60)
        self.assertTrue(result["decision_changed"])
        self.assertEqual(result["old_decision"], "REJECT")
        self.assertEqual(result["new_decision"], "ACCEPT")
        self.assertEqual(result["score"], 0.75)

    def test_non_finite_numbers_rejected(self):
        with self.assertRaises(ValueError):
            compare_thresholds(float("nan"), 0.8, 0.6)


class SourceGroundedSemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.semantic_matrix_path = PROJECT / "semantic_tests" / "semantic_test_matrix.json"
        cls.matrix = json.loads(cls.semantic_matrix_path.read_text(encoding="utf-8"))

    def test_semantic_test_matrix_has_unique_ids_and_source_bounds(self):
        cases = self.matrix["cases"]
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), len(set(ids)))
        for case in cases:
            self.assertTrue(case["assertion"].strip())
            self.assertTrue(case["scope_limit"].strip())
            self.assertTrue(case["automated_test"].startswith("test_"))
        self.assertTrue(self.matrix["source_claim_boundary"])

    def test_selected_sefer_yetzirah_presentation_is_edition_scoped(self):
        source = next(s for s in self.matrix["sources"] if s["id"] == "SRC-SY-GRA-2-4")
        self.assertEqual(source["reference_status"], "SOURCE_TEXT_LOCATED")
        self.assertIn("Sefer_Yetzirah_Gra_Version.2.4", source["uri"])
        self.assertIn("231", source["excerpt"])
        self.assertIn("forward and back", source["excerpt"])
        self.assertIn("edition", source["scope_limit"].lower())

    def test_221_231_scholarship_reference_stays_review_required(self):
        source = next(s for s in self.matrix["sources"] if s["id"] == "SRC-VARIANT-221-231")
        self.assertEqual(source["reference_status"], "BIBLIOGRAPHIC_REFERENCE_REQUIRES_FULL_TEXT_REVIEW")
        self.assertNotEqual(source["reference_status"], "VERIFIED")
        self.assertIn("not", source["scope_limit"].lower())

    def test_corpus_context_injects_only_structural_facts_requested_by_rules(self):
        context = load_corpus_context(REPO_ROOT)
        self.assertEqual(context["status"], "LOADED")
        self.assertEqual(context["counts"]["letters"], 22)
        self.assertEqual(context["counts"]["undirected_gates"], 231)
        self.assertEqual(context["counts"]["directed_transitions"], 462)
        self.assertEqual(context["counts"]["unordered_triples"], 1540)
        bundle = {
            "evidence": [],
            "claims": [],
            "rules": [{
                "id": "R-STRUCTURAL-GATE-001",
                "status": "ACTIVE_SPECIFIED",
                "description": "Structural count test only; no semantic gate meaning is inferred.",
                "antecedents": [{
                    "subject": "gate:GATE-001",
                    "predicate": "corpus_connects_unordered",
                    "object": "א|ב",
                }],
                "consequent": {
                    "subject": "test",
                    "predicate": "corpus_loaded_gate",
                    "object": "GATE-001",
                },
                "source_refs": ["repo://research/data/LETTER_GATE_MAP_231_V1.json#GATE-001"],
            }],
        }
        result = run_bundle(bundle, corpus_context=context)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(len(result["derived_claims"]), 1)
        self.assertEqual(result["derived_claims"][0]["status"], "DERIVED_NOT_VERIFIED")
        self.assertEqual(result["corpus_context"]["used_structural_facts"], 1)
        self.assertIn("research/data/LETTER_GATE_MAP_231_V1.json",
                      result["trace"][0]["premise_corpus_files"][0])

    def test_source_linked_fixture_does_not_upgrade_conclusion_to_verified(self):
        source = next(s for s in self.matrix["sources"] if s["id"] == "SRC-SY-GRA-2-4")
        bundle = {
            "evidence": [{
                "id": source["id"],
                "source_uri": source["uri"],
                "source_version": source["source_version"],
                "location": source["locator"],
                "status": "SOURCE_TEXT_LOCATED",
                "note": source["scope_limit"],
            }],
            "claims": [{
                "id": "C-SOURCE-EDITION-SCOPE",
                "atom": {
                    "subject": "selected Sefer Yetzirah Gra 2:4 presentation",
                    "predicate": "reports",
                    "object": "22 letters, 231 gates, forward/back movement",
                },
                "epistemic_status": "TEST_FIXTURE",
                "evidence_refs": [source["id"]],
            }],
            "rules": [{
                "id": "R-PRESERVE-EDITION-BOUNDARY",
                "status": "ACTIVE_SPECIFIED",
                "description": "A cited page is a source for an edition-scoped report, not every recension.",
                "antecedents": [{
                    "subject": "selected Sefer Yetzirah Gra 2:4 presentation",
                    "predicate": "reports",
                    "object": "22 letters, 231 gates, forward/back movement",
                }],
                "consequent": {
                    "subject": "claim C-SOURCE-EDITION-SCOPE",
                    "predicate": "scope",
                    "object": "edition_specific_not_universal",
                },
                "source_refs": [source["uri"]],
            }],
        }
        result = run_bundle(bundle)
        self.assertEqual(result["status"], "COMPLETED")
        derived = result["derived_claims"]
        self.assertEqual(len(derived), 1)
        self.assertEqual(derived[0]["status"], "DERIVED_NOT_VERIFIED")
        self.assertEqual(derived[0]["status"], "DERIVED_NOT_VERIFIED")
        self.assertNotEqual(derived[0]["status"], "VERIFIED")

    def test_all_gate_semantics_remain_unassigned_in_registry(self):
        gate_map_path = REPO_ROOT / "research" / "data" / "LETTER_GATE_MAP_231_V1.json"
        gate_map = json.loads(gate_map_path.read_text(encoding="utf-8"))
        self.assertTrue(all(
            gate.get("source_semantics") == "UNASSIGNED"
            for gate in gate_map["undirected_gates"]
        ))


class CorpusIntegrationTests(unittest.TestCase):
    def test_repository_corpus_invariants(self):
        result = validate_corpus(REPO_ROOT)
        self.assertEqual(result["status"], "PASS", json.dumps(result, ensure_ascii=False))
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(result["actual_page_records"], 1000)
        self.assertEqual(result["gate_count"], 231)
        self.assertEqual(result["directed_transition_count"], 462)
        self.assertEqual(result["triple_count"], 1540)

    def test_cli_demo_is_valid_json(self):
        completed = subprocess.run(
            [sys.executable, str(PROJECT / "logic_kernel.py"), "demo", "--compact"],
            check=True, capture_output=True, text=True, cwd=REPO_ROOT,
        )
        decoded = json.loads(completed.stdout)
        self.assertEqual(decoded["engine_type"], "DETERMINISTIC_SYMBOLIC_PROTOTYPE_NOT_GENERAL_AI")
        self.assertEqual(decoded["summary"]["rule_firings"], 2)
        self.assertEqual(decoded["corpus_context"]["status"], "LOADED")
        self.assertEqual(decoded["corpus_context"]["used_structural_facts"], 1)
        self.assertEqual(decoded["action_gate_result"]["decision"], "ALLOW_WITHIN_DECLARED_SCOPE")
        self.assertTrue(decoded["threshold_comparison"]["decision_changed"])
        self.assertEqual(decoded["combinatorial_counts"]["unordered_distinct_triples"], 1540)
        self.assertEqual(decoded["corpus_context"]["registered_letters"], 22)
        self.assertEqual(decoded["corpus_context"]["semantic_status"], "STRUCTURAL_COMBINATORICS_ONLY")


if __name__ == "__main__":
    unittest.main()
