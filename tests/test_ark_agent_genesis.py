import unittest

from scripts.ark_agent_genesis import build_registry, load_seed
from pathlib import Path
import json
import tempfile


class ArkAgentGenesisTests(unittest.TestCase):
    def test_recursive_proposal_reaches_l4_without_activation(self):
        seed = [{
            "agent_id": "L1-001",
            "level": "L1",
            "parent_id": None,
            "source_reference": "docs/canonical.md#role-charter",
        }]
        result = build_registry(seed, children_per_agent=1)
        self.assertEqual(result["agent_count"], 4)
        self.assertEqual([a["level"] for a in result["agents"]], ["L1", "L2", "L3", "L4"])
        self.assertTrue(all(a["execution_authorized"] is False for a in result["agents"]))
        self.assertFalse(result["safety"]["external_agents_spawned"])
        self.assertFalse(result["safety"]["layer4_mutated"])

    def test_seed_requires_source_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seed.json"
            path.write_text(json.dumps({"agents": [{
                "agent_id": "L1-001", "level": "L1", "parent_id": None
            }]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source_reference is required"):
                load_seed(path)

    def test_duplicate_ids_rejected(self):
        seed = [
            {"agent_id": "L1-001", "level": "L1", "parent_id": None, "source_reference": "source.md#one"},
            {"agent_id": "L1-001", "level": "L1", "parent_id": None, "source_reference": "source.md#two"},
        ]
        with self.assertRaisesRegex(ValueError, "Duplicate agent_id"):
            build_registry(seed, children_per_agent=0)


if __name__ == "__main__":
    unittest.main()
