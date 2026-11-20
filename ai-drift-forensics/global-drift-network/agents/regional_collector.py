from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROBES = json.loads((ROOT / "probes" / "PROBE_SET_V1.json").read_text())
OUT = ROOT.parent / "data" / "regional-observations"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def call_endpoint(url: str, prompt: str, token: str | None) -> tuple[int, str, float]:
    body = json.dumps({"prompt": prompt}).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    started = time.perf_counter()
    with urllib.request.urlopen(req, timeout=30) as response:
        output = response.read().decode("utf-8", errors="replace")
        return response.status, output, time.perf_counter() - started


def main() -> int:
    node_id = os.getenv("DRIFT_NODE", "").strip()
    endpoint = os.getenv("DRIFT_ENDPOINT", "").strip()
    token = os.getenv("DRIFT_TOKEN")
    model = os.getenv("DRIFT_MODEL", "").strip()
    language = os.getenv("DRIFT_LANGUAGE", "en").strip()

    # Fail closed: never create or publish observation records without a real,
    # explicitly configured HTTPS endpoint and model identifier.
    missing = [
        name for name, value in (
            ("DRIFT_NODE", node_id),
            ("DRIFT_ENDPOINT", endpoint),
            ("DRIFT_MODEL", model),
        ) if not value
    ]
    if missing:
        raise SystemExit("BLOCKED: missing required configuration: " + ", ".join(missing))
    parsed_endpoint = urllib.parse.urlparse(endpoint)
    if parsed_endpoint.scheme != "https" or not parsed_endpoint.netloc:
        raise SystemExit("BLOCKED: DRIFT_ENDPOINT must be a valid HTTPS URL.")
    if model.upper() == "UNSPECIFIED":
        raise SystemExit("BLOCKED: DRIFT_MODEL must identify the configured model.")

    now = datetime.now(timezone.utc).isoformat()
    records = []
    failures = []

    for probe in PROBES["probes"]:
        rec = {
            "observation_id": f"OBS-{int(time.time())}-{probe['id']}-{node_id}",
            "timestamp": now,
            "node": node_id,
            "language": language,
            "model": model,
            "probe_id": probe["id"],
            "input_snapshot_hash": sha256(probe["prompt"]),
            "status": "UNAVAILABLE",
            "synthetic": False,
        }
        try:
            status, output, latency = call_endpoint(endpoint, probe["prompt"], token)
            if not 200 <= status < 300:
                raise RuntimeError(f"Endpoint returned HTTP {status}")
            rec.update({
                "status": "RECORDED",
                "http_status": status,
                "latency_seconds": round(latency, 4),
                "output_hash": sha256(output),
            })
        except Exception as exc:
            # Keep a truthful failure record for diagnostics. The non-zero
            # exit below prevents this batch from reaching the publisher.
            rec.update({
                "status": "UNAVAILABLE",
                "error_type": type(exc).__name__,
            })
            failures.append(probe["id"])
        records.append(rec)

    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{node_id}.json"
    path.write_text(
        json.dumps({"schema_version": "0.1.0", "observations": records}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "node": node_id,
        "records": len(records),
        "recorded": sum(record["status"] == "RECORDED" for record in records),
        "unavailable": len(failures),
        "path": str(path),
    }))

    if failures:
        raise SystemExit(
            f"BLOCKED: {len(failures)} probe(s) unavailable; batch will not be published."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
