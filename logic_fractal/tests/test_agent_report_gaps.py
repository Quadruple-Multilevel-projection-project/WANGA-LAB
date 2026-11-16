import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.run_logic_agents import source_span_gap_message


class AgentCycleGapMessageTests(unittest.TestCase):
    def test_registered_units_are_reported_with_actual_deficit(self):
        message = source_span_gap_message(11, 50)
        self.assertIn("11 admitted source-span logic units are registered", message)
        self.assertIn("39 more are required", message)
        self.assertNotIn("no source-span logic-unit records are registered yet", message.lower())

    def test_zero_units_are_reported_as_zero(self):
        self.assertEqual(
            source_span_gap_message(0, 50),
            "No admitted source-span logic units are registered; 50 are required."
        )

    def test_met_threshold_is_not_reported_as_a_gap(self):
        self.assertEqual(
            source_span_gap_message(50, 50),
            "50 admitted source-span logic units are registered; configured threshold 50 is met."
        )


if __name__ == "__main__":
    unittest.main()
