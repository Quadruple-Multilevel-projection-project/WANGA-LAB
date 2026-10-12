"""Build the first bounded fractal-logic model candidate from canonical fixtures.

This script generates an auditable candidate artifact; it does not declare model
semantics verified or claim the user conversation corpus has been exhaustively
collected.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve()
RESEARCH_ROOT = HERE.parents[1]  # repository/research/fractal-logic-model
REPO_ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parent))
from fractal_composer import compose_pair, validate_fragment, content_hash


def main() -> int:
    fixture_path = RESEARCH_ROOT / "examples" / "canonical_fragments_v1.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    sources = data["source_registry"]
    fragments = {f["fragment_id"]: f for f in data["fragments"]}
    base_results = [validate_fragment(f, sources) for f in fragments.values()]

    level_one = compose_pair(
        fragments["FL-OBSERVATION"],
        fragments["FL-RELATION-EXTRACT"],
        source_registry=sources,
    )
    level_two = compose_pair(
        level_one["fragment"],
        fragments["FL-REVIEW"],
        source_registry=sources,
    )
    candidate = level_two["fragment"]
    artifact = {
        "model": "WANGA Fractal Logic First Model Candidate V0.1",
        "status": "CANDIDATE_NOT_RELEASED",
        "release_gate": {
            "source_fixtures_valid": all(x["status"] == "VALID_STRUCTURE" for x in base_results),
            "two_scales_composed": level_one["fragment"]["scale"] == 1 and candidate["scale"] == 2,
            "provenance_preserved": len(level_two["composition_trace"]["source_ids_preserved"]) == 3,
            "deterministic_replay": False,
            "negative_boundary_benchmark": False,
            "conversation_archive_coverage": "PARTIAL_ACCESS_ONLY_NOT_EXHAUSTIVELY_VERIFIED",
            "independent_review": False,
            "release_decision": "BLOCKED_PENDING_REPLAY_NEGATIVE_TESTS_SOURCE_REVIEW_AND_REAL_SOURCE_FRAGMENTS",
        },
        "source_registry": data["source_registry"],
        "base_fragment_validation": base_results,
        "composition_levels": [
            {
                "scale": 1,
                "status": level_one["status"],
                "fragment": level_one["fragment"],
                "trace": level_one["composition_trace"],
            },
            {
                "scale": 2,
                "status": level_two["status"],
                "fragment": candidate,
                "trace": level_two["composition_trace"],
            },
        ],
        "model_hash": candidate["model_hash"],
        "semantic_status": "NOT_YET_VERIFIED",
        "limits": [
            "The three source records point to synthetic fixtures, not externally verified claims.",
            "This proves the composer can construct a two-scale typed candidate, not that fractal logic is a true ontology or that it produces intelligence.",
            "Real conversation fragments, independent review, negative/boundary tests and replay acceptance remain required.",
        ],
    }
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/fractal-logic-first-model-candidate.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(out),
        "status": artifact["status"],
        "scale_one_hash": level_one["fragment"]["model_hash"],
        "scale_two_hash": candidate["model_hash"],
        "release_decision": artifact["release_gate"]["release_decision"],
        "semantic_status": artifact["semantic_status"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
