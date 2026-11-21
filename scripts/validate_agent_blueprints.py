#!/usr/bin/env python3
"""Validate every AI231 agent blueprint against the canonical JSON Schema."""
from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-blueprint-v1.schema.json"
BLUEPRINT_DIR = ROOT / "agent_blueprints"


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    checked = 0
    for path in sorted(BLUEPRINT_DIR.rglob("*.json")):
        item = json.loads(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(item), key=lambda error: list(error.absolute_path))
        if errors:
            for error in errors:
                location = ".".join(str(part) for part in error.absolute_path) or "<root>"
                print(f"FAIL: {path}:{location}: {error.message}")
            raise SystemExit(1)

        portability = item["portability_contract"]
        if portability["portability_status"] == "Verified" and not portability.get("exit_test_evidence"):
            raise SystemExit(f"FAIL: {path}: portability marked Verified without exit-test evidence")
        checked += 1

    print(f"PASS: {SCHEMA_PATH.relative_to(ROOT)} is a valid Draft 2020-12 schema")
    print(f"PASS: {checked} committed agent blueprints validate against the exact schema")
    print("PASS: Verified portability requires explicit exit-test evidence")


if __name__ == "__main__":
    main()
