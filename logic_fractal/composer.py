"""Deterministic candidate composer for source-linked logical-fractal maps.

This generates inspectable graph/path candidates from the reviewed Logic Wiki
catalog. It does not infer truth, train weights, or claim a candidate is valid.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping


class CompositionError(ValueError):
    pass


def canonical_hash(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def load_contracts(path: str | Path) -> list[dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    contracts = data.get("rules", [])
    ids = [r.get("id") for r in contracts]
    if not ids or len(ids) != len(set(ids)):
        raise CompositionError("Composition rule IDs must be non-empty and unique.")
    for rule in contracts:
        for field in ("id", "name", "inputs", "output", "invariants", "status"):
            if field not in rule:
                raise CompositionError("Rule %r is missing %s." % (rule.get("id"), field))
        if not rule["invariants"]:
            raise CompositionError("Rule %s must specify at least one invariant." % rule["id"])
    return contracts


def build_candidate_model(catalog: Mapping[str, Any], contracts: list[dict[str, Any]], *, max_depth: int = 3, max_candidates: int = 2000) -> dict[str, Any]:
    if max_depth < 2 or max_depth > 5:
        raise CompositionError("max_depth must be between 2 and 5.")
    if max_candidates < 1 or max_candidates > 10000:
        raise CompositionError("max_candidates must be between 1 and 10000.")
    articles = catalog.get("articles", [])
    sources = catalog.get("sources", [])
    by_id = {a.get("id"): a for a in articles}
    if len(by_id) != len(articles) or None in by_id:
        raise CompositionError("Article IDs must be unique and non-empty.")
    source_ids = {s.get("id") for s in sources}
    edges: list[dict[str, Any]] = []
    adjacency: dict[str, list[str]] = {key: [] for key in by_id}
    for article in articles:
        refs = article.get("sources", [])
        if not refs or not set(refs).issubset(source_ids):
            raise CompositionError("Article %s has no source references or has dangling source IDs." % article["id"])
        for target in article.get("relations", []):
            if target not in by_id:
                raise CompositionError("Article %s has dangling relation %s." % (article["id"], target))
            adjacency[article["id"]].append(target)
            edges.append({
                "id": "EDGE-" + canonical_hash([article["id"], target])[:12],
                "source": article["id"],
                "target": target,
                "source_refs": sorted(set(refs)),
                "relation_status": "EDITORIAL_RELATION_CANDIDATE",
                "epistemic_status": "NOT_SEMANTICALLY_VERIFIED",
            })
    candidates: list[dict[str, Any]] = []
    def walk(path: list[str]) -> None:
        if len(candidates) >= max_candidates:
            return
        if len(path) >= 2:
            path_articles = [by_id[node] for node in path]
            provenance = sorted({src for article in path_articles for src in article.get("sources", [])})
            rule = next((r for r in contracts if r.get("id") == "COMPOSE-CHAIN" and r.get("status") == "ACTIVE_SPECIFIED"), None)
            if rule:
                identity = {"rule": rule["id"], "nodes": path, "sources": provenance}
                candidates.append({
                    "id": "LF-" + canonical_hash(identity)[:14],
                    "composition_rule_id": rule["id"],
                    "member_article_ids": list(path),
                    "member_count": len(path),
                    "source_refs": provenance,
                    "invariants_checked": {
                        "all_members_have_sources": all(bool(a.get("sources")) for a in path_articles),
                        "all_edges_exist_in_catalog": all(path[i+1] in adjacency[path[i]] for i in range(len(path)-1)),
                        "stable_membership_hash": bool(canonical_hash(identity)),
                    },
                    "status": "CANDIDATE_COMPOSITION_NOT_SEMANTICALLY_VERIFIED",
                })
        if len(path) >= max_depth or len(candidates) >= max_candidates:
            return
        for nxt in sorted(adjacency[path[-1]]):
            if nxt not in path:
                walk(path + [nxt])
                if len(candidates) >= max_candidates:
                    return
    for start in sorted(by_id):
        walk([start])
        if len(candidates) >= max_candidates:
            break
    shared: dict[str, list[str]] = {}
    for article in articles:
        for src in article.get("sources", []):
            shared.setdefault(src, []).append(article["id"])
    shared_compositions = []
    for source_id, ids in sorted(shared.items()):
        uniq = sorted(set(ids))
        if len(uniq) >= 2:
            shared_compositions.append({
                "id": "SH-" + canonical_hash([source_id, uniq])[:12],
                "source_ref": source_id,
                "article_ids": uniq,
                "status": "SHARED_SOURCE_ASSOCIATION_NOT_SEMANTIC_ENTAILMENT",
            })
    return {
        "model": "WANGA Logic Fractal Candidate Composer V1",
        "status": "CANDIDATE_MAP_BUILT_NOT_RELEASED",
        "catalog_schema_version": catalog.get("schema_version"),
        "article_count": len(articles),
        "source_count": len(sources),
        "edge_count": len(edges),
        "composition_contract_count": len(contracts),
        "candidate_composition_count": len(candidates),
        "candidate_fractals": candidates,
        "shared_source_compositions": shared_compositions,
        "graph": {
            "nodes": [{"id": a["id"], "title": a["title"], "kind": a["kind"], "status": a["status"], "source_refs": sorted(set(a["sources"]))} for a in sorted(articles, key=lambda x: x["id"])],
            "edges": edges,
        },
        "source_boundary": "Edges are based on the editorial related-entry map in the catalog, not independently proven semantic entailment.",
        "release_status": "NOT_READY_UNLESS_READINESS_GATE_PASSES",
    }
