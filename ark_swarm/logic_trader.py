"""Logic Trader: deterministic selection and packaging of source-linked logic assets.

This is an auditable first implementation of the Logic Trader role. It ranks
Logic Wiki entries and existing composition candidates from lexical task overlap
and catalog links. It does not claim semantic understanding, truth, or model
readiness. Selected packages remain internal candidates until reviewed.
"""
from __future__ import annotations

import hashlib
import json
import re
from typing import Any, Mapping

from logic_fractal.composer import build_candidate_model, load_contracts

TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[\u0590-\u05FF]+", re.UNICODE)
STOP_WORDS = {
    "the", "and", "for", "with", "from", "into", "that", "this", "then", "when",
    "where", "which", "what", "how", "are", "is", "to", "of", "in", "on", "by",
    "a", "an", "or", "as", "it", "be", "can", "should", "will", "model", "task",
    "את", "של", "על", "עם", "כדי", "הוא", "היא", "וכן", "גם", "אשר", "זה", "זאת",
    "איך", "מה", "לבנות", "לבניית", "מתוך", "עבור", "שלנו", "שיש", "יהיה",
}


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def tokenize(text: str) -> list[str]:
    return [m.group(0).casefold() for m in TOKEN_RE.finditer(text) if m.group(0).casefold() not in STOP_WORDS]


def _article_text(article: Mapping[str, Any]) -> str:
    return " ".join(str(article.get(key, "")) for key in (
        "title", "category", "definition", "scope_note", "kind", "status"
    ))


def _validate_catalog(catalog: Mapping[str, Any]) -> dict[str, Any]:
    articles = catalog.get("articles")
    sources = catalog.get("sources")
    if not isinstance(articles, list) or not articles or not isinstance(sources, list) or not sources:
        raise ValueError("Logic Wiki catalog requires non-empty articles and sources arrays")
    article_ids = [item.get("id") for item in articles]
    source_ids = [item.get("id") for item in sources]
    if any(not isinstance(x, str) or not x for x in article_ids) or len(article_ids) != len(set(article_ids)):
        raise ValueError("Logic Wiki article IDs must be unique non-empty strings")
    if any(not isinstance(x, str) or not x for x in source_ids) or len(source_ids) != len(set(source_ids)):
        raise ValueError("Logic Wiki source IDs must be unique non-empty strings")
    known_articles, known_sources = set(article_ids), set(source_ids)
    dangling_sources = sorted({
        source_id for article in articles for source_id in article.get("sources", [])
        if source_id not in known_sources
    })
    dangling_relations = sorted({
        f"{article.get('id')}->{target}" for article in articles for target in article.get("relations", [])
        if target not in known_articles
    })
    if dangling_sources or dangling_relations:
        raise ValueError(json.dumps({
            "dangling_sources": dangling_sources,
            "dangling_relations": dangling_relations,
        }, ensure_ascii=False))
    return {
        "status": "PASS",
        "article_count": len(articles),
        "source_count": len(sources),
        "dangling_source_count": len(dangling_sources),
        "dangling_relation_count": len(dangling_relations),
        "catalog_sha256": canonical_hash(catalog),
    }


def rank_logic_assets(
    task: str,
    catalog: Mapping[str, Any],
    *,
    limit: int = 10,
) -> dict[str, Any]:
    """Rank article-level logic assets by lexical overlap, not inferred meaning."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be non-empty text")
    if not 1 <= limit <= 50:
        raise ValueError("limit must be between 1 and 50")
    _validate_catalog(catalog)
    task_tokens = sorted(set(tokenize(task)))
    if not task_tokens:
        task_tokens = sorted(set(TOKEN_RE.findall(task.casefold())))
    query = set(task_tokens)
    ranked = []
    for article in catalog["articles"]:
        tokens = set(tokenize(_article_text(article)))
        overlap = sorted(query & tokens)
        coverage = len(overlap) / max(1, len(query))
        source_count = len(set(article.get("sources", [])))
        relation_count = len(set(article.get("relations", [])))
        # Small metadata tie-breakers only; lexical overlap remains the main signal.
        score = coverage + min(source_count, 3) * 0.01 + min(relation_count, 3) * 0.005
        ranked.append({
            "article_id": article["id"],
            "title": article.get("title", article["id"]),
            "category": article.get("category", ""),
            "kind": article.get("kind", "UNCLASSIFIED"),
            "status": article.get("status", "UNKNOWN"),
            "source_refs": sorted(set(article.get("sources", []))),
            "related_ids": sorted(set(article.get("relations", []))),
            "matched_terms": overlap,
            "lexical_coverage": round(coverage, 6),
            "selection_score": round(score, 6),
            "selection_method": "LEXICAL_OVERLAP_WITH_SMALL_SOURCE_AND_RELATION_TIE_BREAKERS",
            "semantic_relevance": "NOT_ESTABLISHED",
        })
    ranked.sort(key=lambda row: (-row["selection_score"], row["article_id"]))
    return {
        "status": "RANKED_CANDIDATES_NOT_SEMANTICALLY_VERIFIED",
        "task_sha256": canonical_hash(task),
        "task_terms": task_tokens,
        "candidate_count": len(ranked),
        "selected_assets": ranked[:limit],
        "ranking_limitations": [
            "Lexical overlap is not semantic relevance and may miss synonyms or context.",
            "An article status is preserved and is not promoted by this ranking.",
            "Source references identify catalog records; they do not independently authenticate the sources.",
        ],
    }


def trade_logic(
    task: str,
    catalog: Mapping[str, Any],
    contracts: list[dict[str, Any]],
    *,
    max_depth: int = 3,
    max_candidates: int = 2000,
    top_assets: int = 10,
    top_compositions: int = 10,
) -> dict[str, Any]:
    """Build a catalog graph, rank logic assets, and create an inspectable candidate package."""
    catalog_audit = _validate_catalog(catalog)
    ranked = rank_logic_assets(task, catalog, limit=top_assets)
    composition = build_candidate_model(
        catalog, contracts, max_depth=max_depth, max_candidates=max_candidates
    )
    articles_by_id = {article["id"]: article for article in catalog["articles"]}
    sources_by_id = {source["id"]: source for source in catalog["sources"]}
    scores = {row["article_id"]: row for row in ranked["selected_assets"]}

    candidate_rows = []
    for candidate in composition["candidate_fractals"]:
        member_ids = candidate["member_article_ids"]
        member_scores = [
            scores.get(article_id, {
                "selection_score": _score_one(articles_by_id[article_id], ranked["task_terms"]),
                "matched_terms": sorted(set(ranked["task_terms"]) & set(tokenize(_article_text(articles_by_id[article_id])))),
            })
            for article_id in member_ids
        ]
        mean_score = sum(float(row["selection_score"]) for row in member_scores) / len(member_scores)
        source_refs = sorted(set(candidate["source_refs"]))
        candidate_rows.append({
            "candidate_id": candidate["id"],
            "member_article_ids": member_ids,
            "member_titles": [articles_by_id[item].get("title", item) for item in member_ids],
            "source_refs": source_refs,
            "source_count": len(source_refs),
            "composition_rule_id": candidate["composition_rule_id"],
            "member_lexical_scores": [round(float(row["selection_score"]), 6) for row in member_scores],
            "selection_score": round(mean_score + min(len(source_refs), 4) * 0.005, 6),
            "invariants_checked": candidate["invariants_checked"],
            "status": "INTERNAL_CANDIDATE_NOT_RELEASED",
            "semantic_entailment": "NOT_ESTABLISHED",
        })
    candidate_rows.sort(key=lambda row: (-row["selection_score"], -row["source_count"], row["candidate_id"]))
    selected_compositions = candidate_rows[:top_compositions]
    selected_assets = ranked["selected_assets"]
    selected_article_ids = {row["article_id"] for row in selected_assets}
    chosen = selected_compositions[0] if selected_compositions else None
    chosen_ids = chosen["member_article_ids"] if chosen else sorted(selected_article_ids)[:top_assets]
    chosen_sources = sorted({
        source_id
        for article_id in chosen_ids
        for source_id in articles_by_id[article_id].get("sources", [])
    })
    package_payload = {
        "task_sha256": canonical_hash(task),
        "article_ids": chosen_ids,
        "composition_candidate_id": chosen["candidate_id"] if chosen else None,
        "source_refs": chosen_sources,
        "composition_rule_id": chosen["composition_rule_id"] if chosen else None,
    }
    logic_package = {
        "package_id": "LT-" + canonical_hash(package_payload)[:16],
        "version": "0.1",
        "status": "INTERNAL_CANDIDATE_NOT_RELEASED",
        "task": task,
        "task_sha256": canonical_hash(task),
        "member_articles": [
            {
                "id": article_id,
                "title": articles_by_id[article_id].get("title", article_id),
                "kind": articles_by_id[article_id].get("kind", "UNCLASSIFIED"),
                "status": articles_by_id[article_id].get("status", "UNKNOWN"),
                "definition": articles_by_id[article_id].get("definition", ""),
                "source_refs": sorted(set(articles_by_id[article_id].get("sources", []))),
                "relation_refs": sorted(set(articles_by_id[article_id].get("relations", []))),
            }
            for article_id in chosen_ids
        ],
        "sources": [sources_by_id[source_id] for source_id in chosen_sources],
        "composition_candidate": chosen,
        "semantic_status": "NOT_YET_VERIFIED",
        "model_hash": canonical_hash(package_payload),
        "boundary": "This is a selected research package candidate, not an executable proof or released model.",
    }
    return {
        "trader": "WANGA Logic Trader V1",
        "status": "CANDIDATE_PACKAGE_ASSEMBLED",
        "task": task,
        "catalog_audit": catalog_audit,
        "ranking": ranked,
        "composition_graph": {
            "status": composition["status"],
            "node_count": len(composition["graph"]["nodes"]),
            "edge_count": composition["edge_count"],
            "candidate_composition_count": composition["candidate_composition_count"],
            "shared_source_composition_count": len(composition["shared_source_compositions"]),
            "source_boundary": composition["source_boundary"],
        },
        "candidate_compositions": selected_compositions,
        "logic_package": logic_package,
        "package_hash": canonical_hash(logic_package),
        "semantic_status": "NOT_YET_VERIFIED",
    }


def _score_one(article: Mapping[str, Any], task_terms: list[str]) -> float:
    tokens = set(tokenize(_article_text(article)))
    coverage = len(set(task_terms) & tokens) / max(1, len(task_terms))
    return round(coverage + min(len(article.get("sources", [])), 3) * 0.01
                 + min(len(article.get("relations", [])), 3) * 0.005, 6)
