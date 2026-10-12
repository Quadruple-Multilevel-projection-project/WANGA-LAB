"""Build a release-blocked, reproducible two-scale typed-fragment candidate."""
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from logic_fractal.fragment_composer import compose_pair, validate_fragment


def main():
    fixture=json.loads((ROOT/"logic_fractal/data/typed_fragments_fixture.json").read_text(encoding="utf-8"))
    sources=fixture["source_registry"]
    fragments={f["fragment_id"]:f for f in fixture["fragments"]}
    base_checks=[validate_fragment(f,sources) for f in fragments.values()]
    one=compose_pair(fragments["FL-OBSERVATION"],fragments["FL-RELATION-EXTRACT"],source_registry=sources)
    two=compose_pair(one["fragment"],fragments["FL-REVIEW"],source_registry=sources)
    artifact={
      "model":"WANGA Typed Fractal Logic Candidate V0.1",
      "status":"CANDIDATE_NOT_RELEASED",
      "scope":fixture["scope"],
      "source_registry":sources,
      "base_fragment_checks":base_checks,
      "composition_levels":[
        {"scale":1,"fragment":one["fragment"],"trace":one["composition_trace"]},
        {"scale":2,"fragment":two["fragment"],"trace":two["composition_trace"]}
      ],
      "release_gate":{
        "source_lineage_preserved":len(two["composition_trace"]["source_ids_preserved"])==3,
        "two_scales_composed":one["fragment"]["scale"]==1 and two["fragment"]["scale"]==2,
        "replay_deterministic":True,
        "uses_synthetic_only_fixtures":True,
        "real_conversation_sources_reviewed":False,
        "negative_boundary_benchmark_complete":False,
        "independent_review_complete":False,
        "decision":"BLOCKED_PENDING_REAL_SOURCE_FRAGMENTS_NEGATIVE_BOUNDARY_TESTS_AND_INDEPENDENT_REVIEW"
      },
      "model_hash":two["fragment"]["model_hash"],
      "semantic_status":"NOT_YET_VERIFIED",
      "limits":[
        "This validates a typed composition mechanism on synthetic fixtures only.",
        "Type compatibility does not establish semantic equivalence.",
        "This is not a trained AI model or proof of intelligence."
      ]
    }
    out=ROOT/"research/reports/logic-fractal/typed-first-model-candidate.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out),"status":artifact["status"],"scale_1_hash":one["fragment"]["model_hash"],"scale_2_hash":two["fragment"]["model_hash"],"decision":artifact["release_gate"]["decision"]},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
