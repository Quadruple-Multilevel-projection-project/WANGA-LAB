#!/usr/bin/env python3
"""Create a reproducible inventory of the Agency Agents upstream catalog.

Run from an AI231 checkout:
  python scripts/inventory_agency_agents.py --repo /path/to/agency-agents \
      --commit 8ae6164602c95ca78828b148b9052460ee426885 \
      --output artifacts/agency-agents/inventory.json

No network access, installation, imports from upstream, or agent execution occurs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ACTION_RECORD = {
    "timestamp": "2026-11-16T15:30:00+02:00",
    "contract_start_time": "2026-11-16T15:27:30+02:00",
    "action_id": "ACT-20261116-AI231-AGENCY-INVENTORY-FIX-005",
    "sha256": "3bb25f09b033f015687bd5f7e7ccbcebd353cdc533b39739293f8d8a2ac82651",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def frontmatter(path: Path) -> dict[str, str] | None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return None
    result: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if match:
            result[match.group(1)] = match.group(2).strip().strip("\"'")
    return result


def build_inventory(repo: Path, commit: str) -> dict[str, Any]:
    divisions_path = repo / "divisions.json"
    if not divisions_path.is_file():
        raise FileNotFoundError(f"Missing source-of-truth division registry: {divisions_path}")
    divisions_doc = json.loads(divisions_path.read_text(encoding="utf-8"))
    divisions = divisions_doc.get("divisions")
    if not isinstance(divisions, dict):
        raise ValueError("divisions.json must contain an object named 'divisions'")

    agents: list[dict[str, str]] = []
    division_counts: dict[str, int] = {}
    for slug, metadata in sorted(divisions.items()):
        directory = repo / slug
        if not directory.is_dir():
            raise ValueError(f"Registered division directory is missing: {slug}")
        count = 0
        for path in sorted(directory.rglob("*.md")):
            if ".git" in path.parts:
                continue
            meta = frontmatter(path)
            if meta is None:
                continue
            rel = path.relative_to(repo).as_posix()
            agents.append({
                "slug": path.stem,
                "division": slug,
                "division_label": str(metadata.get("label", slug)),
                "name": meta.get("name", path.stem),
                "description": meta.get("description", ""),
                "path": rel,
                "sha256": sha256_file(path),
            })
            count += 1
        if count == 0:
            raise ValueError(f"Registered division has no frontmatter agent files: {slug}")
        division_counts[slug] = count

    license_candidates = [repo / "LICENSE", repo / "LICENSE.md", repo / "LICENSE.txt"]
    license_file = next((p for p in license_candidates if p.is_file()), None)
    return {
        "schema_version": "1.0",
        "source": {
            "repository": "https://github.com/msitarzewski/agency-agents",
            "commit": commit,
            "divisions_registry": "divisions.json",
            "divisions_registry_sha256": sha256_file(divisions_path),
            "license_file": license_file.relative_to(repo).as_posix() if license_file else None,
            "license_sha256": sha256_file(license_file) if license_file else None,
        },
        "counts": {
            "divisions": len(divisions),
            "agents": len(agents),
            "agents_by_division": division_counts,
        },
        "agents": agents,
        "inventory_status": "LOCAL_TREE_INVENTORIED_LICENSE_REQUIRES_HUMAN_REVIEW",
        "execution_status": "NO_AGENTS_INSTALLED_OR_EXECUTED",
        "action_record": ACTION_RECORD,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="Local read-only checkout of upstream")
    parser.add_argument("--commit", required=True, help="Exact upstream commit SHA")
    parser.add_argument("--output", required=True, type=Path, help="JSON output path")
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not repo.is_dir():
        parser.error(f"--repo is not a directory: {repo}")
    if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
        parser.error("--commit must be a full 40-character lowercase Git SHA")

    inventory = build_inventory(repo, args.commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "INVENTORY_WRITTEN",
        "agents": inventory["counts"]["agents"],
        "divisions": inventory["counts"]["divisions"],
        "output": str(args.output),
        "execution_status": inventory["execution_status"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
