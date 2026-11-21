#!/usr/bin/env python3
"""Verify the AI231 Agent Blueprint contract using only the Python standard library.

This checks the canonical schema, the existing agent registry's basic structure,
and every committed JSON blueprint under agent_blueprints/. It deliberately does
not claim runtime, deployment, or model verification.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-blueprint-v1.schema.json"
REGISTRY_PATH = ROOT / "logic_wiki" / "data" / "agent_registry.json"
BLUEPRINT_DIR = ROOT / "agent_blueprints"

ALLOWED_PERMISSIONS = {
    "generate_text",
    "analyze_supplied_data",
    "read_public_web_content",
    "create_internal_task",
    "write_internal_report",
    "read_agent_registry",
}
REQUIRED = {
    "id", "name", "version", "status", "mission", "system_instructions",
    "capabilities", "tool_permissions", "input_contract", "output_contract",
    "boundaries", "acceptance_tests", "failure_behavior", "provenance",
    "system_requirements", "portability_contract",
}
STATUSES = {
    "draft", "validated", "approved", "materialized",
    "tested", "active", "blocked", "deprecated",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def validate_blueprint(item: object, source: Path) -> None:
    if not isinstance(item, dict):
        fail(f"{source}: blueprint must be a JSON object")
    missing = REQUIRED - item.keys()
    if missing:
        fail(f"{source}: missing fields: {', '.join(sorted(missing))}")
    if item["status"] not in STATUSES:
        fail(f"{source}: invalid lifecycle status")
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", str(item["version"])):
        fail(f"{source}: version must be semantic x.y.z")
    if not isinstance(item["capabilities"], list) or len(item["capabilities"]) < 2:
        fail(f"{source}: at least two capabilities are required")
    permissions = item["tool_permissions"]
    if not isinstance(permissions, list) or not permissions:
        fail(f"{source}: at least one tool permission is required")
    unknown = set(permissions) - ALLOWED_PERMISSIONS
    if unknown:
        fail(f"{source}: permissions outside allowlist: {', '.join(sorted(unknown))}")
    if not isinstance(item["boundaries"], list) or len(item["boundaries"]) < 3:
        fail(f"{source}: at least three boundaries are required")
    if not isinstance(item["acceptance_tests"], list) or len(item["acceptance_tests"]) < 3:
        fail(f"{source}: at least three acceptance tests are required")
    if not isinstance(item["input_contract"], dict) or len(item["input_contract"].get("requirements", [])) < 2:
        fail(f"{source}: input contract requires at least two requirements")
    if not isinstance(item["output_contract"], dict):
        fail(f"{source}: output_contract must be an object")
    if not isinstance(item["provenance"], dict) or not item["provenance"].get("created_at") or not item["provenance"].get("created_by"):
        fail(f"{source}: provenance must include created_at and created_by")
    system_requirements = item.get("system_requirements")
    if not isinstance(system_requirements, list) or "SYS-PORTABILITY-001" not in system_requirements:
        fail(f"{source}: SYS-PORTABILITY-001 must be declared")
    portability = item.get("portability_contract")
    required_portability = {
        "provider_dependencies", "model_adapter_interface", "alternative_providers_or_fallback",
        "data_export_format", "owner_controlled_source_location", "deployment_reproduction_steps",
        "secrets_location_and_rotation", "exit_test", "portability_status",
    }
    if not isinstance(portability, dict):
        fail(f"{source}: portability_contract must be an object")
    missing_portability = required_portability - portability.keys()
    if missing_portability:
        fail(f"{source}: missing portability fields: {', '.join(sorted(missing_portability))}")
    if portability.get("portability_status") == "Verified" and not portability.get("exit_test_evidence"):
        fail(f"{source}: portability cannot be Verified without exit-test evidence")
    runtime = item.get("runtime", {})
    if runtime and (runtime.get("isolation_required") is not True or runtime.get("network_egress") is not False):
        fail(f"{source}: runtime must require isolation and deny network egress")


def main() -> None:
    if not SCHEMA_PATH.is_file():
        fail("canonical blueprint schema is missing")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if schema.get("title") != "AI231 Agent Blueprint v1":
        fail("unexpected schema title")
    if set(schema.get("required", [])) != REQUIRED:
        fail("schema required-field contract does not match verifier")
    if not REGISTRY_PATH.is_file():
        fail("existing agent registry is missing")
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if not isinstance(registry.get("agents"), list):
        fail("existing agent registry must contain an agents array")
    ids = [agent.get("id") for agent in registry["agents"] if isinstance(agent, dict)]
    if len(ids) != len(set(ids)):
        fail("existing agent registry contains duplicate agent IDs")

    checked = 0
    if BLUEPRINT_DIR.exists():
        for path in sorted(BLUEPRINT_DIR.rglob("*.json")):
            validate_blueprint(json.loads(path.read_text(encoding="utf-8")), path)
            checked += 1

    print("PASS: AI231 agent blueprint contract")
    print(f"PASS: canonical schema fields ({len(REQUIRED)})")
    print(f"PASS: existing agent registry ({len(ids)} entries; unique IDs)")
    print(f"PASS: committed blueprints ({checked})")
    print("NOTE: runtime materialization and deployment are not verified by this script")


if __name__ == "__main__":
    main()
