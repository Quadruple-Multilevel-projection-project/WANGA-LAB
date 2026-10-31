import json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/deterministic_point_schema.json").read_text(encoding="utf-8"))
VALIDATOR = jsonschema.Draft7Validator(SCHEMA, format_checker=jsonschema.FormatChecker())

def evidence():
    return {
        "source_uri": "https://example.invalid/source",
        "source_version": "fixture-v1",
        "source_sha256": None,
        "exact_locator": "section-1",
        "language": "en",
        "permission_scope": "SYNTHETIC_TEST_FIXTURE",
        "excerpt_or_summary": "Synthetic schema fixture only; not a real-world incident."
    }

def valid_record(status="OBSERVED"):
    return {
        "coordinate_id": "COORD-001",
        "timestamp_utc": "2026-10-17T00:00:00Z",
        "status": status,
        "legacy_system_status": "NOT_ASSESSED",
        "source_refs": ["https://example.invalid/source"],
        "source_evidence": [evidence()],
        "context": "Synthetic schema fixture only",
        "failure_observation": "Synthetic test record; not a real-world event.",
        "affected_component": "synthetic-component",
        "observed_state": "synthetic-state",
        "prior_incident_ids": []
    }

def test_valid_observation_is_accepted():
    assert list(VALIDATOR.iter_errors(valid_record())) == []

def test_verified_record_without_verification_is_rejected():
    record = valid_record("VERIFIED")
    assert list(VALIDATOR.iter_errors(record)), "VERIFIED must require explicit verification evidence"

def test_unknown_fields_are_rejected():
    record = valid_record()
    record["drift_coefficient"] = 0.0
    assert list(VALIDATOR.iter_errors(record))
