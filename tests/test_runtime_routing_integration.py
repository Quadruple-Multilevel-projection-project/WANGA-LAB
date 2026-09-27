import unittest

from wanga_runtime.core import WangaRuntime
from wanga_runtime.routing import route_request


class RuntimeRoutingIntegrationTests(unittest.TestCase):
    def test_specific_compute_route_precedes_generic_model_route(self):
        decision = route_request("compute/runtime/model-fabric/virtual-gpu")
        self.assertEqual(decision.target, "compute-infrastructure")
        self.assertEqual(decision.priority, 100)

    def test_runtime_receives_routed_role_and_emits_verification(self):
        decision = route_request("drift/evidence/forensic-audit")
        self.assertEqual(decision.target, "ai-drift-forensics")
        runtime = WangaRuntime()
        report = runtime.run({"route": decision.target}, roles=("planner", "verifier"))
        self.assertEqual(report["verification_status"], "PASSED")
        self.assertIn("VERIFIED", report["state"])
        self.assertEqual(report["evidence"][-1]["stage"], "VERIFY")
        self.assertEqual(report["evidence"][-1]["status"], "PASS")

    def test_unknown_route_is_explicit_and_deterministic(self):
        first = route_request("unknown/domain")
        second = route_request("unknown/domain")
        self.assertEqual(first, second)
        self.assertEqual(first.target, "unrouted")
        self.assertEqual(first.priority, 0)


if __name__ == "__main__":
    unittest.main()
