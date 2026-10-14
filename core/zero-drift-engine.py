#!/usr/bin/env python3
"""Validate a bounded drift-contract JSON record.

This utility checks record shape and status consistency only. It does not detect
all possible model drift, prove semantic truth, or guarantee zero drift.

Usage:
    python core/zero-drift-engine.py path/to/record.json

Expected fields:
    schema_version, baseline_id, observed_id, checks, declared_status

Each check: { "id": str, "baseline": any, "observed": any, "scope": str }
Declared status: NO_DECLARED_CHANGE, DECLARED_CHANGE, or INSUFFICIENT_EVIDENCE.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = {
    "NO_DECLARED_CHANGE",
    "DECLARED_CHANGE",
    "INSUFFICIENT_EVIDENCE",
}


def evaluate(record: dict[str, Any]) -> dict[str, Any]:
    required = {"schema_version", "baseline_id", "observed_id", "checks", "declared_status"}
    missing = sorted(required - record.keys())
    errors: list[str] = []
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    status = record.get("declared_status")
    if status not in ALLOWED_STATUSES:
        errors.append("declared_status is not an allowed value")
    checks = record.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be a list")
        checks = []
    seen: set[str] = set()
    changed: list[str] = []
    unknown: list[str] = []
    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"checks[{index}] must be an object")
            continue
        check_id = check.get("id")
        if not isinstance(check_id, str) or not check_id:
            errors.append(f"checks[{index}].id must be a non-empty string")
            continue
        if check_id in seen:
            errors.append(f"duplicate check id: {check_id}")
        seen.add(check_id)
        if not isinstance(check.get("scope"), str) or not check["scope"]:
            errors.append(f"checks[{index}].scope must be a non-empty string")
        if "baseline" not in check or "observed" not in check:
            unknown.append(check_id)
        elif check["baseline"] != check["observed"]:
            changed.append(check_id)
    if unknown and status != "INSUFFICIENT_EVIDENCE":
        errors.append("checks with missing values require INSUFFICIENT_EVIDENCE")
    if changed and status == "NO_DECLARED_CHANGE":
        errors.append("observed changes conflict with NO_DECLARED_CHANGE")
    if not changed and not unknown and status == "DECLARED_CHANGE":
        errors.append("DECLARED_CHANGE has no differing checks")
    return {
        "schema_version": record.get("schema_version"),
        "baseline_id": record.get("baseline_id"),
        "observed_id": record.get("observed_id"),
        "status": "FAILED" if errors else "STRUCTURALLY_VALID",
        "declared_status": status,
        "changed_check_ids": changed,
        "insufficient_check_ids": unknown,
        "errors": errors,
        "scope_note": (
            "Structural comparison of supplied fields only; not a guarantee of zero drift "
            "and not semantic verification."
        ),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} path/to/record.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAILED", "errors": [str(exc)]}, ensure_ascii=False))
        return 2
    if not isinstance(record, dict):
        print(json.dumps({"status": "FAILED", "errors": ["top-level JSON must be an object"]}, ensure_ascii=False))
        return 2
    result = evaluate(record)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["status"] == "STRUCTURALLY_VALID" else 1


if __name__ == "__main__":
    raise SystemExit(main())
