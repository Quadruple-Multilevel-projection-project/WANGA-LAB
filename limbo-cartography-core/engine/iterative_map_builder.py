"""Build a deterministic, cumulative graph and last-observation estimate from Limbo records."""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "cartography" / "reality_matrix.json"
OUTPUT_PATH = ROOT / "cartography" / "iterative_crash_map.json"
TUNING_DIR = ROOT / "cartography" / "tuning_candidates"
BUNDLE_DIR = ROOT / "cartography" / "logic_bundles"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json_files(directory: Path, identity_field: str) -> list[dict]:
    items = []
    if not directory.exists():
        return items
    for path in sorted(directory.glob("*.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(item, dict) and isinstance(item.get(identity_field), str):
            items.append(item)
    return items


def build_iterative_map(
    matrix: dict[str, Any],
    tuning_candidates: list[dict] | None = None,
    logic_bundles: list[dict] | None = None,
) -> dict:
    """Pure builder: same matrix and candidate inputs yield the same map hash."""
    tuning_candidates = tuning_candidates or []
    logic_bundles = logic_bundles or []
    incidents = matrix.get("daily_seismic_records", [])
    events = matrix.get("history_events", [])
    nodes: list[dict] = []
    edges: list[dict] = []
    node_ids: set[str] = set()

    def add_node(node: dict) -> None:
        if node["node_id"] in node_ids:
            raise ValueError(f"DUPLICATE_MAP_NODE_ID:{node['node_id']}")
        node_ids.add(node["node_id"])
        nodes.append(node)

    def add_edge(source: str, target: str, relation: str, evidence_refs: list[str] | None = None) -> None:
        basis = {"source": source, "target": target, "relation": relation}
        if source not in node_ids or target not in node_ids:
            raise ValueError(f"DANGLING_MAP_EDGE:{source}:{relation}:{target}")
        edge = {
            "edge_id": "EDGE-" + sha256_json(basis)[:20],
            "source": source,
            "target": target,
            "relation": relation,
            "evidence_refs": sorted(set(evidence_refs or [])),
            "epistemic_status": "RECORDED_LINK",
        }
        edges.append(edge)

    incident_ids = {item["coordinate_id"] for item in incidents}
    event_ids = {item["event_id"] for item in events}
    latest_retest_by_incident: dict[str, dict] = {}

    for event in sorted(events, key=lambda item: (item.get("timestamp_utc", ""), item.get("event_id", ""))):
        if event.get("event_type") == "RETEST":
            for incident_id in event.get("affected_incident_ids", []):
                latest_retest_by_incident[incident_id] = event

    incident_assessments = []
    for incident in sorted(incidents, key=lambda item: (item.get("timestamp_utc", ""), item.get("coordinate_id", ""))):
        incident_id = incident["coordinate_id"]
        node_id = f"INCIDENT:{incident_id}"
        add_node({
            "node_id": node_id,
            "node_type": "CRASH_POINT",
            "record_id": incident_id,
            "timestamp_utc": incident.get("timestamp_utc"),
            "component": incident.get("affected_component"),
            "status": incident.get("status"),
            "observed_state": incident.get("observed_state"),
            "source_refs": sorted(set(incident.get("source_refs", []))),
            "source_locators": [
                {
                    "source_uri": item.get("source_uri"),
                    "source_version": item.get("source_version"),
                    "source_sha256": item.get("source_sha256"),
                    "exact_locator": item.get("exact_locator"),
                    "permission_scope": item.get("permission_scope"),
                }
                for item in incident.get("source_evidence", [])
            ],
        })
        retest = latest_retest_by_incident.get(incident_id)
        retest_result = retest.get("result") if retest else None
        assessment = {
            "incident_id": incident_id,
            "latest_retest_event_id": retest.get("event_id") if retest else None,
            "latest_retest_result": retest_result,
            "follow_up_state": (
                "NO_RETEST_RECORDED" if retest is None else
                "PASS_RECORDED" if retest_result == "PASS" else
                "FAIL_RECORDED" if retest_result == "FAIL" else
                "RETEST_NOT_PASSED"
            ),
        }
        incident_assessments.append(assessment)

    for incident in incidents:
        for prior_id in incident.get("prior_incident_ids", []):
            if prior_id in incident_ids:
                add_edge(f"INCIDENT:{prior_id}", f"INCIDENT:{incident['coordinate_id']}", "PRECEDES", incident.get("source_refs", []))

    for event in sorted(events, key=lambda item: (item.get("timestamp_utc", ""), item.get("event_id", ""))):
        event_id = event["event_id"]
        node_id = f"EVENT:{event_id}"
        add_node({
            "node_id": node_id,
            "node_type": "HISTORY_EVENT",
            "record_id": event_id,
            "event_type": event.get("event_type"),
            "timestamp_utc": event.get("timestamp_utc"),
            "component": event.get("component"),
            "result": event.get("result"),
            "source_refs": sorted({e.get("source_uri") for e in event.get("source_evidence", []) if e.get("source_uri")}),
        })
    for event in events:
        event_id = event["event_id"]
        node_id = f"EVENT:{event_id}"
        for incident_id in event.get("affected_incident_ids", []):
            if incident_id in incident_ids:
                add_edge(node_id, f"INCIDENT:{incident_id}", "AFFECTS_INCIDENT", event.get("evidence_refs", []))
        for previous_id in event.get("previous_event_ids", []):
            if previous_id in event_ids:
                add_edge(f"EVENT:{previous_id}", node_id, "PRECEDES", event.get("evidence_refs", []))

    for candidate in sorted(tuning_candidates, key=lambda item: item.get("candidate_id", "")):
        candidate_id = candidate["candidate_id"]
        node_id = f"TUNING:{candidate_id}"
        add_node({
            "node_id": node_id,
            "node_type": "TUNING_CONFIGURATION_CANDIDATE",
            "record_id": candidate_id,
            "status": candidate.get("status", "UNKNOWN"),
            "component": candidate.get("component"),
            "replay_status": candidate.get("replay_status", "NOT_RECORDED"),
            "semantic_status": candidate.get("semantic_status", "NOT_RECORDED"),
            "configuration_delta": candidate.get("configuration_delta", {}),
            "parent_incident_ids": sorted(candidate.get("parent_incident_ids", [])),
        })
        change_id = candidate.get("change_event_id")
        retest_id = candidate.get("retest_event_id")
        if change_id in event_ids:
            add_edge(node_id, f"EVENT:{change_id}", "DERIVED_FROM_CHANGE")
        if retest_id in event_ids:
            add_edge(node_id, f"EVENT:{retest_id}", "SUPPORTED_BY_RETEST")
        for incident_id in candidate.get("parent_incident_ids", []):
            if incident_id in incident_ids:
                add_edge(node_id, f"INCIDENT:{incident_id}", "APPLIES_TO_INCIDENT")

    for bundle in sorted(logic_bundles, key=lambda item: item.get("bundle_id", "")):
        bundle_id = bundle["bundle_id"]
        node_id = f"BUNDLE:{bundle_id}"
        add_node({
            "node_id": node_id,
            "node_type": "LOGIC_CONFIGURATION_CANDIDATE",
            "record_id": bundle_id,
            "status": bundle.get("status", "DRAFT_UNVERIFIED"),
            "version": bundle.get("version"),
            "source_refs": sorted(set(bundle.get("source_refs", []))),
            "source_candidate_sha256": bundle.get("source_candidate_sha256"),
            "verification": bundle.get("verification", {"verified": False}),
        })
        bundle_sources = set(bundle.get("source_refs", []))
        for incident in incidents:
            if bundle_sources.intersection(incident.get("source_refs", [])):
                add_edge(node_id, f"INCIDENT:{incident['coordinate_id']}", "SHARES_SOURCE_REFERENCE")

    nodes.sort(key=lambda item: item["node_id"])
    edges.sort(key=lambda item: (item["source"], item["relation"], item["target"], item["edge_id"]))
    all_times = [
        item.get("timestamp_utc")
        for item in incidents + events
        if isinstance(item.get("timestamp_utc"), str)
    ]
    as_of = max(all_times) if all_times else None
    latest_incident = max(incidents, key=lambda item: (item.get("timestamp_utc", ""), item.get("coordinate_id", "")), default=None)

    event_counts = Counter(item.get("result", "NOT_APPLICABLE") for item in events if item.get("event_type") == "RETEST")
    unresolved = [item["incident_id"] for item in incident_assessments if item["follow_up_state"] != "PASS_RECORDED"]
    components = sorted({item.get("affected_component") for item in incidents if item.get("affected_component")})
    state_estimate = {
        "status": "INSUFFICIENT_EVIDENCE" if not incidents else "LAST_OBSERVATION_ONLY",
        "as_of_latest_recorded_time_utc": as_of,
        "latest_crash_point": None if latest_incident is None else {
            "incident_id": latest_incident.get("coordinate_id"),
            "timestamp_utc": latest_incident.get("timestamp_utc"),
            "component": latest_incident.get("affected_component"),
            "observed_state": latest_incident.get("observed_state"),
            "source_refs": sorted(set(latest_incident.get("source_refs", []))),
        },
        "registered_incident_count": len(incidents),
        "registered_history_event_count": len(events),
        "affected_components": components,
        "retest_result_counts": dict(sorted(event_counts.items())),
        "incidents_without_latest_passing_retest": sorted(unresolved),
        "registered_incident_follow_up": incident_assessments,
        "trend_estimate": "NOT_ESTIMABLE_WITHOUT_SOURCE_COVERAGE_METADATA",
        "interpretation_boundary": (
            "This is a description of the latest registered observation and recorded follow-ups, "
            "not a verified assessment of the whole system or a forecast."
        ),
    }

    source_basis = {
        "matrix_version": matrix.get("cartography_version"),
        "matrix_sha256": sha256_json(matrix),
        "nodes": nodes,
        "edges": edges,
        "state_estimate": state_estimate,
        "monitoring_horizon_years": 20,
        "history_retention": "APPEND_ONLY_NO_AUTOMATIC_PRUNING",
    }
    result = {
        "map_version": "1.0.0",
        "map_status": "NO_REGISTERED_POINTS" if not incidents and not events else "BUILT_FROM_REGISTERED_RECORDS",
        "monitoring_horizon_years": 20,
        "history_retention": "APPEND_ONLY_NO_AUTOMATIC_PRUNING",
        "source_matrix_version": matrix.get("cartography_version"),
        "source_matrix_sha256": source_basis["matrix_sha256"],
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": nodes,
        "edges": edges,
        "state_estimate": state_estimate,
        "map_sha256": sha256_json(source_basis),
    }
    return result


def build_and_write_map() -> dict:
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    tuning = load_json_files(TUNING_DIR, "candidate_id")
    bundles = load_json_files(BUNDLE_DIR, "bundle_id")
    result = build_iterative_map(matrix, tuning, bundles)
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["map_status"],
        "node_count": result["node_count"],
        "edge_count": result["edge_count"],
        "map_sha256": result["map_sha256"],
        "state_estimate": result["state_estimate"]["status"],
        "output": str(OUTPUT_PATH.relative_to(ROOT)),
        "history_retention": result["history_retention"],
    }, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    try:
        build_and_write_map()
    except Exception as exc:
        print(json.dumps({"status": "FAILED", "error": f"{type(exc).__name__}:{exc}"}, ensure_ascii=False, indent=2))
        raise SystemExit(1)
