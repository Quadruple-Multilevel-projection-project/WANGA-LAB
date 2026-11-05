import unittest

from wanga_runtime.core import WangaRuntime


class WangaRuntimeStateEvidenceTests(unittest.TestCase):
    def test_deterministic_execution_state_and_evidence(self):
        runtime = WangaRuntime()
        first = runtime.run({"question": "deterministic"})
        second = runtime.run({"question": "deterministic"})

        self.assertEqual(first, second)
        self.assertEqual(first["verification_status"], "PASSED")
        self.assertEqual(
            first["state"],
            [
                "INGESTED",
                "ROUTED:planner",
                "COMPLETED:planner",
                "ROUTED:implementer",
                "COMPLETED:implementer",
                "ROUTED:verifier",
                "COMPLETED:verifier",
                "VERIFIED",
                "EVIDENCE_EMITTED",
                "COMPLETED",
            ],
        )
        self.assertEqual([item["status"] for item in first["evidence"]], ["COMPLETED", "COMPLETED", "COMPLETED", "PASS"])
        self.assertEqual(first["evidence"][-1]["stage"], "VERIFY")

    def test_unknown_role_stops_before_execution(self):
        runtime = WangaRuntime()
        report = runtime.run({"question": "route"}, roles=("planner", "unknown"))

        self.assertEqual(report["verification_status"], "FAILED")
        self.assertEqual(report["state"], ["INGESTED", "ROUTED:planner", "COMPLETED:planner", "FAILED"])
        self.assertEqual(report["evidence"][-1]["status"], "FAIL")
        self.assertEqual(report["evidence"][-1]["detail"]["unknown_role"], "unknown")


if __name__ == "__main__":
    unittest.main()
