import json
import unittest

from wanga_runtime.probabilistic_io import (
    HALT,
    PENDING,
    STATE,
    ProbabilisticIOInterface,
)


class ProbabilisticIOInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.io = ProbabilisticIOInterface()

    @staticmethod
    def valid_logic():
        return {
            "first_order": {
                "internal": "checked",
                "external": "checked",
                "coordination": "checked",
            },
            "second_order": {
                "part_1": "checked",
                "part_2": "checked",
                "part_3": "checked",
            },
            "private_logic": {
                "part_1": "open",
                "part_2": "open",
                "part_3": "open",
            },
            "private_complete": False,
            "investigation_complete": False,
            "contradictions": [],
        }

    def test_valid_request_produces_structured_proposal(self):
        result = self.io.propose({"action": "write", "payload": "hello", "logical_consistency": self.valid_logic()})
        self.assertEqual(result.supervisor_status, PENDING)
        self.assertEqual(result.logical_state_id, STATE)
        self.assertTrue(result.validation.valid)
        proposal = json.loads(result.payload)
        self.assertEqual(proposal["execution"], "NOT_PERFORMED")
        self.assertIn("request_digest", proposal)

    def test_missing_context_halts(self):
        result = self.io.propose({"action": "write"})
        self.assertEqual(result.payload, HALT)
        self.assertFalse(result.validation.valid)
        self.assertIn("payload", result.validation.missing_context)
        self.assertIn("logical_consistency", result.validation.missing_context)

    def test_execution_boundary_halts(self):
        result = self.io.propose(
            {"action": "write", "payload": "hello", "execute": True, "logical_consistency": self.valid_logic()}
        )
        self.assertEqual(result.payload, HALT)
        self.assertIn(
            "EXECUTION_REQUESTED_INSIDE_PROPOSAL_ONLY_BOUNDARY",
            result.validation.contradiction_vector,
        )

    def test_state_mutation_boundary_halts(self):
        result = self.io.propose(
            {"action": "write", "payload": "hello", "mutate_state": True, "logical_consistency": self.valid_logic()}
        )
        self.assertEqual(result.payload, HALT)
        self.assertIn(
            "STATE_MUTATION_REQUESTED_INSIDE_PROPOSAL_ONLY_BOUNDARY",
            result.validation.contradiction_vector,
        )

    def test_non_object_request_halts_without_guessing(self):
        result = self.io.propose("not-an-object")
        self.assertEqual(result.payload, HALT)
        self.assertIn("REQUEST_MUST_BE_OBJECT", result.validation.contradiction_vector)


if __name__ == "__main__":
    unittest.main()
