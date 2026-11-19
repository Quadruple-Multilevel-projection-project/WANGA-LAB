from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-blueprint-v1.schema.json"
BLUEPRINT_DIR = ROOT / "agent_blueprints"


class AgentBlueprintSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())
        cls.blueprints = [
            (path, json.loads(path.read_text(encoding="utf-8")))
            for path in sorted(BLUEPRINT_DIR.rglob("*.json"))
        ]

    def test_schema_definition_is_valid(self):
        Draft202012Validator.check_schema(self.schema)

    def test_all_committed_blueprints_validate(self):
        self.assertGreaterEqual(len(self.blueprints), 1)
        for path, blueprint in self.blueprints:
            with self.subTest(path=str(path.relative_to(ROOT))):
                errors = list(self.validator.iter_errors(blueprint))
                self.assertEqual(errors, [], "; ".join(error.message for error in errors))

    def test_runtime_blueprint_requires_audit_and_rollback(self):
        path, blueprint = next(
            (path, item) for path, item in self.blueprints
            if item.get("id") == "agent-runtime-verifier"
        )
        candidate = copy.deepcopy(blueprint)
        candidate.pop("rollback")
        errors = list(self.validator.iter_errors(candidate))
        self.assertTrue(errors, f"{path} unexpectedly accepted a missing rollback contract")

    def test_tested_or_active_runtime_requires_evidence(self):
        path, blueprint = next(
            (path, item) for path, item in self.blueprints
            if item.get("id") == "agent-runtime-verifier"
        )
        candidate = copy.deepcopy(blueprint)
        candidate["status"] = "active"
        runtime = candidate["runtime"]
        runtime.update({
            "runtime_status": "ACTIVE",
            "backend_configuration": "containerd@1.7.0",
            "environment": "staging",
            "network_egress_policy_ref": "deny-all-policy-v1",
            "invocation_log_refs": [],
            "isolation_evidence_refs": [],
            "acceptance_test_refs": []
        })
        errors = list(self.validator.iter_errors(candidate))
        self.assertTrue(errors, f"{path} unexpectedly accepted active status without execution evidence")

    def test_current_agent_blueprints_are_not_deployed(self):
        for path, blueprint in self.blueprints:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertEqual(blueprint["status"], "draft")
                self.assertEqual(blueprint["runtime"]["runtime_status"], "NOT_CONFIGURED")
                self.assertEqual(blueprint["runtime"]["backend_configuration"], "NOT_CONFIGURED")
                self.assertEqual(blueprint["runtime"]["invocation_log_refs"], [])


if __name__ == "__main__":
    unittest.main()
