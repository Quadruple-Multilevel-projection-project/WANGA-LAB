#!/usr/bin/env python3
"""Independent compliance audit for the Gate 14 structural integration artifact."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = ROOT / "milaot-hahigayon/integration/INTERNAL_FRAMEWORK_CONTRACT.json"
SOURCE_PATH = ROOT / "milaot-hahigayon/sentences/שער-יד.md"
SOURCE_SNAPSHOT_PATH = ROOT / "milaot-hahigayon/source/milot_hahigayon_d1106d9a.html"
BOOK_REGISTRY_PATH = ROOT / "artifacts/book_sentence_registry.json"
OUTPUT_PATH = ROOT / "artifacts/gate14_structural_integration.json"
REPORT_PATH = ROOT / "artifacts/gate14_execution_audit.json"
LINKS_PATH = ROOT / "milaot-hahigayon/integration/explicit_links.json"
PRECEDING_SOURCE_REGISTRY_PATH = ROOT / "milaot-hahigayon/integration/gates_1_8_source_registry.json"

SOURCE_COMMIT = "d1106d9a66528dc3e39cf1ea0732782927d9f678"
FORBIDDEN_OUTPUT_KEYS = {"interpretation", "explanation", "commentary", "external_theory", "summary"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def source_quotes(text: str) -> dict[str, str]:
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


def known_target_ids(registry: dict[str, Any]) -> set[str]:
    ids = {item.get("target_unit_id") for item in registry.get("gates", [])}
    paths = {
        ROOT / "milaot-hahigayon/sentences/שער-ט.md": r"\bT9-\d{3}\b",
        ROOT / "milaot-hahigayon/sentences/שער-י.md": r"\bT10-\d{3}\b",
        ROOT / "milaot-hahigayon/sentences/שער-יא.md": r"\bT11-\d{3}\b",
        ROOT / "milaot-hahigayon/sentences/שער-יב.md": r"\bT12-\d{3}\b",
        ROOT / "docs/LOGIC/MILOT_HIGAYON_GATE_13_SENTENCE_REGISTRY.md": r"\b13\.\d{3}\b",
    }
    for path, pattern in paths.items():
        if path.exists():
            ids.update(re.findall(pattern, path.read_text(encoding="utf-8")))
    return {value for value in ids if isinstance(value, str) and value}



def normalize_canonical_gate14(raw: str) -> tuple[str, int]:
    headings = list(re.finditer(r"<h3[^>]*>\s*שער\s*([^<]+)</h3>", raw, re.I))
    if len(headings) != 14:
        return "", len(headings)
    fragment = raw[headings[13].end():]
    fragment = re.sub(
        r'<sup class="footnote-marker">[\s\S]*?</sup>\s*<i class="footnote">[\s\S]*?</i>',
        "", fragment
    )
    fragment = re.sub(r"<[^>]+>", "", fragment)
    fragment = html.unescape(fragment).replace("\xa0", " ")
    return re.sub(r"\s+", " ", fragment).strip(), len(headings)


def audit(contract: dict[str, Any], source: str, output: dict[str, Any],
          manifest: list[dict[str, Any]], registry: dict[str, Any],
          canonical_source: str, canonical_registry: dict[str, Any]) -> list[str]:
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

    canonical_text, heading_count = normalize_canonical_gate14(canonical_source)
    canonical_chapters = canonical_registry.get("chapters", [])
    canonical_gate14 = canonical_chapters[13] if len(canonical_chapters) >= 14 else {}
    if heading_count != 14:
        findings.append("CANONICAL_SOURCE_HEADING_COUNT_MISMATCH")
    if canonical_registry.get("source", {}).get("commit") != SOURCE_COMMIT:
        findings.append("CANONICAL_REGISTRY_SOURCE_COMMIT_MISMATCH")
    if canonical_gate14.get("normalized_source_text") != canonical_text:
        findings.append("CANONICAL_GATE14_SOURCE_COVERAGE_MISMATCH")
    if not canonical_gate14.get("sentence_units") or any(u.get("original_text") not in canonical_text for u in canonical_gate14.get("sentence_units", [])):
        findings.append("CANONICAL_GATE14_CANDIDATE_UNIT_MISSING_FROM_SOURCE")
    if output.get("canonical_source_coverage", {}).get("full_source_match") is not True:
        findings.append("CANONICAL_SOURCE_COVERAGE_NOT_PASS")

    registry_gates = sorted(item.get("gate") for item in registry.get("gates", []) if isinstance(item.get("gate"), int))
    if registry.get("source_commit") != SOURCE_COMMIT or registry_gates != list(range(1, 9)):
        findings.append("GATE_1_8_SOURCE_REGISTRY_MISMATCH")
    if any(item.get("source_status") != "SOURCE-CHECKED" or not item.get("source_excerpt") for item in registry.get("gates", [])):
        findings.append("GATE_1_8_SOURCE_EVIDENCE_INCOMPLETE")

    source_ids = set(expected)
    target_ids = known_target_ids(registry)
    seen_links: list[dict[str, Any]] = []
    for unit in units:
        uid = unit.get("unit_id", "<missing-id>")
        if unit.get("source_status") == "VERIFIED":
            findings.append(f"UNSUPPORTED_SOURCE_VERIFICATION:{uid}")
        if unit.get("link_status") == "LINKED":
            for link in unit.get("structural_links", []):
                seen_links.append(link)
                if not all(link.get(k) for k in ("source_unit_id", "target_unit_id", "relationship_type", "evidence_reference")):
                    findings.append(f"LINK_WITHOUT_EVIDENCE:{uid}")
                if link.get("source_unit_id") not in source_ids:
                    findings.append(f"UNKNOWN_LINK_SOURCE:{uid}")
                if link.get("target_unit_id") not in target_ids:
                    findings.append(f"UNKNOWN_LINK_TARGET:{uid}")
                if len(str(link.get("evidence_reference", "")).strip()) < 20:
                    findings.append(f"INSUFFICIENT_LINK_EVIDENCE:{uid}")
        elif unit.get("link_status") not in {"UNRESOLVED", "BLOCKED"}:
            findings.append(f"INVALID_LINK_STATUS:{uid}")

    if len(seen_links) != len(manifest):
        findings.append("MANIFEST_OUTPUT_LINK_COUNT_MISMATCH")
    if output.get("rejected_links"):
        findings.append("REJECTED_LINKS_PRESENT")
    if output.get("coverage", {}).get("coverage_status") != "PASS":
        findings.append("SOURCE_COVERAGE_NOT_PASS")
    if output.get("coverage", {}).get("gate_1_8_registry_status") != "SOURCE-CHECKED":
        findings.append("GATE_1_8_REGISTRY_NOT_SOURCE_CHECKED")
    if output.get("status") != "READY_FOR_REVIEW":
        findings.append("INTEGRATION_NOT_READY_FOR_REVIEW")

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
    manifest = json.loads(LINKS_PATH.read_text(encoding="utf-8"))
    registry = load_json(PRECEDING_SOURCE_REGISTRY_PATH)
    canonical_source = SOURCE_SNAPSHOT_PATH.read_text(encoding="utf-8")
    canonical_registry = load_json(BOOK_REGISTRY_PATH)
    findings = audit(contract, source, output, manifest, registry, canonical_source, canonical_registry)

    report = {
        "audit_status": "PASS" if not findings else "FAIL",
        "findings": findings,
        "integration_status": output.get("status"),
        "coverage_status": output.get("coverage", {}).get("coverage_status"),
        "units_audited": len(output.get("units", [])),
        "links_audited": sum(len(unit.get("structural_links", [])) for unit in output.get("units", [])),
        "gate_1_8_source_registry": output.get("coverage", {}).get("gate_1_8_registry_status"),
        "canonical_source_coverage": output.get("canonical_source_coverage", {}).get("status"),
        "canonical_sentence_candidates_gate14": output.get("canonical_source_coverage", {}).get("canonical_sentence_candidates"),
        "legacy_gate14_registry_coverage": output.get("canonical_source_coverage", {}).get("legacy_registry_coverage"),
        "verification_boundary": (
            "Audit PASS confirms source preservation, registry coverage, declared link targets, and required evidence fields. "
            "It does not certify full sentence-level extraction of Gates 1-8 or prove semantic identity of structural correspondences."
        )
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["audit_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
