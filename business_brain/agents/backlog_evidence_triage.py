"""Deterministic, read-only triage for supplied GitHub issue snapshots.

This module performs no network access and never mutates GitHub or another system.
It returns stale-item, missing-priority, unassigned-item, and possible-duplicate
findings for a human or supervisor to review.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from itertools import combinations
from typing import Any, Mapping

RULES_VERSION = "1.0.0"
PRIORITY_LABELS = {"P0", "P1", "P2", "P3"}
STOP_WORDS = {"a", "an", "and", "for", "of", "the", "to", "with"}


def _parse_timestamp(value: str) -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("timestamp must be a non-empty ISO 8601 string")
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"invalid ISO 8601 timestamp: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _label_names(labels: Any) -> set[str]:
    if labels is None:
        return set()
    if not isinstance(labels, list):
        raise ValueError("issue labels must be a list")
    names: set[str] = set()
    for label in labels:
        if isinstance(label, str):
            names.add(label.strip().upper())
        elif isinstance(label, Mapping) and isinstance(label.get("name"), str):
            names.add(label["name"].strip().upper())
        else:
            raise ValueError("each label must be a string or an object with a name")
    return names


def _has_assignee(assignees: Any) -> bool:
    if assignees is None:
        return False
    if not isinstance(assignees, list):
        raise ValueError("issue assignees must be a list")
    return any(bool(item) for item in assignees)


def _title_tokens(title: str) -> set[str]:
    without_prefix = re.sub(r"^\\s*\\[[^\\]]+\\]\\s*", "", title)
    return {token for token in re.findall(r"[a-z0-9]+", without_prefix.lower()) if token not in STOP_WORDS}


def _issue_number(issue: Mapping[str, Any]) -> str:
    return str(issue["number"])


def triage_issues(
    snapshot: Mapping[str, Any],
    as_of: str,
    stale_after_days: int = 7,
    duplicate_threshold: float = 0.5,
) -> dict[str, Any]:
    """Return a deterministic report for a supplied issue snapshot."""
    if not isinstance(snapshot, Mapping):
        raise ValueError("snapshot must be an object")
    issues = snapshot.get("issues")
    if not isinstance(issues, list):
        raise ValueError("snapshot.issues must be a list")
    if stale_after_days < 0:
        raise ValueError("stale_after_days must be non-negative")
    if not 0.0 <= duplicate_threshold <= 1.0:
        raise ValueError("duplicate_threshold must be between 0 and 1")

    as_of_dt = _parse_timestamp(as_of)
    cutoff = as_of_dt - timedelta(days=stale_after_days)
    normalized: list[dict[str, Any]] = []
    for index, issue in enumerate(issues):
        if not isinstance(issue, Mapping):
            raise ValueError(f"issue at index {index} must be an object")
        for required in ("number", "title", "state", "updated_at"):
            if required not in issue:
                raise ValueError(f"issue at index {index} is missing {required}")
        if not isinstance(issue["title"], str) or not issue["title"].strip():
            raise ValueError(f"issue at index {index} has an invalid title")
        state = str(issue["state"]).lower()
        if state not in {"open", "closed"}:
            raise ValueError(f"issue at index {index} has unsupported state {state}")
        updated = _parse_timestamp(issue["updated_at"])
        labels = _label_names(issue.get("labels", []))
        assignees = issue.get("assignees", [])
        normalized.append({
            "number": _issue_number(issue),
            "title": issue["title"].strip(),
            "state": state,
            "updated_at": updated,
            "labels": labels,
            "has_assignee": _has_assignee(assignees),
            "url": issue.get("url"),
            "tokens": _title_tokens(issue["title"]),
        })

    open_issues = [item for item in normalized if item["state"] == "open"]
    stale = sorted(
        (item for item in open_issues if item["updated_at"] < cutoff),
        key=lambda item: int(item["number"]) if item["number"].isdigit() else item["number"],
    )
    missing_priority = sorted(
        item["number"] for item in open_issues
        if not (item["labels"] & PRIORITY_LABELS)
    )
    unassigned = sorted(
        item["number"] for item in open_issues if not item["has_assignee"]
    )

    duplicates: list[dict[str, Any]] = []
    for left, right in combinations(open_issues, 2):
        shared = left["tokens"] & right["tokens"]
        union = left["tokens"] | right["tokens"]
        similarity = len(shared) / len(union) if union else 0.0
        if len(shared) >= 3 and similarity >= duplicate_threshold:
            duplicates.append({
                "issue_numbers": sorted([left["number"], right["number"]]),
                "titles": [left["title"], right["title"]],
                "shared_tokens": sorted(shared),
                "title_jaccard": round(similarity, 4),
                "review_required": True,
                "automatic_merge": False,
            })

    return {
        "agent_id": "agent-backlog-evidence-triage",
        "rules_version": RULES_VERSION,
        "as_of": as_of,
        "snapshot_id": snapshot.get("snapshot_id", "UNSPECIFIED"),
        "source_commit": snapshot.get("source_commit", "UNSPECIFIED"),
        "source_ref": snapshot.get("source_ref", "UNSPECIFIED"),
        "input_issue_count": len(normalized),
        "open_issue_count": len(open_issues),
        "stale_after_days": stale_after_days,
        "stale_open_issue_numbers": [item["number"] for item in stale],
        "missing_priority_issue_numbers": missing_priority,
        "unassigned_open_issue_numbers": unassigned,
        "possible_duplicate_pairs": duplicates,
        "decision_boundary": "READ_ONLY_REVIEW_REQUIRED_NO_AUTOMATIC_GITHUB_MUTATIONS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Triage a supplied AI231 GitHub issue snapshot")
    parser.add_argument("--as-of", required=True, help="ISO 8601 timestamp used for stale-item checks")
    parser.add_argument("--stale-after-days", type=int, default=7)
    parser.add_argument("--duplicate-threshold", type=float, default=0.5)
    args = parser.parse_args()
    try:
        snapshot = json.load(sys.stdin)
        report = triage_issues(
            snapshot,
            as_of=args.as_of,
            stale_after_days=args.stale_after_days,
            duplicate_threshold=args.duplicate_threshold,
        )
    except (ValueError, json.JSONDecodeError) as exc:
        json.dump({"status": "BLOCKED", "error": str(exc)}, sys.stdout, indent=2)
        sys.stdout.write("\\n")
        return 2
    json.dump(report, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
