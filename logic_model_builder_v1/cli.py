"""Command-line interface for the WANGA logic-native model builder."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

from .builder import build_model, execute_model_artifact
from .logic_native_language import compile_lnl
from .providers import OpenAICompatibleProvider, StructuredSpecProvider


def _read_json(path: str) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Input JSON must contain an object")
    return data


def _write(payload: Any, output: str | None) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output:
        target = Path(output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


def _provider(name: str):
    if name == "template":
        return StructuredSpecProvider()
    return OpenAICompatibleProvider()


def main(argv: list[str] | None = None) -> int:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="WANGA Logic-Native Language / Model Builder V1")
    sub = parser.add_subparsers(dest="command", required=True)

    compile_p = sub.add_parser("compile", help="Compile an .lnl file to a model artifact")
    compile_p.add_argument("source")
    compile_p.add_argument("--out")

    build_p = sub.add_parser("build", help="Build a model from a structured specification")
    build_p.add_argument("spec")
    build_p.add_argument("--provider", choices=["template", "llm"], default="template")
    build_p.add_argument("--max-attempts", type=int, default=3)
    build_p.add_argument("--out")
    build_p.add_argument("--execute", action="store_true")
    build_p.add_argument("--repo-root", default=str(root))
    build_p.add_argument("--no-corpus", action="store_true")

    run_p = sub.add_parser("run", help="Execute a compiled model artifact")
    run_p.add_argument("artifact")
    run_p.add_argument("--repo-root", default=str(root))
    run_p.add_argument("--no-corpus", action="store_true")
    run_p.add_argument("--out")

    demo_p = sub.add_parser("demo", help="Run the synthetic end-to-end model-builder example")
    demo_p.add_argument("--provider", choices=["template", "llm"], default="template")
    demo_p.add_argument("--repo-root", default=str(root))
    demo_p.add_argument("--no-corpus", action="store_true")
    demo_p.add_argument("--out")

    args = parser.parse_args(argv)
    if args.command == "compile":
        artifact = compile_lnl(Path(args.source).read_text(encoding="utf-8"))
        _write(artifact, args.out)
        return 0 if artifact.get("status") == "COMPILED_FOR_REVIEW" else 2

    if args.command == "build":
        spec = _read_json(args.spec)
        built = build_model(spec, _provider(args.provider), max_attempts=args.max_attempts)
        if args.execute and built.get("status") == "MODEL_BUILT_READY_FOR_REVIEW":
            built["execution_result"] = execute_model_artifact(
                built["model_artifact"], repo_root=args.repo_root, use_corpus=not args.no_corpus
            )
        _write(built, args.out)
        return 0 if built.get("status") == "MODEL_BUILT_READY_FOR_REVIEW" else 2

    if args.command == "run":
        artifact = _read_json(args.artifact)
        result = execute_model_artifact(artifact, repo_root=args.repo_root, use_corpus=not args.no_corpus)
        _write(result, args.out)
        return 0 if result.get("status") == "GOALS_MET" else 2

    spec_path = Path(__file__).parent / "examples" / "site_change_spec.json"
    spec = _read_json(str(spec_path))
    built = build_model(spec, _provider(args.provider))
    if built.get("status") == "MODEL_BUILT_READY_FOR_REVIEW":
        built["execution_result"] = execute_model_artifact(
            built["model_artifact"], repo_root=args.repo_root, use_corpus=not args.no_corpus
        )
    _write(built, args.out)
    return 0 if built.get("status") == "MODEL_BUILT_READY_FOR_REVIEW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
