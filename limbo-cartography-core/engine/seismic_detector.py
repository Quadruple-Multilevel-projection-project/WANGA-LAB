"""Append source-backed Limbo incident records without rewriting history."""
from __future__ import annotations
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "cartography" / "inbox" / "limbo_points"
MATRIX_PATH = ROOT / "cartography" / "reality_matrix.json"
SCHEMA_PATH = ROOT / "schemas" / "deterministic_point_schema.json"

def record_seismic_events() -> dict:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    records = matrix.get("daily_seismic_records", [])
    persisted_ids = {r.get("coordinate_id") for r in records}
    seen_ids = set(persisted_ids)
    added, rejected = [], []
    for path in sorted(INBOX.glob("*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            validator.validate(item)
            incident_id = item["coordinate_id"]
            if incident_id in seen_ids:
                raise ValueError(f"DUPLICATE_COORDINATE_ID:{incident_id}")
            if incident_id in item.get("prior_incident_ids", []):
                raise ValueError("INCIDENT_CANNOT_REFERENCE_ITSELF_AS_PRIOR")
            unknown_prior = sorted(set(item.get("prior_incident_ids", [])) - persisted_ids)
            if unknown_prior:
                raise ValueError("UNKNOWN_PRIOR_INCIDENT_IDS:" + ",".join(unknown_prior))
            if item["status"] == "VERIFIED":
                verification = item.get("verification")
                if not isinstance(verification, dict) or not verification.get("procedure") or not verification.get("evidence_refs"):
                    raise ValueError("VERIFIED_REQUIRES_PROCEDURE_AND_EVIDENCE_REFS")
            seen_ids.add(incident_id)
            added.append(item)
        except Exception as exc:
            rejected.append({"file": path.name, "reason": f"{type(exc).__name__}:{exc}"})
    if rejected:
        result = {"status": "FAILED", "added": 0, "rejected": rejected,
                  "matrix_record_count": len(records), "history_preserved": True}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    if added:
        records.extend(added)
        matrix["daily_seismic_records"] = records
        matrix["last_updated"] = datetime.now(timezone.utc).date().isoformat()
        MATRIX_PATH.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {"status": "UPDATED" if added else "NO_INPUTS", "added": len(added), "rejected": 0,
              "matrix_record_count": len(records), "history_preserved": True,
              "input_directory": str(INBOX.relative_to(ROOT))}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result

if __name__ == "__main__":
    result = record_seismic_events()
    sys.exit(1 if result["status"] == "FAILED" else 0)
