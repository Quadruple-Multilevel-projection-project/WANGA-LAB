from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[2]
BUILDER = ROOT / "scripts" / "build_first_fractal_model.py"
OUTPUT = ROOT / "research" / "reports" / "logic-fractal" / "typed-first-model-candidate.json"


class FirstModelBuilderRegressionTests(unittest.TestCase):
    def test_builder_archives_reproducible_release_blocked_candidate(self):
        completed = subprocess.run(
            [sys.executable, str(BUILDER)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("CANDIDATE_NOT_RELEASED", completed.stdout)
        artifact = json.loads(OUTPUT.read_text(encoding="utf-8"))

        self.assertEqual(artifact["status"], "CANDIDATE_NOT_RELEASED")
        self.assertEqual(artifact["semantic_status"], "NOT_YET_VERIFIED")
        self.assertRegex(artifact["model_hash"], re.compile(r"^[0-9a-f]{64}$"))
        self.assertEqual(
            [level["scale"] for level in artifact["composition_levels"]],
            [1, 2],
        )
        self.assertTrue(artifact["release_gate"]["source_lineage_preserved"])
        self.assertTrue(artifact["release_gate"]["two_scales_composed"])
        self.assertTrue(artifact["release_gate"]["replay_deterministic"])
        self.assertTrue(artifact["release_gate"]["uses_synthetic_only_fixtures"])
        self.assertFalse(artifact["release_gate"]["real_conversation_sources_reviewed"])
        self.assertFalse(artifact["release_gate"]["negative_boundary_benchmark_complete"])
        self.assertFalse(artifact["release_gate"]["independent_review_complete"])
        self.assertEqual(
            artifact["release_gate"]["decision"],
            "BLOCKED_PENDING_REAL_SOURCE_FRAGMENTS_NEGATIVE_BOUNDARY_TESTS_AND_INDEPENDENT_REVIEW",
        )


if __name__ == "__main__":
    unittest.main()
