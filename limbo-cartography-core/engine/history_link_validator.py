"""Append source-backed change/retest events and validate links without rewriting prior history."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "cartography" / "inbox" / "history_events"
MATRIX_PATH = ROOT / "cartography" / "reality_matrix.json"
INCIDENT_SCHEMA_PATH = ROOT / "schemas" / "deterministic_point_schema.json"
EVENT_SCHEMA_PATH = ROOT / "schemas" / "history_event_schema.json"


def _parse_time(value: str):
    from datetime import datetime
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def validate_history_data(matrix: dict[str, Any], incident_schema: dict, event_schema: dict) -> dict:
    errors: list[str] = []
    incidents = matrix.get("daily_seismic_records")
    events = matrix.get("history_events")
    if not isinstance(incidents, list):
        return {"status": "FAILED", "errors": ["MATRIX_RECORDS_NOT_LIST"], "incident_count": 0, "event_count": 0}
    if not isinstance(events, list):
        return {"status": "FAILED", "errors": ["MATRIX_HISTORY_EVENTS_NOT_LIST"], "incident_count": len(incidents), "event_count": 0}

    incident_validator = jsonschema.Draft7Validator(incident_schema, format_checker=jsonschema.FormatChecker())
    event_validator = jsonschema.Draft7Validator(event_schema, format_checker=jsonschema.FormatChecker())
    seen_incidents: set[str] = set()
    for index, incident in enumerate(incidents):
        for error in incident_validator.iter_errors(incident):
            errors.append(f"INCIDENT_{index}:{error.message}")
        incident_id = incident.get("coordinate_id") if isinstance(incident, dict) else None
        if not isinstance(incident_id, str) or not incident_id:
            continue
        if incident_id in seen_incidents:
            errors.append(f"DUPLICATE_INCIDENT_ID:{incident_id}")
            continue
        for prior_id in incident.get("prior_incident_ids", []):
            if prior_id not in seen_incidents:
                errors.append(f"NON_PRIOR_OR_DANGLING_INCIDENT_REF:{incident_id}:{prior_id}")
        seen_incidents.add(incident_id)

    seen_events: dict[str, dict] = {}
    for index, event in enumerate(events):
        for error in event_validator.iter_errors(event):
            errors.append(f"EVENT_{index}:{error.message}")
        if not isinstance(event, dict):
            continue
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            continue
        if event_id in seen_events:
            errors.append(f"DUPLICATE_EVENT_ID:{event_id}")
            continue
        for incident_id in event.get("affected_incident_ids", []):
            if incident_id not in seen_incidents:
                errors.append(f"DANGLING_EVENT_INCIDENT_REF:{event_id}:{incident_id}")
        for parent_id in event.get("previous_event_ids", []):
            parent = seen_events.get(parent_id)
            if parent is None:
                errors.append(f"NON_PRIOR_OR_DANGLING_EVENT_REF:{event_id}:{parent_id}")
                continue
            try:
                if _parse_time(event["timestamp_utc"]) < _parse_time(parent["timestamp_utc"]):
                    errors.append(f"EVENT_TIME_PRECEDES_PARENT:{event_id}:{parent_id}")
            except Exception:
                errors.append(f"INVALID_EVENT_TIME_LINK:{event_id}:{parent_id}")
        seen_events[event_id] = event

    if errors:
        status = "FAILED"
    elif not incidents and not events:
        status = "NO_INPUTS"
    elif incidents and not events:
        status = "NO_FOLLOW_UP_EVENTS"
    else:
        status = "STRUCTURALLY_VALID"
    return {
        "status": status,
        "incident_count": len(incidents),
        "event_count": len(events),
        "dangling_references": sum("DANGLING" in error or "NON_PRIOR" in error for error in errors),
        "errors": errors,
        "semantic_verification": False
    }


def ingest_history_events(matrix: dict[str, Any], incoming: list[tuple[str, dict]], incident_schema: dict, event_schema: dict) -> dict:
    incidents = matrix.get("daily_seismic_records", [])
    existing_events = matrix.get("history_events", [])
    incident_ids = {item.get("coordinate_id") for item in incidents}
    seen_event_ids = {item.get("event_id") for item in existing_events}
    event_validator = jsonschema.Draft7Validator(event_schema, format_checker=jsonschema.FormatChecker())
    accepted: list[dict] = []
    rejected: list[dict] = []
    parent_events = {item.get("event_id"): item for item in existing_events}

    for filename, item in sorted(incoming, key=lambda pair: (pair[1].get("timestamp_utc", ""), pair[0])):
        try:
            event_validator.validate(item)
            event_id = item["event_id"]
            if event_id in seen_event_ids:
                raise ValueError(f"DUPLICATE_EVENT_ID:{event_id}")
            unknown_incidents = sorted(set(item["affected_incident_ids"]) - incident_ids)
            if unknown_incidents:
                raise ValueError("UNKNOWN_INCIDENT_IDS:" + ",".join(unknown_incidents))
            unknown_parents = sorted(set(item["previous_event_ids"]) - set(parent_events))
            if unknown_parents:
                raise ValueError("UNKNOWN_PRIOR_EVENT_IDS:" + ",".join(unknown_parents))
            for parent_id in item["previous_event_ids"]:
                if _parse_time(item["timestamp_utc"]) < _parse_time(parent_events[parent_id]["timestamp_utc"]):
                    raise ValueError(f"EVENT_TIME_PRECEDES_PARENT:{parent_id}")
            seen_event_ids.add(event_id)
            accepted.append(item)
            parent_events[event_id] = item
        except Exception as exc:
            rejected.append({"file": filename, "reason": f"{type(exc).__name__}:{exc}"})

    if rejected:
        return {"status": "FAILED", "added": 0, "rejected": rejected, "history_preserved": True}
    if accepted:
        matrix["history_events"].extend(accepted)
    validation = validate_history_data(matrix, incident_schema, event_schema)
    if validation["status"] == "FAILED":
        return {"status": "FAILED", "added": 0, "rejected": validation["errors"], "history_preserved": True}
    if accepted:
        return {"status": "UPDATED", "added": len(accepted), "rejected": 0,
                "incident_count": len(incidents), "event_count": len(matrix["history_events"]),
                "history_preserved": True}
    return {"status": validation["status"] if validation["status"] != "STRUCTURALLY_VALID" else "NO_NEW_EVENTS",
            "added": 0, "rejected": 0, "incident_count": len(incidents),
            "event_count": len(existing_events), "history_preserved": True}


def run_history_validation() -> dict:
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    incident_schema = json.loads(INCIDENT_SCHEMA_PATH.read_text(encoding="utf-8"))
    event_schema = json.loads(EVENT_SCHEMA_PATH.read_text(encoding="utf-8"))
    incoming = []
    for path in sorted(INBOX.glob("*.json")):
        try:
            incoming.append((path.name, json.loads(path.read_text(encoding="utf-8"))))
        except Exception as exc:
            incoming.append((path.name, {"__parse_error__": f"{type(exc).__name__}:{exc}"}))

    parse_errors = [{"file": name, "reason": item["__parse_error__"]} for name, item in incoming if "__parse_error__" in item]
    if parse_errors:
        result = {"status": "FAILED", "added": 0, "rejected": parse_errors, "history_preserved": True}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result

    result = ingest_history_events(matrix, incoming, incident_schema, event_schema)
    if result["status"] == "UPDATED":
        MATRIX_PATH.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif result["status"] == "FAILED":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    else:
        result = validate_history_data(matrix, incident_schema, event_schema)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    result = run_history_validation()
    sys.exit(1 if result["status"] == "FAILED" else 0)
