from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBES = json.loads((ROOT / "probes" / "PROBE_SET_V1.json").read_text())
NODES = json.loads((ROOT / "regional_agents.json").read_text())["nodes"]
OUT = ROOT.parent / "data" / "regional-observations"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def call_endpoint(url: str, prompt: str, token: str | None) -> tuple[int, str, float]:
    body = json.dumps({"prompt": prompt}).encode()
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode("utf-8", errors="replace")
        return r.status, text, time.perf_counter() - started


def main() -> None:
    now = datetime.now(timezone.utc).isoformat()
    node_id = os.getenv("DRIFT_NODE", "UNASSIGNED")
    endpoint = os.getenv("DRIFT_ENDPOINT")
    token = os.getenv("DRIFT_TOKEN")
    model = os.getenv("DRIFT_MODEL", "UNSPECIFIED")
    language = os.getenv("DRIFT_LANGUAGE", "en")

    records = []
    for probe in PROBES["probes"]:
        rec = {
            "observation_id": f"OBS-{int(time.time())}-{probe['id']}-{node_id}",
            "timestamp": now,
            "node": node_id,
            "language": language,
            "model": model,
            "probe_id": probe["id"],
            "input_snapshot_hash": sha256(probe["prompt"]),
            "status": "NOT_CONFIGURED",
            "synthetic": False,
        }
        if endpoint:
            try:
                status, output, latency = call_endpoint(endpoint, probe["prompt"], token)
                rec.update({
                    "status": "RECORDED" if 200 <= status < 300 else "HTTP_ERROR",
                    "http_status": status,
                    "latency_seconds": round(latency, 4),
                    "output_hash": sha256(output),
                })
            except Exception as exc:
                rec.update({"status": "UNAVAILABLE", "error_type": type(exc).__name__})
        records.append(rec)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{node_id}.json"
    path.write_text(json.dumps({"schema_version": "0.1.0", "observations": records}, indent=2) + "\n")

    # GitHub Actions exposes this file path to the artifact-upload step. Only this
    # run's newly written file is uploaded; the historical directory is never bundled.
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as output:
            output.write(f"artifact_path={path}\n")
            output.write(f"record_count={len(records)}\n")

    print(json.dumps({"node": node_id, "records": len(records), "path": str(path)}))


if __name__ == "__main__":
    main()
