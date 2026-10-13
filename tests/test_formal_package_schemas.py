from __future__ import annotations

import unittest
from pathlib import Path
import json

from formal_reasoning.formalization_queue import queue_candidate_for_formalization
from formal_reasoning.evaluation import load_evaluation_policy

try:
    import jsonschema
except ImportError as exc:
    raise unittest.SkipTest("optional dependency jsonschema is not installed") from exc

ROOT = Path(__file__).resolve().parents[1]


def load_schema(name):
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def valid_package():
    return {
        "schema_version": "wanga-logic-package/1.0",
        "package_id": "LOGIC-PACK-001",
        "version": "0.1.0",
        "status": "INTERNAL_CANDIDATE_NOT_RELEASED",
        "formal_semantics": {
            "logic_fragment": "propositional_boolean",
            "variables": {"p": "Bool"},
            "supported_operators": ["not", "and", "or", "implies"]
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
        "release_approval": None
    }


class LogicJsonSchemaTests(unittest.TestCase):
    def test_schemas_are_valid_draft_2020_12(self):
        package_schema = load_schema("logic-package-contract-v1.schema.json")
        formal_schema = load_schema("typed-formal-fragment-v1.schema.json")
        jsonschema.Draft202012Validator.check_schema(package_schema)
        jsonschema.Draft202012Validator.check_schema(formal_schema)

    def test_candidate_evaluation_policy_schema_and_config_match(self):
        policy_schema = load_schema("candidate-evaluation-policy-v1.schema.json")
        jsonschema.Draft202012Validator.check_schema(policy_schema)
        policy_file = ROOT / "formal_reasoning/config/evaluation_policy.json"
        policy = json.loads(policy_file.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(policy_schema).validate(policy)
        thresholds, status = load_evaluation_policy()
        self.assertEqual(status, "INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED")
        self.assertIn("min_evidence_coverage", thresholds)
        self.assertIn("max_false_accept_rate", thresholds)
        self.assertIn("max_counterexample_escape_rate", thresholds)

    def test_internal_candidate_contract_is_valid(self):
        validator = jsonschema.Draft202012Validator(load_schema("logic-package-contract-v1.schema.json"))
        validator.validate(valid_package())

    def test_verified_cannot_pass_without_independent_approval(self):
        package = valid_package()
        package["status"] = "VERIFIED"
        package["semantic_status"] = "VERIFIED_WITHIN_ENCODED_FRAGMENT"
        validator = jsonschema.Draft202012Validator(load_schema("logic-package-contract-v1.schema.json"))
        self.assertTrue(list(validator.iter_errors(package)))

    def test_formal_fragment_schema_accepts_source_backed_premise(self):
        spec = {
            "schema_version": "wanga-formal-fragment/1.0",
            "variables": {"x": "Int"},
            "premises": [{"id": "P1", "expr": {"op": "gt", "args": [{"var": "x"}, {"const": 0}]},
                          "source_refs": ["SRC-001"], "assumption": False}],
            "conclusion": {"op": "gt", "args": [{"var": "x"}, {"const": -1}]}
        }
        validator = jsonschema.Draft202012Validator(load_schema("typed-formal-fragment-v1.schema.json"))
        validator.validate(spec)

    def test_formalization_queue_item_matches_schema(self):
        candidate = {
            "package_id": "LT-0123456789abcdef",
            "version": "0.1",
            "member_articles": [{"id": "logic-a", "definition": "A test definition.", "source_refs": ["SRC-1"]}],
            "sources": [{"id": "SRC-1"}]
        }
        item = queue_candidate_for_formalization(candidate)
        schema = json.loads((ROOT / "schemas/logic-formalization-queue-item-v1.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(item)
        self.assertEqual(item["solver_execution_status"], "NOT_RUN_NO_FORMAL_AST")
        self.assertFalse(item["automatic_semantic_conversion"])

    def test_formal_fragment_schema_rejects_unscoped_premise(self):
        spec = {
            "schema_version": "wanga-formal-fragment/1.0",
            "variables": {"x": "Int"},
            "premises": [{"id": "P1", "expr": {"var": "x"}, "source_refs": [], "assumption": False}],
            "conclusion": {"var": "x"}
        }
        validator = jsonschema.Draft202012Validator(load_schema("typed-formal-fragment-v1.schema.json"))
        self.assertTrue(list(validator.iter_errors(spec)))


if __name__ == "__main__":
    unittest.main()
