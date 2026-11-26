#!/usr/bin/env python3
"""Deterministic WANGA 231-gate catalog and source-observation compiler.

This compiler does NOT infer semantics. It builds the mathematically complete
unordered-pair catalog, records literal Unicode evidence found in source files,
and leaves unsupported TANTA fields ABSTAIN. No model is allowed to issue LOCK.
"""
from __future__ import annotations
import argparse, hashlib, json, math, re
from pathlib import Path

ALPHABET = list("אבגדהוזחטיכלמנסעפצקרשת")
TOTAL_GATES = math.comb(len(ALPHABET), 2)
ALBAM_AXES = {"אל", "במ", "גן", "דס", "הע", "ופ", "זצ", "חק", "טר", "יש", "כת"}

def gate_catalog():
    gates = []
    for idx, (a_i, b_i) in enumerate(
        ((i, j) for i in range(len(ALPHABET)) for j in range(i + 1, len(ALPHABET))), 1
    ):
        pair = ALPHABET[a_i] + ALPHABET[b_i]
        row, col = divmod(idx - 1, 11)
        theta = (idx - 1) / TOTAL_GATES * 2 * math.pi
        # Deterministic visualization coordinates only; not physical measurements.
        z = 1 - 2 * (idx - 0.5) / TOTAL_GATES
        radius = math.sqrt(max(0.0, 1 - z * z))
        phi = idx * math.pi * (3 - math.sqrt(5))
        gates.append({
            "gate_id": idx, "pair": pair,
            "matrix_21x11": {"row": row + 1, "col": col + 1,
                             "is_albam_axis": pair in ALBAM_AXES},
            "phase_wheel": {"angle_deg": round(math.degrees(theta), 9),
                            "slot_230": ((idx - 1) % 230) + 1,
                            "slot_semantics": "UNVERIFIED_INDEX_NOT_CRYSTALLOGRAPHIC_GROUP"},
            "star_vector": {"pseudo_vx": round(radius * math.cos(phi), 9),
                            "pseudo_vy": round(radius * math.sin(phi), 9),
                            "pseudo_vz": round(z, 9),
                            "coordinate_status": "VISUALIZATION_ONLY"},
            "tanta_layers": {
                "taamim": {"marks": [], "status": "ABSTAIN"},
                "nekudot": {"marks": [], "status": "ABSTAIN"},
                "tagin": {"global_topology": None, "private_modulation": None,
                          "status": "ABSTAIN"},
                "otiot": {"pair": pair, "status": "CATALOGED_NOT_SEMANTICALLY_LOCKED"}
            },
            "evidence": [],
            "ternary_status": "ABSTAIN",
            "lock_reason": "No authoritative source mapping and independent approval supplied."
        })
    assert len(gates) == 231 and len({g["pair"] for g in gates}) == 231
    assert len({(g["matrix_21x11"]["row"], g["matrix_21x11"]["col"]) for g in gates}) == 231
    return gates

def source_observations(input_dir: Path, gate_by_pair):
    observations = []
    if not input_dir.exists():
        return observations
    # Preserve source text and offsets. A matched adjacent pair is an occurrence,
    # not proof of a semantic gate or TANTA assignment.
    for path in sorted(p for p in input_dir.rglob("*") if p.is_file()):
        try:
            raw = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        for match in re.finditer(r"[א-ת]{2}", raw):
            pair = match.group(0)
            key = "".join(sorted(pair, key=ALPHABET.index)) if all(c in ALPHABET for c in pair) and pair[0] != pair[1] else None
            if key not in gate_by_pair:
                continue
            observations.append({
                "source_path": str(path), "source_sha256": digest,
                "char_start": match.start(), "char_end": match.end(),
                "literal_excerpt": match.group(0), "catalog_pair": key,
                "evidence_type": "LITERAL_ADJACENT_LETTER_OCCURRENCE",
                "semantic_claim": False, "ternary_status": "ABSTAIN"
            })
    return observations

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", default="sources")
    ap.add_argument("--output-dir", default="compiled")
    ap.add_argument("--strict-lock-only", action="store_true",
                    help="Reserved safety option; no LOCKs are issued by this version.")
    args = ap.parse_args()
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    gates = gate_catalog()
    by_pair = {g["pair"]: g for g in gates}
    observations = source_observations(Path(args.input_dir), by_pair)
    for obs in observations:
        by_pair[obs["catalog_pair"]]["evidence"].append(obs)
    payload = {
        "compiler": "WANGA-TANTA-231", "version": "1.0.0",
        "status": "CATALOG_COMPILED_SEMANTICS_UNVERIFIED",
        "alphabet": ALPHABET, "gate_count": len(gates),
        "combinatorial_check": "C(22,2)=231",
        "matrix": {"rows": 21, "cols": 11, "capacity": 231},
        "source_observation_count": len(observations),
        "policy": {
            "model_generated_lock": False,
            "literal_occurrence_is_not_semantic_proof": True,
            "unverified_space_group_slots_are_not_crystallographic_groups": True,
            "missing_or_conflicting_tanta_data": "ABSTAIN"
        },
        "gates": gates
    }
    (out / "wanga_231_gate_catalog.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "source_observations.json").write_text(
        json.dumps(observations, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {
        "status": payload["status"], "gate_count": len(gates),
        "matrix_cells": 231, "source_observations": len(observations),
        "locked_gates": 0, "abstain_gates": 231
    }
    (out / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
