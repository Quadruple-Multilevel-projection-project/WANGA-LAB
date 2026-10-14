"""Validate explicitly supplied Limbo records; never invent collapse coordinates."""
from __future__ import annotations

import json
import sys
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
    existing_ids = {r.get("coordinate_id") for r in matrix["daily_seismic_records"]}
    added: list[dict] = []
    rejected: list[dict] = []

    for path in sorted(INBOX.glob("*.json")):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            validator.validate(item)
            coordinate_id = item["coordinate_id"]
            if coordinate_id in existing_ids:
                raise ValueError(f"DUPLICATE_COORDINATE_ID:{coordinate_id}")
            if item["status"] == "VERIFIED":
                verification = item.get("verification")
                if not isinstance(verification, dict) or not verification.get("procedure") or not verification.get("evidence_refs"):
                    raise ValueError("VERIFIED_REQUIRES_PROCEDURE_AND_EVIDENCE_REFS")
            existing_ids.add(coordinate_id)
            added.append(item)
        except Exception as exc:
            rejected.append({"file": path.name, "reason": f"{type(exc).__name__}:{exc}"})

    if rejected:
        print(json.dumps({"status": "FAILED", "added": len(added), "rejected": rejected}, ensure_ascii=False, indent=2))
        return {"status": "FAILED", "added": len(added), "rejected": rejected}

    if added:
        matrix["daily_seismic_records"].extend(added)
        matrix["daily_seismic_records"].sort(key=lambda x: (x["timestamp_utc"], x["coordinate_id"]))
        MATRIX_PATH.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    result = {"status": "UPDATED" if added else "NO_INPUTS", "added": len(added), "rejected": 0,
              "matrix_record_count": len(matrix["daily_seismic_records"]),
              "input_directory": str(INBOX.relative_to(ROOT))}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    result = record_seismic_events()
    sys.exit(1 if result["status"] == "FAILED" else 0)
