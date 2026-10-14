"""Validate repository shape and recorded data; do not simulate a clean result."""
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
    "engine/axiomatic_stress_tester.py",
    "engine/logic_bundle_builder.py",
    "schemas/deterministic_point_schema.json",
    "cartography/reality_matrix.json",
    "tests/test_drift_validator.py",
    "tests/test_schemas.py",
    "tests/test_cartography.py",
]
EXPECTED_DIRS = [
    ".github/agents", ".github/workflows", "engine", "schemas",
    "cartography", "cartography/logic_bundles", "cartography/inbox/limbo_points",
    "cartography/inbox/keystone_cases", "cartography/inbox/logic_bundles", "cartography/run_logs", "tests"
]


def validate_drift_status() -> dict:
    errors: list[str] = []
    for rel in EXPECTED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"MISSING_FILE:{rel}")
    for rel in EXPECTED_DIRS:
        if not (ROOT / rel).is_dir():
            errors.append(f"MISSING_DIRECTORY:{rel}")

    schema_path = ROOT / "schemas/deterministic_point_schema.json"
    matrix_path = ROOT / "cartography/reality_matrix.json"
    schema = None
    if schema_path.is_file():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            if jsonschema is not None:
                jsonschema.Draft7Validator.check_schema(schema)
        except Exception as exc:
            errors.append(f"INVALID_SCHEMA:{type(exc).__name__}:{exc}")

    if matrix_path.is_file():
        try:
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            if not isinstance(matrix, dict):
                errors.append("MATRIX_TOP_LEVEL_NOT_OBJECT")
            elif not isinstance(matrix.get("daily_seismic_records"), list):
                errors.append("MATRIX_RECORDS_NOT_LIST")
            elif schema is not None and jsonschema is not None:
                validator = jsonschema.Draft7Validator(schema, format_checker=jsonschema.FormatChecker())
                for idx, record in enumerate(matrix["daily_seismic_records"]):
                    for err in validator.iter_errors(record):
                        errors.append(f"MATRIX_RECORD_{idx}:{err.message}")
        except Exception as exc:
            errors.append(f"INVALID_MATRIX:{type(exc).__name__}:{exc}")

    report = {
        "status": "FAILED" if errors else "STRUCTURALLY_VALID",
        "drift_detected": bool(errors),
        "checked_files": len(EXPECTED_FILES),
        "checked_directories": len(EXPECTED_DIRS),
        "errors": errors,
        "scope": "Repository structure and schema only; not semantic verification."
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


if __name__ == "__main__":
    sys.exit(1 if validate_drift_status()["drift_detected"] else 0)
