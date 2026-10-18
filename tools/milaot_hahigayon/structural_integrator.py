#!/usr/bin/env python3
"""Source-preserving structural integration for Milaot HaHigayon.

This module indexes Gate 14 source units and attaches only evidence-bearing
links in a separate manifest. It distinguishes source location from full
sentence-level extraction and never infers links from keyword similarity alone.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / "milaot-hahigayon/sentences/INDEX.md"
GATE14_PATH = ROOT / "milaot-hahigayon/sentences/שער-יד.md"
GATE13_PATH = ROOT / "docs/LOGIC/MILOT_HIGAYON_GATE_13_SENTENCE_REGISTRY.md"
CONTRACT_PATH = ROOT / "milaot-hahigayon/integration/INTERNAL_FRAMEWORK_CONTRACT.json"
LINKS_PATH = ROOT / "milaot-hahigayon/integration/explicit_links.json"
PRECEDING_SOURCE_REGISTRY_PATH = ROOT / "milaot-hahigayon/integration/gates_1_8_source_registry.json"
OUT_DIR = ROOT / "artifacts"
OUT_PATH = OUT_DIR / "gate14_structural_integration.json"

SOURCE_COMMIT = "d1106d9a66528dc3e39cf1ea0732782927d9f678"
GATE_NUMERALS = {
    "א": 1, "א׳": 1, "ב": 2, "ב׳": 2, "ג": 3, "ג׳": 3,
    "ד": 4, "ד׳": 4, "ה": 5, "ה׳": 5, "ו": 6, "ו׳": 6,
    "ז": 7, "ז׳": 7, "ח": 8, "ח׳": 8, "ט": 9, "ט׳": 9,
    "י": 10, "י׳": 10, "י״א": 11, "י״ב": 12, "י״ג": 13,
    "י״ד": 14, "יג": 13, "יד": 14
}


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Required source file missing: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def parse_gate14_units(text: str) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    current_id: str | None = None
    current_label: str | None = None

    for line in text.splitlines():
        heading = re.match(r"^###\s+(T14-\d+)\s+[—–-]\s+(.+?)\s*$", line)
        if heading:
            current_id, current_label = heading.group(1), heading.group(2)
            continue
        quote = re.match(r"^>\s?(.*)$", line)
        if quote and current_id:
            units.append({
                "unit_id": current_id,
                "source_label": current_label,
                "source_text": quote.group(1),
                "source_file": "milaot-hahigayon/sentences/שער-יד.md",
                "source_status": "EXTRACTED_NOT_SOURCE_VERIFIED",
                "structural_links": [],
                "link_status": "UNRESOLVED"
            })
            current_id = None
            current_label = None

    if not units:
        raise ValueError("No Gate 14 source units were parsed; refusing empty output.")
    return units


def validate_preceding_registry(registry: dict[str, Any]) -> tuple[bool, list[int]]:
    gates = registry.get("gates", [])
    gate_numbers = sorted(
        item.get("gate") for item in gates
        if isinstance(item, dict) and isinstance(item.get("gate"), int)
    )
    valid = (
        registry.get("registry_id") == "MILAOT_HAHIGAYON_GATES_1_8_SOURCE_REGISTRY_V1"
        and registry.get("source_commit") == SOURCE_COMMIT
        and registry.get("status") == "SOURCE_CHECKED"
        and gate_numbers == list(range(1, 9))
        and all(
            item.get("source_status") == "SOURCE-CHECKED"
            and bool(item.get("target_unit_id"))
            and bool(item.get("source_heading"))
            and bool(item.get("source_excerpt"))
            for item in gates
        )
    )
    return valid, gate_numbers


def detect_coverage(index_text: str, registry: dict[str, Any]) -> dict[str, Any]:
    gate_states: dict[int, str] = {}
    row_pattern = re.compile(
        r"(?m)^\|\s*([^|]+?)\s*\|\s*\x60?([^|]+?)\x60?\s*\|\s*(EXTRACTED|SOURCE-LOCATED)\s*\|"
    )
    for match in row_pattern.finditer(index_text):
        label = match.group(1).strip()
        status = match.group(3).strip()
        gate = GATE_NUMERALS.get(label)
        if gate is not None:
            gate_states[gate] = status

    required = set(range(1, 14))
    covered = {gate for gate, status in gate_states.items() if status in {"EXTRACTED", "SOURCE-LOCATED"}}
    extracted = sorted(gate for gate, status in gate_states.items() if status == "EXTRACTED")
    source_located = sorted(gate for gate, status in gate_states.items() if status == "SOURCE-LOCATED")
    missing = sorted(required - covered)
    registry_valid, registry_gates = validate_preceding_registry(registry)

    # A source locator is coverage evidence, not a claim of full sentence extraction.
    coverage_pass = not missing and registry_valid and set(range(1, 9)).issubset(set(registry_gates))
    return {
        "indexed_gates": sorted(gate_states),
        "extracted_gates": extracted,
        "source_located_gates": source_located,
        "required_preceding_gates": sorted(required),
        "gates_not_covered": missing,
        "gates_not_sentence_extracted": sorted(required - set(extracted)),
        "gate_1_8_registry_status": "SOURCE-CHECKED" if registry_valid else "INVALID",
        "coverage_status": "PASS" if coverage_pass else "BLOCKED",
        "basis": [
            "milaot-hahigayon/sentences/INDEX.md",
            "milaot-hahigayon/integration/gates_1_8_source_registry.json"
        ],
        "coverage_boundary": (
            "Gates 1-8 are source-located at an immutable source commit; this does not "
            "claim full sentence-level extraction for those gates."
        )
    }


def validate_link(link: dict[str, Any], source_ids: set[str], target_ids: set[str]) -> list[str]:
    required = ("source_unit_id", "target_unit_id", "relationship_type", "evidence_reference")
    errors = [f"missing:{key}" for key in required if not link.get(key)]
    if link.get("source_unit_id") and link["source_unit_id"] not in source_ids:
        errors.append("unknown_source_unit_id")
    if link.get("target_unit_id") and link["target_unit_id"] not in target_ids:
        errors.append("unknown_target_unit_id")
    if link.get("evidence_reference") and len(link["evidence_reference"].strip()) < 20:
        errors.append("insufficient_evidence_reference")
    return errors


def collect_target_ids(registry: dict[str, Any]) -> set[str]:
    target_ids = {
        item["target_unit_id"] for item in registry.get("gates", [])
        if item.get("target_unit_id")
    }
    patterns = {
        ROOT / "milaot-hahigayon/sentences/שער-ט.md": r"\bT9-\d{3}\b",
        ROOT / "milaot-hahigayon/sentences/שער-י.md": r"\bT10-\d{3}\b",
        ROOT / "milaot-hahigayon/sentences/שער-יא.md": r"\bT11-\d{3}\b",
        ROOT / "milaot-hahigayon/sentences/שער-יב.md": r"\bT12-\d{3}\b",
        GATE13_PATH: r"\b13\.\d{3}\b"
    }
    for path, pattern in patterns.items():
        if path.exists():
            target_ids.update(re.findall(pattern, path.read_text(encoding="utf-8")))
    return target_ids


def integrate() -> dict[str, Any]:
    contract = json.loads(read_text(CONTRACT_PATH))
    index_text = read_text(INDEX_PATH)
    gate14_text = read_text(GATE14_PATH)
    gate13_text = read_text(GATE13_PATH)
    preceding_registry = json.loads(read_text(PRECEDING_SOURCE_REGISTRY_PATH))
    coverage = detect_coverage(index_text, preceding_registry)
    units = parse_gate14_units(gate14_text)
    explicit_links = read_json(LINKS_PATH, [])

    source_ids = {unit["unit_id"] for unit in units}
    target_ids = collect_target_ids(preceding_registry)
    links_by_source: dict[str, list[dict[str, Any]]] = {}
    rejected_links: list[dict[str, Any]] = []
    for link in explicit_links:
        errors = validate_link(link, source_ids, target_ids)
        if errors:
            rejected_links.append({"link": link, "errors": errors})
            continue
        links_by_source.setdefault(link["source_unit_id"], []).append(link)

    for unit in units:
        links = links_by_source.get(unit["unit_id"], [])
        unit["structural_links"] = links
        unit["link_status"] = "LINKED" if links else "UNRESOLVED"

    gate13_present = bool(gate13_text.strip())
    status = (
        "READY_FOR_REVIEW"
        if coverage["coverage_status"] == "PASS" and not rejected_links and gate13_present
        else "BLOCKED"
    )

    result = {
        "contract_id": contract["contract_id"],
        "artifact_type": "SOURCE_PRESERVING_STRUCTURAL_INTEGRATION",
        "status": status,
        "target_gate": 14,
        "preceding_gates": list(range(1, 14)),
        "coverage": coverage,
        "gate13_registry_present": gate13_present,
        "source_preserved": True,
        "interpretation_added": False,
        "explanatory_commentary_added": False,
        "external_theory_added": False,
        "units": units,
        "rejected_links": rejected_links,
        "limitations": [
            "Gates 1-8 have immutable source locators and checked excerpts, but not full sentence-level extraction in the repository index.",
            "Structural correspondence labels are metadata; they are not quotations or claims made verbatim by the source.",
            "No relation is inferred from keyword similarity alone; links require a named target and evidence reference.",
            "EXTRACTED does not mean SOURCE-CHECKED or VERIFIED."
        ],
        "source_artifacts": [
            "milaot-hahigayon/sentences/INDEX.md",
            "milaot-hahigayon/sentences/שער-יד.md",
            "milaot-hahigayon/integration/gates_1_8_source_registry.json",
            "milaot-hahigayon/integration/explicit_links.json",
            "docs/LOGIC/MILOT_HIGAYON_GATE_13_SENTENCE_REGISTRY.md"
        ]
    }
    return result


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = integrate()
    OUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "units_indexed": len(result["units"]),
        "links_attached": sum(len(unit["structural_links"]) for unit in result["units"]),
        "rejected_links": len(result["rejected_links"]),
        "coverage_status": result["coverage"]["coverage_status"],
        "source_located_gates": result["coverage"]["source_located_gates"],
        "gates_not_sentence_extracted": result["coverage"]["gates_not_sentence_extracted"],
        "output": str(OUT_PATH.relative_to(ROOT))
    }, ensure_ascii=False, indent=2))
    return 0 if result["status"] != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
