#!/usr/bin/env python3
"""Create a deterministic *proposed* ARK agent registry from a sourced seed.

This tool does not create accounts, provision external agents, access secrets,
delete nodes, or mutate Layer 4. It emits a reviewable registry proposal only.
Input JSON: {"agents":[{"agent_id":"L1-001","level":"L1",
"parent_id":null,"source_reference":"path/to/source.md#section"}]}
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LEVELS = ("L1", "L2", "L3", "L4")
MAX_AGENTS = 1000
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


def load_seed(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("agents")
    if not isinstance(rows, list) or not rows:
        raise ValueError("Input must contain a non-empty 'agents' array.")
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Each agent must be a JSON object.")
        agent_id = row.get("agent_id")
        level = row.get("level")
        source = row.get("source_reference")
        if not isinstance(agent_id, str) or not ID_RE.fullmatch(agent_id):
            raise ValueError(f"Invalid agent_id: {agent_id!r}")
        if agent_id in seen:
            raise ValueError(f"Duplicate agent_id: {agent_id}")
        seen.add(agent_id)
        if level not in LEVELS:
            raise ValueError(f"{agent_id}: level must be one of {LEVELS}")
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"{agent_id}: source_reference is required.")
    for row in rows:
        parent = row.get("parent_id")
        if parent is not None and parent not in seen:
            raise ValueError(f"{row['agent_id']}: parent_id {parent!r} is not in seed.")
    return rows


def build_registry(seed: list[dict], children_per_agent: int) -> dict:
    agents: list[dict] = []
    seen_ids: set[str] = set()

    def add_agent(agent_id: str, level: str, parent_id: str | None,
                  source_reference: str, status: str) -> None:
        if agent_id in seen_ids:
            raise ValueError(f"Generated agent ID collision: {agent_id}")
        seen_ids.add(agent_id)
        agents.append({
            "agent_id": agent_id,
            "level": level,
            "parent_id": parent_id,
            "source_reference": source_reference,
            "status": status,
            "execution_authorized": False,
            "capabilities": [],
            "created_by": "ark_agent_genesis.py",
        })
        level_index = LEVELS.index(level)
        if children_per_agent and level_index < len(LEVELS) - 1:
            child_level = LEVELS[level_index + 1]
            for n in range(1, children_per_agent + 1):
                child_id = f"{agent_id}.{child_level}.{n:03d}"
                add_agent(child_id, child_level, agent_id, source_reference, "PROPOSED")
                if len(agents) > MAX_AGENTS:
                    raise ValueError(f"Proposal exceeds safety cap ({MAX_AGENTS} agents).")

    for row in seed:
        add_agent(
            row["agent_id"], row["level"], row.get("parent_id"),
            row["source_reference"].strip(), "PLANNED",
        )
        if len(agents) > MAX_AGENTS:
            raise ValueError(f"Proposal exceeds safety cap ({MAX_AGENTS} agents).")

    return {
        "schema_version": "1.0",
        "record_type": "PROPOSED_AGENT_REGISTRY",
        "authority": "No authority is implied by this generated file.",
        "agent_count": len(agents),
        "levels": list(LEVELS),
        "agents": agents,
        "safety": {
            "external_agents_spawned": False,
            "email_account_created": False,
            "credentials_generated_or_stored": False,
            "layer4_mutated": False,
            "source_grounding_required": True,
            "human_review_required_before_activation": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", required=True, type=Path,
                        help="JSON file with explicitly sourced seed agents.")
    parser.add_argument("--out", required=True, type=Path,
                        help="Output JSON path.")
    parser.add_argument("--children-per-agent", type=int, default=0,
                        help="Propose this many children at every level through L4 (default: 0).")
    args = parser.parse_args()
    if not 0 <= args.children_per_agent <= 10:
        parser.error("--children-per-agent must be between 0 and 10.")
    try:
        seed = load_seed(args.seed)
        registry = build_registry(seed, args.children_per_agent)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote proposal: {args.out} ({registry['agent_count']} entries; none activated)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
