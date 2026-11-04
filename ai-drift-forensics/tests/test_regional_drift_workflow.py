from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

AGENTS_DIR = Path(__file__).resolve().parents[1] / "global-drift-network" / "agents"
sys.path.insert(0, str(AGENTS_DIR))
import regional_collector


class RegionalDriftWorkflowTests(unittest.TestCase):
    def test_collector_exports_only_the_new_observation_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output_dir = root / "observations"
            github_output = root / "github-output.txt"
            environment = {
                "DRIFT_NODE": "REG-US",
                "DRIFT_LANGUAGE": "en",
                "DRIFT_ENDPOINT": "",
                "DRIFT_TOKEN": "",
                "DRIFT_MODEL": "UNCONFIGURED",
                "GITHUB_OUTPUT": str(github_output),
            }
            with patch.object(regional_collector, "OUT", output_dir), patch.dict(os.environ, environment):
                captured = StringIO()
                with redirect_stdout(captured):
                    regional_collector.main()

            result = json.loads(captured.getvalue())
            self.assertEqual("REG-US", result["node"])
            self.assertEqual(6, result["records"])
            observation_path = Path(result["path"])
            self.assertTrue(observation_path.is_file())
            self.assertEqual(output_dir, observation_path.parent)

            output_lines = github_output.read_text(encoding="utf-8").splitlines()
            self.assertIn(f"artifact_path={observation_path}", output_lines)
            self.assertIn("record_count=6", output_lines)

            payload = json.loads(observation_path.read_text(encoding="utf-8"))
            self.assertEqual(6, len(payload["observations"]))
            self.assertTrue(all(item["status"] == "NOT_CONFIGURED" for item in payload["observations"]))

    def test_workflow_uploads_only_current_files_and_uses_pull_request(self):
        workflow_path = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "regional-drift-agents.yml"
        workflow = workflow_path.read_text(encoding="utf-8")

        self.assertNotIn("git push", workflow)
        self.assertNotIn("git add ai-drift-forensics/global-drift-network/data/regional-observations/", workflow)
        self.assertIn("peter-evans/create-pull-request@v7", workflow)
        self.assertEqual(8, workflow.count("steps.collect.outputs.artifact_path"))
        self.assertIn("pattern: regional-*", workflow)
        self.assertIn("Expected exactly 8 regional observation files", workflow)
        self.assertIn("pull-requests: write", workflow)


if __name__ == "__main__":
    unittest.main()
