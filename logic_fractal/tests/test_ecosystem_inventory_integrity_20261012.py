import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class EcosystemInventoryIntegrityTests(unittest.TestCase):
    def test_inventory_names_are_unique_and_branches_are_present(self):
        inventory = json.loads((ROOT / "research/ecosystem/repository_inventory.json").read_text(encoding="utf-8"))
        repos = inventory["repositories"]
        names = [r["full_name"] for r in repos]
        self.assertEqual(len(names), len(set(names)))
        self.assertGreaterEqual(len(repos), 10)
        self.assertTrue(all(r.get("default_branch") for r in repos))

    def test_scan_cursor_is_resumable(self):
        inventory = json.loads((ROOT / "research/ecosystem/repository_inventory.json").read_text(encoding="utf-8"))
        cursor = inventory["scan_cursor"]
        self.assertEqual(cursor["completed_batch_number"], 1)
        self.assertEqual(cursor["completed_batch_size"], 10)
        self.assertEqual(len(cursor["scanned_repo_names"]), 10)
        self.assertGreater(len(cursor["next_batch_repo_names"]), 0)

if __name__ == "__main__":
    unittest.main()
