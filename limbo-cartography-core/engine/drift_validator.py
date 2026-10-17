"""Validate repository shape and recorded data; never simulate a clean forensic result."""
from __future__ import annotations
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    jsonschema = None

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_FILES = [
    "README.md",
    ".github/agents/cartography-agent-instructions.md",
    ".github/workflows/daily-cartography-agent.yml",
    "engine/__init__.py",
    "engine/deterministic_executor.py",
    "engine/drift_validator.py",
    "engine/seismic_detector.py",
    "engine/history_link_validator.py",
    "engine/tuning_candidate_builder.py",
    "engine/axiomatic_stress_tester.py",
    "engine/logic_bundle_builder.py",
    "schemas/deterministic_point_schema.json",
    "schemas/history_event_schema.json",
    "cartography/reality_matrix.json",
    "cartography/inbox/history_events/.gitkeep",
    "cartography/tuning_candidates/.gitkeep",
    "tests/test_drift_validator.py",
    "tests/test_schemas.py",
    "tests/test_cartography.py",
    "tests/test_history_links.py",
]
EXPECTED_DIRS = [
    ".github/agents", ".github/workflows", "engine", "schemas",
    "cartography", "cartography/logic_bundles", "cartography/tuning_candidates",
    "cartography/inbox/limbo_points", "cartography/inbox/history_events",
    "cartography/inbox/keystone_cases", "cartography/inbox/logic_bundles",
    "cartography/run_logs", "tests"
]

def validate_drift_status() -> dict:
    errors = []
    for rel in EXPECTED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"MISSING_FILE:{rel}")
    for rel in EXPECTED_DIRS:
        if not (ROOT / rel).is_dir():
            errors.append(f"MISSING_DIRECTORY:{rel}")

    incident_schema = event_schema = None
    schema_paths = {
        "INCIDENT": ROOT / "schemas/deterministic_point_schema.json",
        "EVENT": ROOT / "schemas/history_event_schema.json",
    }
    for label, path in schema_paths.items():
        if not path.is_file():
            continue
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            if jsonschema is not None:
                jsonschema.Draft7Validator.check_schema(schema)
            if label == "INCIDENT":
                incident_schema = schema
            else:
                event_schema = schema
        except Exception as exc:
            errors.append(f"INVALID_{label}_SCHEMA:{type(exc).__name__}:{exc}")

    matrix_path = ROOT / "cartography/reality_matrix.json"
    if matrix_path.is_file():
        try:
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            if not isinstance(matrix, dict):
                errors.append("MATRIX_TOP_LEVEL_NOT_OBJECT")
            else:
                records = matrix.get("daily_seismic_records")
                events = matrix.get("history_events")
                if not isinstance(records, list):
                    errors.append("MATRIX_RECORDS_NOT_LIST")
                if not isinstance(events, list):
                    errors.append("MATRIX_HISTORY_EVENTS_NOT_LIST")
                if jsonschema is not None and incident_schema is not None and isinstance(records, list):
                    validator = jsonschema.Draft7Validator(incident_schema, format_checker=jsonschema.FormatChecker())
                    for idx, record in enumerate(records):
                        for err in validator.iter_errors(record):
                            errors.append(f"MATRIX_RECORD_{idx}:{err.message}")
                if jsonschema is not None and event_schema is not None and isinstance(events, list):
                    validator = jsonschema.Draft7Validator(event_schema, format_checker=jsonschema.FormatChecker())
                    for idx, event in enumerate(events):
                        for err in validator.iter_errors(event):
                            errors.append(f"MATRIX_EVENT_{idx}:{err.message}")
        except Exception as exc:
            errors.append(f"INVALID_MATRIX:{type(exc).__name__}:{exc}")

    report = {
        "status": "FAILED" if errors else "STRUCTURALLY_VALID",
        "drift_detected": bool(errors),
        "checked_files": len(EXPECTED_FILES),
        "checked_directories": len(EXPECTED_DIRS),
        "errors": errors,
        "scope": "Repository shape, schemas and recorded structure only; not semantic verification or real-system replay."
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report

if __name__ == "__main__":
    sys.exit(1 if validate_drift_status()["drift_detected"] else 0)
