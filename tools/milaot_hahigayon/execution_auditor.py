#!/usr/bin/env python3
"""Independent compliance audit for the Gate 14 structural integration artifact."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "milaot-hahigayon/integration/INTERNAL_FRAMEWORK_CONTRACT.json"
SOURCE_PATH = ROOT / "milaot-hahigayon/sentences/שער-יד.md"
OUTPUT_PATH = ROOT / "artifacts/gate14_structural_integration.json"
REPORT_PATH = ROOT / "artifacts/gate14_execution_audit.json"

FORBIDDEN_OUTPUT_KEYS = {
    "interpretation",
    "explanation",
    "commentary",
    "external_theory",
    "summary"
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_quotes(text: str) -> dict[str, str]:
    import re
    result: dict[str, str] = {}
    current_id: str | None = None
    for line in text.splitlines():
        heading = re.match(r"^###\s+(T14-\d+)\s+[—–-]", line)
        if heading:
            current_id = heading.group(1)
            continue
        quote = re.match(r"^>\s?(.*)$", line)
        if quote and current_id:
            result[current_id] = quote.group(1)
            current_id = None
    return result


def audit(contract: dict[str, Any], source: str, output: dict[str, Any]) -> list[str]:
    findings: list[str] = []

    if output.get("target_gate") != 14:
        findings.append("TARGET_GATE_MISMATCH")
    if output.get("preceding_gates") != list(range(1, 14)):
        findings.append("PRECEDING_GATE_SCOPE_MISMATCH")

    for key in ("interpretation_added", "explanatory_commentary_added", "external_theory_added"):
        if output.get(key) is not False:
            findings.append(f"POLICY_VIOLATION:{key}")

    units = output.get("units")
    if not isinstance(units, list) or not units:
        findings.append("NO_SOURCE_UNITS")
        units = []

    expected = source_quotes(source)
    actual = {unit.get("unit_id"): unit.get("source_text") for unit in units}
    if actual != expected:
        findings.append("SOURCE_QUOTE_PRESERVATION_MISMATCH")

    if output.get("source_preserved") is not True:
        findings.append("SOURCE_PRESERVATION_NOT_ASSERTED")

    for unit in units:
        uid = unit.get("unit_id", "<missing-id>")
        if unit.get("source_status") == "VERIFIED":
            findings.append(f"UNSUPPORTED_SOURCE_VERIFICATION:{uid}")
        if unit.get("link_status") == "LINKED":
            for link in unit.get("structural_links", []):
                if not all(link.get(k) for k in (
                    "source_unit_id", "target_unit_id", "relationship_type", "evidence_reference"
                )):
                    findings.append(f"LINK_WITHOUT_EVIDENCE:{uid}")
        elif unit.get("link_status") not in {"UNRESOLVED", "BLOCKED"}:
            findings.append(f"INVALID_LINK_STATUS:{uid}")

    def scan_keys(value: Any, path: str = "$") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in FORBIDDEN_OUTPUT_KEYS:
                    findings.append(f"FORBIDDEN_FIELD:{path}.{key}")
                scan_keys(child, f"{path}.{key}")
        elif isinstance(value, list):
            for i, child in enumerate(value):
                scan_keys(child, f"{path}[{i}]")

    scan_keys(output)
    return sorted(set(findings))


def main() -> int:
    contract = load_json(CONTRACT_PATH)
    output = load_json(OUTPUT_PATH)
    source = SOURCE_PATH.read_text(encoding="utf-8")
    findings = audit(contract, source, output)

    report = {
        "audit_status": "PASS" if not findings else "FAIL",
        "findings": findings,
        "integration_status": output.get("status"),
        "coverage_status": output.get("coverage", {}).get("coverage_status"),
        "units_audited": len(output.get("units", [])),
        "verification_boundary": (
            "Audit PASS confirms only the tested invariants. It does not prove "
            "semantic integration or source correctness beyond the checks performed."
        )
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["audit_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
