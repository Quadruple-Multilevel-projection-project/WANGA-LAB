"""Immutable event-set state for local ARK-Swarm runs.

The event-set merge is a small grow-only set (G-Set) CRDT demonstration. It is
not a peer-to-peer transport implementation and does not synchronize across
machines by itself.
"""
from __future__ import annotations
import hashlib
import json
from typing import Any, Mapping


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def make_event(*, cycle_id: str, agent_id: str, event_type: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    if not all(isinstance(x, str) and x.strip() for x in (cycle_id, agent_id, event_type)):
        raise ValueError("cycle_id, agent_id, and event_type must be non-empty strings")
    if not isinstance(payload, Mapping):
        raise ValueError("payload must be an object")
    core = {"cycle_id": cycle_id, "agent_id": agent_id, "event_type": event_type, "payload": dict(payload)}
    return {"event_id": "EV-" + digest(core)[:24], **core}


def merge_event_sets(*event_sets: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Merge event sets with idempotent, commutative union semantics."""
    merged: dict[str, dict[str, Any]] = {}
    for event_set in event_sets:
        if not isinstance(event_set, list):
            raise ValueError("each event set must be a list")
        for item in event_set:
            if not isinstance(item, Mapping) or not isinstance(item.get("event_id"), str):
                raise ValueError("each event must contain an event_id")
            event = dict(item)
            event_id = event["event_id"]
            prior = merged.get(event_id)
            if prior is not None and canonical_json(prior) != canonical_json(event):
                raise ValueError(f"event ID collision with different payload: {event_id}")
            merged[event_id] = event
    events = [merged[key] for key in sorted(merged)]
    return {
        "schema_version": "ark-swarm-gset/1.0",
        "merge_semantics": "GROW_ONLY_SET_UNION",
        "event_count": len(events),
        "events": events,
        "event_set_sha256": digest(events),
        "network_sync_status": "LOCAL_ONLY_P2P_NOT_IMPLEMENTED",
    }


def validation_credit(role_results: list[Mapping[str, Any]]) -> dict[str, Any]:
    """Compute shared software-validation credit from explicit test outcomes.

    This is a test metric, not a biological dopamine signal or learning update.
    """
    if not role_results:
        return {"status": "NO_RESULTS", "passed": 0, "total": 0, "score": 0.0}
    passed = sum(1 for role in role_results if role.get("passed") is True)
    total = len(role_results)
    return {
        "status": "MEASURED_TEST_CREDIT_NOT_REINFORCEMENT_LEARNING",
        "passed": passed,
        "total": total,
        "score": round(passed / total, 6),
        "policy": "Only explicit role/test outcomes contribute. No model weights are updated.",
    }
