import unittest

from governance.constitutional_gate import evaluate_task, may_dispatch


class ConstitutionalGateTests(unittest.TestCase):
    def test_missing_canonical_axiom_fails_closed(self):
        decision = evaluate_task({
            "constitutional_axiom_id": "AXIOM-001",
            "requested_operation": "core_compute",
            "allowed_operations": ["core_compute"],
        })
        self.assertEqual(decision.status, "BLOCKED")
        self.assertFalse(may_dispatch(decision))

    def test_documentation_only_is_review_not_execution(self):
        decision = evaluate_task({"requested_operation": "documentation_only"})
        self.assertEqual(decision.status, "PASS_FOR_REVIEW")
        self.assertFalse(may_dispatch(decision))

    def test_complete_approved_envelope_passes(self):
        decision = evaluate_task({
            "task_id": "T-1",
            "message_id": "M-1",
            "constitutional_axiom_id": "AXIOM-001",
            "constitution_source_ref": "canonical://axiom-001",
            "constitution_version": "1.0",
            "axiom_source_verified": True,
            "derived_law_refs": ["ROOT-LAW-1"],
            "requested_operation": "core_compute",
            "allowed_operations": ["core_compute"],
            "source_refs": ["source://evidence-1"],
            "unresolved_conflicts": [],
            "architect_approval_receipt": "approval://architect/receipt-1",
        })
        self.assertEqual(decision.status, "PASS")
        self.assertTrue(may_dispatch(decision))
        self.assertEqual(len(decision.receipt_sha256), 64)


if __name__ == "__main__":
    unittest.main()
