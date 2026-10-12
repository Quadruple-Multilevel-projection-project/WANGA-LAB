"""Validate the versioned ARK-Swarm library-integration decision matrix (stdlib only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "research/ecosystem/library_integration_matrix.json"
VALID_PRIORITIES = {"P0", "P1", "P2", "P3", "P0_P1", "P1_P2", "P1_P3", "P2_P3"}
REQUIRED_CATEGORY_FIELDS = {"id", "priority", "need", "candidate_libraries", "acceptance"}
REQUIRED_LIBRARY_FIELDS = {"name", "fit", "decision", "official_url", "status"}
REQUIRED_RULES = {
    "Z3_SAT_IS_NOT_TRUTH",
    "ENTAILMENT_ENCODING_REQUIRED",
    "PROOF_DOES_NOT_AUTHENTICATE_PREMISES",
    "PROBLOG_IS_MODEL_RELATIVE",
    "ACTIVE_INFERENCE_REQUIRES_MODEL",
    "CONNECTOME_ROLE_IS_HYPOTHESIS",
    "FRACTAL_SHAPE_IS_NOT_VALIDITY",
}


def validate_matrix(matrix: dict) -> list[str]:
    errors: list[str] = []
    if matrix.get("schema_version") != "wanga-library-integration-matrix/1.0":
        errors.append("unexpected schema_version")
    categories = matrix.get("categories")
    if not isinstance(categories, list) or not categories:
        return errors + ["categories must be a non-empty list"]
    ids = [category.get("id") for category in categories if isinstance(category, dict)]
    if len(ids) != len(categories) or len(ids) != len(set(ids)):
        errors.append("category IDs must be unique and every category must be an object")
    for index, category in enumerate(categories):
        missing = REQUIRED_CATEGORY_FIELDS - set(category)
        if missing:
            errors.append(f"category[{index}] missing fields: {sorted(missing)}")
        if category.get("priority") not in VALID_PRIORITIES:
            errors.append(f"category[{index}] invalid priority: {category.get('priority')!r}")
        libraries = category.get("candidate_libraries", [])
        if not isinstance(libraries, list) or not libraries:
            errors.append(f"category[{index}] candidate_libraries must be non-empty")
            continue
        names = set()
        for lib_index, library in enumerate(libraries):
            missing_lib = REQUIRED_LIBRARY_FIELDS - set(library) if isinstance(library, dict) else REQUIRED_LIBRARY_FIELDS
            if missing_lib:
                errors.append(f"category[{index}].candidate_libraries[{lib_index}] missing fields: {sorted(missing_lib)}")
                continue
            if library["name"] in names:
                errors.append(f"category[{index}] duplicate library: {library['name']}")
            names.add(library["name"])
            if not library["official_url"].startswith("https://"):
                errors.append(f"{library['name']} official_url must use HTTPS")
    rules = {item.get("rule") for item in matrix.get("mandatory_semantic_rules", [])}
    if not REQUIRED_RULES.issubset(rules):
        errors.append(f"missing semantic rules: {sorted(REQUIRED_RULES - rules)}")
    if "logical assets only" not in matrix.get("scope", {}).get("logic_trader", "").casefold():
        errors.append("Logic Trader logical-asset scope is missing")
    return errors


def main() -> int:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    errors = validate_matrix(matrix)
    if errors:
        print(json.dumps({"status": "FAIL", "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    libraries = sum(len(c["candidate_libraries"]) for c in matrix["categories"])
    print(json.dumps({
        "status": "PASS",
        "category_count": len(matrix["categories"]),
        "library_decisions": libraries,
        "semantic_rule_count": len(matrix["mandatory_semantic_rules"]),
        "acceptance_gate_count": len(matrix["acceptance_gates"]),
        "result": "DECISION_MATRIX_VALID_NOT_A_CLAIM_THAT_DEPENDENCIES_ARE_INSTALLED",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
