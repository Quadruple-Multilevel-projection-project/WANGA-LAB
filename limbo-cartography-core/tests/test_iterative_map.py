import copy

from engine.iterative_map_builder import build_iterative_map


def incident(incident_id, timestamp, prior=None, component="runtime-a", state="failure-observed"):
    return {
        "coordinate_id": incident_id,
        "timestamp_utc": timestamp,
        "status": "OBSERVED",
        "legacy_system_status": "LOCAL_STRUCTURE_FAILURE",
        "source_refs": [f"https://example.invalid/{incident_id}"],
        "source_evidence": [{
            "source_uri": f"https://example.invalid/{incident_id}",
            "source_version": "fixture-v1",
            "source_sha256": None,
            "exact_locator": "fixture:line-1",
            "language": "en",
            "permission_scope": "SYNTHETIC_TEST_FIXTURE",
            "excerpt_or_summary": "Synthetic unit-test fixture; not a real crash."
        }],
        "context": "Synthetic fixture only",
        "failure_observation": "Synthetic failure",
        "affected_component": component,
        "observed_state": state,
        "prior_incident_ids": [prior] if prior else [],
    }


def event(event_id, event_type, timestamp, incident_id, previous=None, result=None):
    item = {
        "event_id": event_id,
        "event_type": event_type,
        "timestamp_utc": timestamp,
        "affected_incident_ids": [incident_id],
        "component": "runtime-a",
        "source_evidence": [{
            "source_uri": f"https://example.invalid/{event_id}",
            "source_version": "fixture-v1",
            "source_sha256": None,
            "exact_locator": "fixture:event",
            "language": "en",
            "permission_scope": "SYNTHETIC_TEST_FIXTURE",
            "excerpt_or_summary": "Synthetic unit-test fixture; not a real event."
        }],
        "previous_event_ids": [previous] if previous else [],
    }
    if event_type == "CHANGE_APPLIED":
        item["change_summary"] = "Synthetic configuration change"
        item["configuration_delta"] = {"threshold": 0.8}
    else:
        item["test_id"] = "SYNTHETIC-TEST"
        item["result"] = result or "PASS"
        item["evidence_refs"] = ["fixture:retest-result"]
    return item


def test_empty_map_is_explicitly_insufficient_not_a_clean_state():
    result = build_iterative_map({"cartography_version": "1.1.0", "daily_seismic_records": [], "history_events": []})
    assert result["map_status"] == "NO_REGISTERED_POINTS"
    assert result["state_estimate"]["status"] == "INSUFFICIENT_EVIDENCE"
    assert result["node_count"] == 0
    assert result["edge_count"] == 0
    assert result["history_retention"] == "APPEND_ONLY_NO_AUTOMATIC_PRUNING"


def test_map_links_crashes_to_prior_points_events_and_tuning_candidate():
    first = incident("INC-001", "2026-01-01T00:00:00Z")
    second = incident("INC-002", "2026-02-01T00:00:00Z", prior="INC-001")
    change = event("CHANGE-001", "CHANGE_APPLIED", "2026-02-02T00:00:00Z", "INC-002")
    retest = event("RETEST-001", "RETEST", "2026-02-03T00:00:00Z", "INC-002", previous="CHANGE-001", result="PASS")
    candidate = {
        "candidate_id": "TUNE-001",
        "status": "CANDIDATE_REPLAY_REQUIRED",
        "component": "runtime-a",
        "parent_incident_ids": ["INC-002"],
        "change_event_id": "CHANGE-001",
        "retest_event_id": "RETEST-001",
        "configuration_delta": {"threshold": 0.8},
        "replay_status": "NOT_RUN",
        "semantic_status": "NOT_YET_VERIFIED",
    }
    matrix = {"cartography_version": "1.1.0", "daily_seismic_records": [first, second], "history_events": [change, retest]}
    result = build_iterative_map(matrix, [candidate], [])
    ids = {node["node_id"] for node in result["nodes"]}
    assert {"INCIDENT:INC-001", "INCIDENT:INC-002", "EVENT:CHANGE-001", "EVENT:RETEST-001", "TUNING:TUNE-001"} <= ids
    links = {(edge["source"], edge["target"], edge["relation"]) for edge in result["edges"]}
    assert ("INCIDENT:INC-001", "INCIDENT:INC-002", "PRECEDES") in links
    assert ("EVENT:CHANGE-001", "EVENT:RETEST-001", "PRECEDES") in links
    assert ("TUNING:TUNE-001", "EVENT:RETEST-001", "SUPPORTED_BY_RETEST") in links
    assert result["state_estimate"]["latest_crash_point"]["incident_id"] == "INC-002"
    assert result["state_estimate"]["incidents_without_latest_passing_retest"] == ["INC-001"]


def test_recurring_identical_failure_signature_is_mapped_without_forecasting():
    matrix = {
        "cartography_version": "1.1.0",
        "daily_seismic_records": [
            incident("INC-001", "2026-01-01T00:00:00Z", component="vitruvius-queue", state="signature=orchestrator_stages_gates"),
            incident("INC-002", "2026-01-02T00:00:00Z", prior="INC-001", component="vitruvius-queue", state="signature=orchestrator_stages_gates"),
            incident("INC-003", "2026-01-03T00:00:00Z", prior="INC-002", component="vitruvius-queue", state="signature=orchestrator_stages_gates"),
        ],
        "history_events": [],
    }
    result = build_iterative_map(matrix)
    state = result["state_estimate"]
    cluster = next(item for item in state["recurrence_clusters"] if item["component"] == "vitruvius-queue")
    assert state["status"] == "RECURRENCE_PATTERN_OBSERVED"
    assert state["recurring_unresolved_cluster_count"] == 1
    assert cluster["observation_count"] == 3
    assert cluster["incident_count_without_passing_retest"] == 3
    assert cluster["observed_intervals_hours"] == [24.0, 24.0]
    assert cluster["cluster_status"] == "RECURRENT_UNRESOLVED"
    assert state["trend_estimate"] == "RECURRENCE_OBSERVED_NO_COVERAGE_BASELINE_FOR_EXTRAPOLATION"


def test_map_hash_is_stable_for_identical_inputs():
    matrix = {"cartography_version": "1.1.0", "daily_seismic_records": [incident("INC-001", "2026-01-01T00:00:00Z")], "history_events": []}
    first = build_iterative_map(matrix)
    second = build_iterative_map(copy.deepcopy(matrix))
    assert first["map_sha256"] == second["map_sha256"]
    assert first == second
