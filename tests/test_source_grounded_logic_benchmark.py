from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_source_grounded_logic_benchmark import audit_manifest


CASE_SCHEMA_PATH = ROOT / "schemas/source-grounded-logic-benchmark-case-v1.schema.json"
MANIFEST_SCHEMA_PATH = ROOT / "schemas/source-grounded-logic-benchmark-manifest-v1.schema.json"


def source_fixture():
    return {"sources": [{"id": "SRC-TEST", "type": "TEST_FIXTURE", "uri": "fixture://source/1"}]}


def empty_manifest():
    return {
        "schema_version": "wanga-source-grounded-benchmark-manifest/1.0",
        "dataset_id": "TEST-DATASET",
        "dataset_version": "0.0.1",
        "status": "BLOCKED_EMPTY_WAITING_REVIEWED_CASES",
        "minimum_risk_cases": 30,
        "required_risk_case_types": ["NEGATIVE", "BOUNDARY", "COUNTEREXAMPLE"],
        "required_splits": ["TRAIN", "VALIDATION", "HOLDOUT"],
        "minimum_source_classes": 3,
        "source_registry": "logic_wiki/data/articles.json",
        "case_schema": "schemas/source-grounded-logic-benchmark-case-v1.schema.json",
        "cases": [],
    }


def reviewed_case(case_id="CASE-TEST-001", case_type="POSITIVE", split="TRAIN", expected="ENTAILED_WITHIN_ENCODING"):
    return {
        "schema_version": "wanga-source-grounded-benchmark-case/1.0",
        "case_id": case_id,
        "case_type": case_type,
        "split": split,
        "claim_text": "TEST_FIXTURE only: P and P implies Q entail Q.",
        "source_refs": ["SRC-TEST"],
        "source_spans": [{
            "source_ref": "SRC-TEST",
            "locator": "fixture://source/1#span-1",
            "span_sha256": "a" * 64,
            "permission_scope": "TEST_FIXTURE_NOT_ELIGIBLE_FOR_READINESS",
        }],
        "formalization_status": "REVIEWED_FORMALIZATION",
        "semantic_status": "NOT_YET_VERIFIED",
        "execute_in_benchmark": True,
        "formal_spec": {
            "schema_version": "wanga-formal-claim/1.0",
            "claim_id": case_id,
            "variables": ["P", "Q"],
            "premises": ["P -> Q", "P"],
            "conclusion": "Q",
            "source_refs": ["SRC-TEST"],
            "epistemic_status": "TEST_FIXTURE",
        },
        "expected_status": expected,
        "review": {
            "reviewer_id": "test-reviewer",
            "reviewed_at": "2026-10-12T00:00:00Z",
            "source_mapping_decision": "ACCEPTED_FOR_BENCHMARK",
            "formalization_decision": "ACCEPTED_WITHIN_PROPOSITIONAL_FRAGMENT",
            "notes": "TEST_FIXTURE; not a real source-grounded case.",
        },
    }


class SourceGroundedBenchmarkIntakeTests(unittest.TestCase):
    def setUp(self):
        self.manifest = empty_manifest()
        self.catalog = source_fixture()

    def test_empty_manifest_is_blocked_and_rates_are_null_not_zero(self):
        report = audit_manifest(
            self.manifest,
            CASE_SCHEMA_PATH,
            MANIFEST_SCHEMA_PATH,
            self.catalog,
            root=ROOT,
        )
        self.assertEqual(report["status"], "BLOCKED_INSUFFICIENT_REVIEWED_CASES")
        self.assertEqual(report["case_count"], 0)
        self.assertEqual(report["reviewed_executable_case_count"], 0)
        self.assertIsNone(report["metrics"]["false_accept_rate"])
        self.assertIsNone(report["metrics"]["counterexample_escape_rate"])
        self.assertEqual(report["semantic_status"], "NOT_YET_VERIFIED")

    def test_readiness_reports_metric_gates_as_blocked_when_no_eligible_cases_exist(self):
        report = audit_manifest(
            self.manifest,
            CASE_SCHEMA_PATH,
            MANIFEST_SCHEMA_PATH,
            self.catalog,
            root=ROOT,
        )
        self.assertFalse(report["readiness_requirements"]["metric_gates_pass"])
        self.assertTrue(all(value is False for value in report["metric_gates"].values()))
        self.assertEqual(report["threshold_status"], "INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED")

    def test_case_and_manifest_json_schemas_are_valid(self):
        try:
            import jsonschema
        except ImportError as exc:
            self.skipTest(f"jsonschema unavailable: {exc}")
        case_schema = json.loads(CASE_SCHEMA_PATH.read_text(encoding="utf-8"))
        manifest_schema = json.loads(MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(case_schema)
        jsonschema.Draft202012Validator.check_schema(manifest_schema)
        jsonschema.Draft202012Validator(manifest_schema).validate(self.manifest)

    def test_reviewed_fixture_executes_but_does_not_count_toward_readiness(self):
        self.manifest["cases"] = [reviewed_case()]
        report = audit_manifest(
            self.manifest,
            CASE_SCHEMA_PATH,
            MANIFEST_SCHEMA_PATH,
            self.catalog,
            root=ROOT,
        )
        self.assertEqual(report["reviewed_executable_case_count"], 1)
        self.assertEqual(report["passed_cases"], 1)
        self.assertEqual(report["status"], "BLOCKED_INSUFFICIENT_REVIEWED_CASES")
        self.assertEqual(report["eligible_reviewed_case_count"], 0)
        self.assertEqual(report["case_results"][0]["status"], "PASS")

    def test_unformalized_case_is_not_sent_to_solver(self):
        case = reviewed_case()
        case["formalization_status"] = "NOT_FORMALIZED"
        case["execute_in_benchmark"] = False
        for key in ("formal_spec", "expected_status", "review"):
            case.pop(key)
        self.manifest["cases"] = [case]
        report = audit_manifest(
            self.manifest,
            CASE_SCHEMA_PATH,
            MANIFEST_SCHEMA_PATH,
            self.catalog,
            root=ROOT,
        )
        self.assertEqual(report["reviewed_executable_case_count"], 0)
        self.assertEqual(report["status"], "BLOCKED_INSUFFICIENT_REVIEWED_CASES")

    def test_unknown_source_is_rejected(self):
        case = reviewed_case()
        case["source_refs"] = ["SRC-MISSING"]
        self.manifest["cases"] = [case]
        report = audit_manifest(
            self.manifest,
            CASE_SCHEMA_PATH,
            MANIFEST_SCHEMA_PATH,
            self.catalog,
            root=ROOT,
        )
        self.assertEqual(report["status"], "INVALID_CASES")
        self.assertIn("unknown source refs", " ".join(report["case_errors"][0]["errors"]))

    def test_risk_case_cannot_expect_successful_entailment(self):
        self.manifest["cases"] = [reviewed_case(case_type="COUNTEREXAMPLE", expected="ENTAILED_WITHIN_ENCODING")]
        report = audit_manifest(
            self.manifest,
            CASE_SCHEMA_PATH,
            MANIFEST_SCHEMA_PATH,
            self.catalog,
            root=ROOT,
        )
        self.assertEqual(report["status"], "INVALID_CASES")
        self.assertIn("risk-case expected status", " ".join(report["case_errors"][0]["errors"]))


if __name__ == "__main__":
    unittest.main()
