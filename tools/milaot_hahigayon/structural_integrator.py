#!/usr/bin/env python3
"""Source-preserving structural integration for Milaot HaHigayon.

This module does not interpret the text. It indexes source units and attaches
only links explicitly recorded in a separate link manifest.
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
OUT_DIR = ROOT / "artifacts"
OUT_PATH = OUT_DIR / "gate14_structural_integration.json"


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


def detect_coverage(index_text: str) -> dict[str, Any]:
    indexed_gates: set[int] = set()
    for match in re.finditer(r"(?m)^\|\s*([^|]+?)\s*\|\s*\x60?([^|]+?)\x60?\s*\|\s*EXTRACTED\s*\|", index_text):
        label = match.group(1).strip()
        numeral_map = {
            "א׳": 1, "ב׳": 2, "ג׳": 3, "ד׳": 4, "ה׳": 5, "ו׳": 6,
            "ז׳": 7, "ח׳": 8, "ט׳": 9, "י׳": 10, "י״א": 11,
            "י״ב": 12, "י״ג": 13, "י״ד": 14, "יג": 13, "יד": 14
        }
        if label in numeral_map:
            indexed_gates.add(numeral_map[label])

    # The index is an inventory, not proof that no other source exists.
    # This records coverage listed by the repository index only.
    required = set(range(1, 14))
    missing = sorted(required - indexed_gates)
    return {
        "indexed_gates": sorted(indexed_gates),
        "required_preceding_gates": sorted(required),
        "gates_not_listed_as_extracted": missing,
        "coverage_status": "PASS" if not missing else "BLOCKED",
        "basis": "milaot-hahigayon/sentences/INDEX.md"
    }


def validate_link(link: dict[str, Any]) -> list[str]:
    required = ("source_unit_id", "target_unit_id", "relationship_type", "evidence_reference")
    return [f"missing:{key}" for key in required if not link.get(key)]


def integrate() -> dict[str, Any]:
    contract = json.loads(read_text(CONTRACT_PATH))
    index_text = read_text(INDEX_PATH)
    gate14_text = read_text(GATE14_PATH)
    gate13_text = read_text(GATE13_PATH)
    coverage = detect_coverage(index_text)
    units = parse_gate14_units(gate14_text)
    explicit_links = read_json(LINKS_PATH, [])

    links_by_source: dict[str, list[dict[str, Any]]] = {}
    rejected_links: list[dict[str, Any]] = []
    for link in explicit_links:
        errors = validate_link(link)
        if errors or not link.get("evidence_reference"):
            rejected_links.append({"link": link, "errors": errors or ["missing:evidence_reference"]})
            continue
        links_by_source.setdefault(link["source_unit_id"], []).append(link)

    for unit in units:
        links = links_by_source.get(unit["unit_id"], [])
        unit["structural_links"] = links
        unit["link_status"] = "LINKED" if links else "UNRESOLVED"

    # Gate 13 is checked for presence; no automatic semantic matching is allowed.
    gate13_present = bool(gate13_text.strip())
    status = "READY_FOR_REVIEW" if coverage["coverage_status"] == "PASS" and not rejected_links else "BLOCKED"

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
            "The repository index currently lists extraction for Gates 9-14, not Gates 1-8.",
            "No relation is inferred from keyword similarity; links require explicit evidence references.",
            "EXTRACTED does not mean SOURCE-CHECKED or VERIFIED."
        ] if status == "BLOCKED" else [],
        "source_artifacts": [
            "milaot-hahigayon/sentences/INDEX.md",
            "milaot-hahigayon/sentences/שער-יד.md",
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
        "coverage_status": result["coverage"]["coverage_status"],
        "output": str(OUT_PATH.relative_to(ROOT))
    }, ensure_ascii=False, indent=2))
    return 0 if result["status"] != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
