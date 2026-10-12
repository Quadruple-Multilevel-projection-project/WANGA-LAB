from __future__ import annotations

import unittest

from formal_reasoning.package_contract import validate_package_contract


def package_template():
    return {
        "schema_version": "wanga-logic-package/1.0",
        "package_id": "LOGIC-PACK-001",
        "version": "0.1.0",
        "status": "INTERNAL_CANDIDATE_NOT_RELEASED",
        "formal_semantics": {
            "logic_fragment": "propositional_boolean",
            "variables": {"p": "Bool"},
            "supported_operators": ["not", "and", "or", "implies"],
        },
        "premises": [
            {"id": "P1", "expr": {"var": "p"}, "source_refs": ["SRC-001"], "assumption": False}
        ],
        "conclusion": {"var": "p"},
        "source_refs": ["SRC-001"],
        "composition_rule": None,
        "tests": ["formal-case-F001"],
        "known_limits": ["Does not formalize arbitrary natural language."],
        "semantic_status": "NOT_YET_VERIFIED",
        "release_approval": None,
    }


class LogicPackageContractTests(unittest.TestCase):
    def test_internal_candidate_validates_but_is_not_released(self):
        result = validate_package_contract(package_template())
        self.assertEqual(result["status"], "VALID_CONTRACT")
        self.assertFalse(result["release_allowed"])

    def test_premise_without_source_must_be_explicit_assumption(self):
        package = package_template()
        package["premises"][0]["source_refs"] = []
        result = validate_package_contract(package)
        self.assertEqual(result["status"], "INVALID")
        self.assertTrue(any("explicit assumption=true" in error for error in result["errors"]))

    def test_candidate_cannot_promote_itself_to_verified(self):
        package = package_template()
        package["status"] = "VERIFIED"
        package["semantic_status"] = "VERIFIED_WITHIN_ENCODED_FRAGMENT"
        result = validate_package_contract(package)
        self.assertEqual(result["status"], "INVALID")
        self.assertFalse(result["release_allowed"])
        self.assertTrue(any("independent release_approval" in error for error in result["errors"]))

    def test_verified_requires_complete_independent_approval(self):
        package = package_template()
        package["status"] = "VERIFIED"
        package["semantic_status"] = "VERIFIED_WITHIN_ENCODED_FRAGMENT"
        package["release_approval"] = {
            "reviewer_id": "reviewer-1",
            "approved_at": "2026-10-12T00:00:00Z",
            "benchmark_report_sha256": "a" * 64,
            "evidence_refs": ["SRC-001"],
            "independent_review_pass": True,
        }
        result = validate_package_contract(package)
        self.assertEqual(result["status"], "VALID_CONTRACT")
        self.assertTrue(result["release_allowed"])

    def test_internal_candidate_cannot_smuggle_release_approval(self):
        package = package_template()
        package["release_approval"] = {"reviewer_id": "untrusted"}
        result = validate_package_contract(package)
        self.assertEqual(result["status"], "INVALID")


if __name__ == "__main__":
    unittest.main()
