from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from logic_fractal.source_candidate_builder import write_candidate_artifact


def main() -> int:
    artifact = write_candidate_artifact()
    print(json.dumps({
        "candidate_id": artifact["candidate_id"],
        "status": artifact["status"],
        "model_hash": artifact["composition"]["fragment"]["model_hash"],
        "artifact_hash": artifact["artifact_hash"],
        "output": "research/reports/logic-fractal/source-backed-gate13-candidate.json",
        "test_outcomes": artifact["test_outcomes"],
        "release_decision": artifact["release_decision"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
