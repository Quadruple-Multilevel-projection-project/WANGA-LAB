import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/deterministic_point_schema.json").read_text(encoding="utf-8"))
VALIDATOR = jsonschema.Draft7Validator(SCHEMA, format_checker=jsonschema.FormatChecker())


def test_valid_observation_is_accepted():
    record = {
        "coordinate_id": "COORD-001",
        "timestamp_utc": "2026-10-14T10:00:00Z",
        "status": "OBSERVED",
        "legacy_system_status": "NOT_ASSESSED",
        "source_refs": ["https://example.invalid/source#section-1"],
        "context": "Synthetic schema fixture only",
        "failure_observation": "Synthetic test record; not a real-world event."
    }
    assert list(VALIDATOR.iter_errors(record)) == []


def test_verified_record_without_verification_is_rejected():
    record = {
        "coordinate_id": "COORD-002",
        "timestamp_utc": "2026-10-14T10:00:00Z",
        "status": "VERIFIED",
        "legacy_system_status": "NOT_ASSESSED",
        "source_refs": ["fixture:source"],
        "context": "Synthetic schema fixture only",
        "failure_observation": "Synthetic test record."
    }
    assert list(VALIDATOR.iter_errors(record)), "VERIFIED must require explicit verification evidence"


def test_unknown_fields_are_rejected():
    record = {
        "coordinate_id": "COORD-003",
        "timestamp_utc": "2026-10-14T10:00:00Z",
        "status": "OBSERVED",
        "legacy_system_status": "NOT_ASSESSED",
        "source_refs": ["fixture:source"],
        "context": "fixture",
        "failure_observation": "fixture",
        "drift_coefficient": 0.0
    }
    assert list(VALIDATOR.iter_errors(record))
