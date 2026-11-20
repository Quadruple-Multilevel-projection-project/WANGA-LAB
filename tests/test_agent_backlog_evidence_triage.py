import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

from business_brain.agents.backlog_evidence_triage import triage_issues

ROOT = Path(__file__).resolve().parents[1]


class AgentBlueprintSchemaTests(unittest.TestCase):
    def test_existing_and_new_blueprints_match_canonical_schema(self):
        schema = json.loads((ROOT / "schemas/agent-blueprint-v1.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        paths = [
            ROOT / "agent_blueprints/agent-runtime-verifier.json",
            ROOT / "agent_blueprints/agent-blueprint-architect.json",
            ROOT / "agent_blueprints/agent-backlog-evidence-triage.json",
        ]
        for path in paths:
            with self.subTest(blueprint=path.name):
                blueprint = json.loads(path.read_text(encoding="utf-8"))
                validator.validate(blueprint)

    def test_new_agent_is_draft_and_has_no_network_egress(self):
        blueprint = json.loads((ROOT / "agent_blueprints/agent-backlog-evidence-triage.json").read_text(encoding="utf-8"))
        self.assertEqual(blueprint["status"], "draft")
        self.assertTrue(blueprint["runtime"]["isolation_required"])
        self.assertFalse(blueprint["runtime"]["network_egress"])
        self.assertEqual(blueprint["runtime"]["credential_refs"], [])


class BacklogEvidenceTriageTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = json.loads((ROOT / "examples/backlog-triage-snapshot-2026-11-20.json").read_text(encoding="utf-8"))

    def test_stale_and_recent_issues_are_separated(self):
        report = triage_issues(self.snapshot, as_of="2026-11-20T09:06:41+02:00")
        self.assertEqual(report["stale_open_issue_numbers"], ["90", "91", "126"])
        self.assertNotIn("148", report["stale_open_issue_numbers"])
        self.assertNotIn("149", report["stale_open_issue_numbers"])

    def test_paid_pilot_issues_are_flagged_as_candidates_not_merged(self):
        report = triage_issues(self.snapshot, as_of="2026-11-20T09:06:41+02:00")
        pairs = [item["issue_numbers"] for item in report["possible_duplicate_pairs"]]
        self.assertIn(["148", "149"], pairs)
        pair = next(item for item in report["possible_duplicate_pairs"] if item["issue_numbers"] == ["148", "149"])
        self.assertTrue(pair["review_required"])
        self.assertFalse(pair["automatic_merge"])
        self.assertGreaterEqual(len(pair["shared_tokens"]), 3)

    def test_missing_priority_and_unassigned_items_are_reported(self):
        report = triage_issues(self.snapshot, as_of="2026-11-20T09:06:41+02:00")
        self.assertEqual(set(report["missing_priority_issue_numbers"]), {"90", "91", "126", "148", "149"})
        self.assertEqual(set(report["unassigned_open_issue_numbers"]), {"90", "91", "126", "148", "149"})

    def test_input_snapshot_is_not_mutated(self):
        snapshot = deepcopy(self.snapshot)
        triage_issues(snapshot, as_of="2026-11-20T09:06:41+02:00")
        self.assertEqual(snapshot, self.snapshot)

    def test_invalid_timestamp_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "invalid ISO 8601 timestamp"):
            triage_issues(self.snapshot, as_of="not-a-date")


if __name__ == "__main__":
    unittest.main()
