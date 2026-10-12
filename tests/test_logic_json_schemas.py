from __future__ import annotations

import unittest
from pathlib import Path
import json

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
        formal_schema = load_schema("formal-fragment-v1.schema.json")
        jsonschema.Draft202012Validator.check_schema(package_schema)
        jsonschema.Draft202012Validator.check_schema(formal_schema)

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
        validator = jsonschema.Draft202012Validator(load_schema("formal-fragment-v1.schema.json"))
        validator.validate(spec)

    def test_formal_fragment_schema_rejects_unscoped_premise(self):
        spec = {
            "schema_version": "wanga-formal-fragment/1.0",
            "variables": {"x": "Int"},
            "premises": [{"id": "P1", "expr": {"var": "x"}, "source_refs": [], "assumption": False}],
            "conclusion": {"var": "x"}
        }
        validator = jsonschema.Draft202012Validator(load_schema("formal-fragment-v1.schema.json"))
        self.assertTrue(list(validator.iter_errors(spec)))


if __name__ == "__main__":
    unittest.main()
