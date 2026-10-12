"""CLI for building, verifying and branching WANGA-X Blueprints."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

from .engine import ROOT, append_rollback_frame, build_blueprint, load_catalog, verify_blueprint, write_artifact


def read_json(path: str) -> dict[str, Any]:
    result = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise ValueError("Input must be a JSON object.")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="WANGA-X requirement-driven architecture Blueprint engine")
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="derive required computation and generate architecture candidates")
    build.add_argument("requirement")
    build.add_argument("--out")
    build.add_argument("--repo-root", default=str(ROOT))
    verify = sub.add_parser("verify", help="verify a Blueprint artifact's structural contract")
    verify.add_argument("artifact")
    rollback = sub.add_parser("rollback", help="append a rollback branch referencing a prior frame")
    rollback.add_argument("artifact")
    rollback.add_argument("--frame", required=True)
    rollback.add_argument("--note", required=True)
    rollback.add_argument("--out", required=True)
    demo = sub.add_parser("demo", help="build the logic-native model-builder requirement fixture")
    demo.add_argument("--out")
    demo.add_argument("--repo-root", default=str(ROOT))
    args = parser.parse_args(argv)

    if args.command == "build":
        result = build_blueprint(read_json(args.requirement), repo_root=args.repo_root)
        write_artifact(result, args.out) if args.out else print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["verification"]["status"] == "PASS" else 2
    if args.command == "verify":
        artifact = read_json(args.artifact)
        report = verify_blueprint(artifact.get("blueprint", {}), load_catalog())
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["status"] == "PASS" else 2
    if args.command == "rollback":
        artifact = read_json(args.artifact)
        updated = append_rollback_frame(artifact, args.frame, args.note)
        write_artifact(updated, args.out)
        print(json.dumps({
            "status": "ROLLBACK_BRANCH_CREATED", "output_artifact": args.out,
            "target_frame": args.frame, "new_frame": updated["reversibility"]["rollback_frame_id"],
            "frame_count": len(updated["construction_frames"]),
        }, ensure_ascii=False, indent=2))
        return 0
    requirement_path = Path(__file__).parent / "examples" / "logic_model_builder_requirement.json"
    result = build_blueprint(read_json(str(requirement_path)), repo_root=args.repo_root)
    write_artifact(result, args.out) if args.out else print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verification"]["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
