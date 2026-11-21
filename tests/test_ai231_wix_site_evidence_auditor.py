import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-blueprint-v1.schema.json"
BLUEPRINT_PATH = ROOT / "agent_blueprints" / "ai231-wix-site-evidence-auditor.json"


class WixSiteEvidenceAuditorBlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.blueprint = json.loads(BLUEPRINT_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_blueprint_passes_canonical_schema(self):
        self.validator.validate(self.blueprint)

    def test_agent_is_draft_and_read_only(self):
        self.assertEqual(self.blueprint["status"], "draft")
        self.assertTrue(self.blueprint["runtime"]["isolation_required"])
        self.assertFalse(self.blueprint["runtime"]["network_egress"])
        self.assertEqual(self.blueprint["runtime"]["credential_refs"], [])
        permissions = set(self.blueprint["tool_permissions"])
        self.assertNotIn("publish_wix_site", permissions)
        self.assertNotIn("write_wix_site", permissions)
        self.assertNotIn("modify_production_site", permissions)

    def test_dynamic_routes_are_unresolved_until_verified(self):
        text = " ".join(
            test["description"] + " " + test["expected"]
            for test in self.blueprint["acceptance_tests"]
        ).lower()
        self.assertIn("unresolved_dynamic_route", text)
        self.assertIn("wix blog", text)

    def test_production_write_requests_are_blocked(self):
        text = " ".join(
            test["description"] + " " + test["expected"]
            for test in self.blueprint["acceptance_tests"]
        ).lower()
        self.assertIn("blocked", text)
        self.assertIn("production wix", text)

    def test_rollback_is_explicit(self):
        failure = self.blueprint["failure_behavior"].lower()
        self.assertIn("rollback", failure)
        self.assertIn("discard", failure)
        self.assertIn("revert", failure)

    def test_schema_rejects_network_egress(self):
        unsafe = copy.deepcopy(self.blueprint)
        unsafe["runtime"]["network_egress"] = True
        self.assertTrue(list(self.validator.iter_errors(unsafe)))


    def test_root_relative_links_are_normalized_before_missing_link_classification(self):
        text = " ".join(
            boundary for boundary in self.blueprint["boundaries"]
        ).lower()
        acceptance = " ".join(
            test["description"] + " " + test["expected"]
            for test in self.blueprint["acceptance_tests"]
        ).lower()
        self.assertIn("root-relative", text)
        self.assertIn("normalize", text)
        self.assertIn("root-relative", acceptance)
        self.assertIn("unresolved", acceptance)


if __name__ == "__main__":
    unittest.main()
