import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class CredentialCoordinationConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(
            (ROOT / "config/security/credential-coordination.v1.json").read_text(encoding="utf-8")
        )
        cls.umbrella = json.loads(
            (ROOT / "config/umbrella/global-institute-of-neuronics.v1.json").read_text(encoding="utf-8")
        )

    def test_institute_has_three_bodies_and_independent_oversight(self):
        institute = self.umbrella["institute"]
        self.assertEqual(
            {x["id"] for x in institute["bodies"]},
            {"DEEP-NETWORK-ANALYTICS", "DEEP-NETWORK-LOGISTICS", "DEEP-NETWORK-ALGORITHMS"},
        )
        self.assertEqual(institute["oversight"]["id"], "OR")
        self.assertEqual(institute["oversight"]["access"], "read_only_audit_and_hold_recommendation")

    def test_local_gcm_lock_is_current_user_only(self):
        lock = self.config["concurrency"]["local_gcm"]
        self.assertEqual(lock["scope"], "CurrentUser")
        self.assertEqual(lock["supported_scopes"], ["CurrentUser"])
        self.assertIn("Machine", lock["unsupported_scopes"])
        self.assertTrue(lock["diagnostics"]["automatic_deletion"] is False)

    def test_cloud_lock_is_not_misrepresented_as_implemented(self):
        cloud = self.config["concurrency"]["cloud_orchestrator"]
        self.assertEqual(cloud["state"], "NOT_IMPLEMENTED")
        self.assertIn("fencing_token", cloud["required_primitives"])
        self.assertIn("Do not use a local file lock", cloud["prohibited_substitution"])

    def test_secret_reference_contains_no_secret_value(self):
        ref = self.config["providers"]["appdeploy_secret_vault"]["credential_refs"][0]
        self.assertEqual(ref["name"], "GITHUB_FINE_GRAINED_TOKEN")
        self.assertNotIn("value", ref)
        self.assertNotIn("token", ref)
        self.assertEqual(ref["scope"], "single_repository")

    def test_oversight_cannot_read_or_write_credentials(self):
        oversight = self.config["policy"]["oversight"]
        self.assertFalse(oversight["can_read_secret_values"])
        self.assertFalse(oversight["can_write_credentials"])

    def test_oauth_token_exchange_is_disabled_until_upstream_and_provider_gate(self):
        exchange = self.config["token_exchange"]
        self.assertEqual(exchange["protocol"], "OAuth 2.0 Token Exchange (RFC 8693)")
        self.assertFalse(exchange["enabled"])
        self.assertEqual(self.config["readiness"]["status"], "PREPARED_NOT_CONNECTED")

    def test_agent_tokens_are_task_scoped(self):
        agents = self.config["policy"]["agents"]
        self.assertEqual(agents["credential_lifetime"], "one_task_or_short_lived_provider_token")
        self.assertTrue(agents["secret_reference_only"])


if __name__ == "__main__":
    unittest.main()
