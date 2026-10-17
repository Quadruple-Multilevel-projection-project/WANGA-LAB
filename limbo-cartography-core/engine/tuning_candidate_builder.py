"""Build tuning candidates only from explicit sourced changes with linked passing retests."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from engine.history_link_validator import validate_history_data

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "cartography" / "reality_matrix.json"
INCIDENT_SCHEMA_PATH = ROOT / "schemas" / "deterministic_point_schema.json"
EVENT_SCHEMA_PATH = ROOT / "schemas" / "history_event_schema.json"
OUT = ROOT / "cartography" / "tuning_candidates"


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_candidates(matrix: dict[str, Any]) -> list[dict]:
    incidents = {item.get("coordinate_id"): item for item in matrix.get("daily_seismic_records", [])}
    events = matrix.get("history_events", [])
    candidates: list[dict] = []
    for change in events:
        if change.get("event_type") != "CHANGE_APPLIED":
            continue
        delta = change.get("configuration_delta")
        evidence = change.get("source_evidence")
        if not isinstance(delta, dict) or not delta or not isinstance(evidence, list) or not evidence:
            continue
        for retest in events:
            if retest.get("event_type") != "RETEST" or retest.get("result") != "PASS":
                continue
            if change.get("event_id") not in retest.get("previous_event_ids", []):
                continue
            if change.get("component") != retest.get("component"):
                continue
            shared_incidents = sorted(set(change.get("affected_incident_ids", [])) & set(retest.get("affected_incident_ids", [])))
            if not shared_incidents or any(incident_id not in incidents for incident_id in shared_incidents):
                continue
            retest_evidence = retest.get("source_evidence")
            if not isinstance(retest_evidence, list) or not retest_evidence:
                continue
            stable_basis = {
                "component": change["component"],
                "incident_ids": shared_incidents,
                "change_event_id": change["event_id"],
                "retest_event_id": retest["event_id"],
                "configuration_delta": delta,
                "change_source_evidence": evidence,
                "retest_source_evidence": retest_evidence
            }
            candidate_id = "TUNE-" + hashlib.sha256(_canonical(stable_basis).encode("utf-8")).hexdigest()[:16]
            candidates.append({
                "candidate_id": candidate_id,
                "status": "CANDIDATE_REPLAY_REQUIRED",
                "component": change["component"],
                "parent_incident_ids": shared_incidents,
                "change_event_id": change["event_id"],
                "retest_event_id": retest["event_id"],
                "configuration_delta": delta,
                "source_evidence": {"change_event": evidence, "passing_retest": retest_evidence},
                "retest_result": "PASS",
                "replay_status": "NOT_RUN",
                "semantic_status": "NOT_YET_VERIFIED",
                "scope": "Reuse of an explicitly recorded configuration change after a linked passing retest; no causal generalization is inferred.",
                "limitations": [
                    "A passing retest applies only to its recorded context.",
                    "Replay against the current target system remains required.",
                    "No weight, relation, or semantic claim is inferred from this candidate."
                ]
            })
    unique = {item["candidate_id"]: item for item in candidates}
    return [unique[key] for key in sorted(unique)]


def build_tuning_candidates() -> dict:
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    incident_schema = json.loads(INCIDENT_SCHEMA_PATH.read_text(encoding="utf-8"))
    event_schema = json.loads(EVENT_SCHEMA_PATH.read_text(encoding="utf-8"))
    validation = validate_history_data(matrix, incident_schema, event_schema)
    if validation["status"] == "FAILED":
        result = {"status": "FAILED", "candidate_count": 0, "errors": validation["errors"]}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    candidates = build_candidates(matrix)
    if not matrix.get("daily_seismic_records") and not matrix.get("history_events"):
        result = {"status": "NO_INPUTS", "candidate_count": 0, "replay_performed": False}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    if not candidates:
        result = {"status": "NO_ELIGIBLE_TUNING_EVIDENCE", "candidate_count": 0, "replay_performed": False}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    OUT.mkdir(parents=True, exist_ok=True)
    created, existing, rejected = [], [], []
    for candidate in candidates:
        path = OUT / f"{candidate['candidate_id']}.json"
        if path.exists():
            try:
                current = json.loads(path.read_text(encoding="utf-8"))
                if current == candidate:
                    existing.append(candidate["candidate_id"])
                else:
                    rejected.append({"candidate_id": candidate["candidate_id"], "reason": "CANDIDATE_ID_CONTENT_MISMATCH"})
            except Exception as exc:
                rejected.append({"candidate_id": candidate["candidate_id"], "reason": f"{type(exc).__name__}:{exc}"})
            continue
        path.write_text(json.dumps(candidate, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        created.append(candidate["candidate_id"])

    status = "FAILED" if rejected else ("BUILT" if created else "NO_NEW_CANDIDATES")
    result = {"status": status, "candidate_count": len(candidates), "created": created,
              "already_present": existing, "rejected": rejected, "replay_performed": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    result = build_tuning_candidates()
    sys.exit(1 if result["status"] == "FAILED" else 0)
