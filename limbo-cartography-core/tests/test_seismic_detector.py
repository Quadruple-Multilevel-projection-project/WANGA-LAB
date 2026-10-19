import json

from engine import seismic_detector


def evidence(incident_id):
    return {
        "source_uri": f"https://example.invalid/{incident_id}",
        "source_version": "fixture-v1",
        "source_sha256": None,
        "exact_locator": "fixture:line-1",
        "language": "en",
        "permission_scope": "SYNTHETIC_TEST_FIXTURE",
        "excerpt_or_summary": "Synthetic intake fixture only; not a real crash."
    }


def record(incident_id, timestamp, prior=None):
    return {
        "coordinate_id": incident_id,
        "timestamp_utc": timestamp,
        "status": "OBSERVED",
        "legacy_system_status": "LOCAL_STRUCTURE_FAILURE",
        "source_refs": [f"https://example.invalid/{incident_id}"],
        "source_evidence": [evidence(incident_id)],
        "context": "Synthetic test fixture",
        "failure_observation": "Synthetic crash point",
        "affected_component": "fixture-component",
        "observed_state": "fixture-state",
        "prior_incident_ids": [prior] if prior else [],
    }


def test_ordered_batch_links_prior_points_and_is_idempotent(tmp_path, monkeypatch):
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    matrix_path = tmp_path / "reality_matrix.json"
    matrix_path.write_text(json.dumps({
        "cartography_version": "1.1.0",
        "last_updated": "2026-10-12",
        "system_state": "INITIALIZED_NO_OBSERVATIONS",
        "daily_seismic_records": [],
        "history_events": [],
    }), encoding="utf-8")

    schema_path = seismic_detector.SCHEMA_PATH
    first = record("INC-001", "2026-10-13T00:00:00Z")
    second = record("INC-002", "2026-10-14T00:00:00Z", "INC-001")
    (inbox / "2026-10-13T000000Z.json").write_text(json.dumps(first), encoding="utf-8")
    (inbox / "2026-10-14T000000Z.json").write_text(json.dumps(second), encoding="utf-8")

    monkeypatch.setattr(seismic_detector, "INBOX", inbox)
    monkeypatch.setattr(seismic_detector, "MATRIX_PATH", matrix_path)
    monkeypatch.setattr(seismic_detector, "SCHEMA_PATH", schema_path)

    first_result = seismic_detector.record_seismic_events()
    assert first_result["status"] == "UPDATED"
    stored = json.loads(matrix_path.read_text(encoding="utf-8"))
    assert [item["coordinate_id"] for item in stored["daily_seismic_records"]] == ["INC-001", "INC-002"]
    assert stored["daily_seismic_records"][1]["prior_incident_ids"] == ["INC-001"]

    second_result = seismic_detector.record_seismic_events()
    assert second_result["status"] == "ALREADY_CURRENT"
    assert second_result["added"] == 0
    assert second_result["already_present"] == ["INC-001", "INC-002"]
