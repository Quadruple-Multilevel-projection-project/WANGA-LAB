import unittest

from wanga_runtime.continuity import (
    HALT,
    LogicalConsistencyGate,
    build_checkpoint,
    checkpoint_digest,
    validate_checkpoint,
)


class LogicalConsistencyGateTests(unittest.TestCase):
    def valid_logic(self):
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

    def test_requires_all_three_layers(self):
        logic = self.valid_logic()
        del logic["second_order"]["part_3"]
        result = LogicalConsistencyGate.validate(logic)
        self.assertFalse(result.valid)
        self.assertIn("second_order.part_3", result.missing_context)

    def test_private_logic_is_not_higher_order(self):
        logic = self.valid_logic()
        logic["private_is_higher_order"] = True
        result = LogicalConsistencyGate.validate(logic)
        self.assertFalse(result.valid)
        self.assertIn("PRIVATE_LOGIC_IS_NOT_A_HIGHER_ORDER", result.contradictions)

    def test_investigation_cannot_close_before_private_completion(self):
        logic = self.valid_logic()
        logic["investigation_complete"] = True
        result = LogicalConsistencyGate.validate(logic)
        self.assertFalse(result.valid)
        self.assertIn(
            "INVESTIGATION_CLOSED_BEFORE_PRIVATE_COMPLETION",
            result.contradictions,
        )

    def test_private_completion_is_allowed_only_after_three_parts_exist(self):
        logic = self.valid_logic()
        logic["private_complete"] = True
        result = LogicalConsistencyGate.validate(logic)
        self.assertTrue(result.valid)
        self.assertTrue(result.private_complete)

    def test_checkpoint_is_deterministic(self):
        checkpoint = build_checkpoint(
            checkpoint_id="PIO-0001",
            central_objective="Complete and verify Probabilistic I/O Interface",
            current_status="TESTED",
            last_completed_action="Unit tests passed",
            next_action={"id": "A-002", "description": "Run frontend verification"},
            logical_consistency={"first_order": {}, "second_order": {}, "private_logic": {}},
        )
        self.assertEqual(validate_checkpoint(checkpoint), ())
        self.assertEqual(checkpoint_digest(checkpoint), checkpoint_digest(checkpoint))
        self.assertEqual(checkpoint.to_json(), checkpoint.to_json())

    def test_checkpoint_requires_single_next_action(self):
        with self.assertRaises(ValueError):
            build_checkpoint(
                checkpoint_id="PIO-0002",
                central_objective="PIO",
                current_status="TESTED",
                last_completed_action="",
                next_action={},
                logical_consistency={},
            )


if __name__ == "__main__":
    unittest.main()
