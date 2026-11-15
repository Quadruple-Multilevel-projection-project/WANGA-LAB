import unittest
from copy import deepcopy
from business_brain.ledger_verifier import (
    LedgerVerificationError, canonical_event_digest, verify_chain,
)


def make_event(event_id, previous):
    event = {
        "event_id": event_id,
        "event_type": "CONTRIBUTION_SUBMITTED",
        "previous_event_sha256": previous,
        "quantity": 0,
        "unit": "LOGIC_CREDIT_INTERNAL",
    }
    event["event_sha256"] = canonical_event_digest(event)
    return event


class LedgerVerifierTests(unittest.TestCase):
    def test_valid_two_event_chain(self):
        first = make_event("LCE-TEST-00000001", None)
        second = make_event("LCE-TEST-00000002", first["event_sha256"])
        self.assertEqual(verify_chain([first, second]), second["event_sha256"])

    def test_rejects_duplicate_event_id(self):
        first = make_event("LCE-TEST-00000001", None)
        duplicate = deepcopy(first)
        with self.assertRaisesRegex(LedgerVerificationError, "duplicate event_id"):
            verify_chain([first, duplicate])

    def test_rejects_broken_previous_hash(self):
        first = make_event("LCE-TEST-00000001", None)
        second = make_event("LCE-TEST-00000002", "f" * 64)
        with self.assertRaisesRegex(LedgerVerificationError, "broken previous"):
            verify_chain([first, second])

    def test_rejects_modified_event(self):
        first = make_event("LCE-TEST-00000001", None)
        first["quantity"] = 100
        with self.assertRaisesRegex(LedgerVerificationError, "digest mismatch"):
            verify_chain([first])

    def test_rejects_empty_ledger(self):
        with self.assertRaisesRegex(LedgerVerificationError, "empty"):
            verify_chain([])


if __name__ == "__main__":
    unittest.main()
