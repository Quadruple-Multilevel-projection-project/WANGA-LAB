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
    runtime = item.get("runtime", {})
    if runtime:
        if runtime.get("isolation_required") is not True or runtime.get("network_egress") is not False:
            fail(f"{source}: runtime must require isolation and deny network egress")
        runtime_required = {
            "runtime_status", "backend_configuration", "environment",
            "invocation_log_refs", "isolation_evidence_refs",
            "network_egress_policy_ref", "acceptance_test_refs",
        }
        missing_runtime = runtime_required - runtime.keys()
        if missing_runtime:
            fail(f"{source}: runtime missing evidence fields: {', '.join(sorted(missing_runtime))}")
        if runtime.get("runtime_status") not in {
            "NOT_CONFIGURED", "CONFIGURED_NOT_INVOKED", "INVOKED_UNVERIFIED",
            "TESTED", "ACTIVE", "BLOCKED",
        }:
            fail(f"{source}: invalid runtime_status")
        audit = item.get("audit_contract")
        rollback = item.get("rollback")
        if not isinstance(audit, dict) or audit.get("hash_algorithm") != "SHA-256":
            fail(f"{source}: runtime blueprint requires a SHA-256 audit_contract")
        required_audit = {
            "timestamp_iso8601", "contract_start_time", "action_id", "repository",
            "branch", "artifact_identifiers", "commit_identifiers", "sha256",
        }
        if not required_audit.issubset(set(audit.get("required_fields", []))):
            fail(f"{source}: audit_contract is missing required signature fields")
        if not isinstance(rollback, dict) or len(rollback.get("procedure", [])) < 3:
            fail(f"{source}: runtime blueprint requires a complete rollback procedure")
        if item["status"] in {"tested", "active"}:
            required_evidence = (
                runtime.get("runtime_status") in {"TESTED", "ACTIVE"}
                and runtime.get("backend_configuration") != "NOT_CONFIGURED"
                and runtime.get("environment") != "NOT_CONFIGURED"
                and bool(runtime.get("invocation_log_refs"))
                and bool(runtime.get("isolation_evidence_refs"))
                and runtime.get("network_egress_policy_ref") != "NOT_CONFIGURED"
                and bool(runtime.get("acceptance_test_refs"))
            )
            if not required_evidence:
                fail(f"{source}: tested/active status lacks exact runtime evidence")
        elif runtime.get("runtime_status") in {"TESTED", "ACTIVE"}:
            fail(f"{source}: runtime evidence cannot be promoted while blueprint status is draft/blocked")


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
