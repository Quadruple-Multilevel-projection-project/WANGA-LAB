import json
from pathlib import Path

from engine.history_link_validator import validate_history_data
from engine.tuning_candidate_builder import build_candidates

ROOT = Path(__file__).resolve().parents[1]
INCIDENT_SCHEMA = json.loads((ROOT / "schemas/deterministic_point_schema.json").read_text(encoding="utf-8"))
EVENT_SCHEMA = json.loads((ROOT / "schemas/history_event_schema.json").read_text(encoding="utf-8"))

def evidence(uri="https://example.invalid/evidence", locator="fixture:line-1"):
    return {
        "source_uri": uri,
        "source_version": "fixture-v1",
        "source_sha256": None,
        "exact_locator": locator,
        "language": "en",
        "permission_scope": "SYNTHETIC_TEST_FIXTURE",
        "excerpt_or_summary": "Synthetic fixture only; not a real incident."
    }

def incident():
    return {
        "coordinate_id": "INC-001",
        "timestamp_utc": "2026-10-17T00:00:00Z",
        "status": "OBSERVED",
        "legacy_system_status": "LOCAL_STRUCTURE_FAILURE",
        "source_refs": ["https://example.invalid/evidence"],
        "source_evidence": [evidence()],
        "context": "Synthetic fixture only",
        "failure_observation": "Synthetic failure observation.",
        "affected_component": "engine-x",
        "observed_state": "synthetic-state",
        "prior_incident_ids": []
    }

def change_event():
    return {
        "event_id": "CHANGE-001",
        "event_type": "CHANGE_APPLIED",
        "timestamp_utc": "2026-10-17T01:00:00Z",
        "affected_incident_ids": ["INC-001"],
        "component": "engine-x",
        "source_evidence": [evidence(locator="fixture:change")],
        "previous_event_ids": [],
        "change_summary": "Synthetic config change for a unit test.",
        "configuration_delta": {"threshold": 0.7}
    }

def retest_event(result="PASS"):
    return {
        "event_id": "RETEST-001",
        "event_type": "RETEST",
        "timestamp_utc": "2026-10-17T02:00:00Z",
        "affected_incident_ids": ["INC-001"],
        "component": "engine-x",
        "source_evidence": [evidence(locator="fixture:retest")],
        "previous_event_ids": ["CHANGE-001"],
        "test_id": "TEST-001",
        "result": result,
        "evidence_refs": ["fixture:retest-result"]
    }

def test_empty_map_reports_no_inputs_not_coverage():
    result = validate_history_data({"daily_seismic_records": [], "history_events": []}, INCIDENT_SCHEMA, EVENT_SCHEMA)
    assert result["status"] == "NO_INPUTS"
    assert result["semantic_verification"] is False

def test_dangling_incident_reference_fails_closed():
    event = change_event()
    event["affected_incident_ids"] = ["INC-MISSING"]
    result = validate_history_data({"daily_seismic_records": [incident()], "history_events": [event]}, INCIDENT_SCHEMA, EVENT_SCHEMA)
    assert result["status"] == "FAILED"
    assert any("DANGLING_EVENT_INCIDENT_REF" in error for error in result["errors"])

def test_only_linked_passing_retest_emits_candidate():
    matrix = {"daily_seismic_records": [incident()], "history_events": [change_event(), retest_event("PASS")]}
    first = build_candidates(matrix)
    second = build_candidates(matrix)
    assert len(first) == 1
    assert first == second
    assert first[0]["status"] == "CANDIDATE_REPLAY_REQUIRED"
    assert first[0]["replay_status"] == "NOT_RUN"
    assert first[0]["semantic_status"] == "NOT_YET_VERIFIED"

def test_failed_retest_does_not_emit_candidate():
    matrix = {"daily_seismic_records": [incident()], "history_events": [change_event(), retest_event("FAIL")]}
    assert build_candidates(matrix) == []

def test_history_parent_must_precede_child():
    event = retest_event("PASS")
    event["timestamp_utc"] = "2026-10-17T00:30:00Z"
    result = validate_history_data({"daily_seismic_records": [incident()], "history_events": [change_event(), event]}, INCIDENT_SCHEMA, EVENT_SCHEMA)
    assert result["status"] == "FAILED"
    assert any("EVENT_TIME_PRECEDES_PARENT" in error for error in result["errors"])
