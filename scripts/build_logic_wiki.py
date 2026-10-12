#!/usr/bin/env python3
"""Build and validate the WANGA Logic Wiki from versioned JSON records."""
from __future__ import annotations
import argparse, datetime, html, json, re, sys
from pathlib import Path

ROOT_DEFAULT = Path(__file__).resolve().parents[1]
ALLOWED_KINDS = {
  "ESTABLISHED_REFERENCE", "WANGA_ENGINEERING_CONCEPT", "WANGA_ARCHITECTURE_CONTRACT",
  "WANGA_RESEARCH_PROPOSAL", "WANGA_IMPLEMENTED_PROTOTYPE", "WANGA_RESEARCH_PROTOTYPE",
  "WANGA_PROCESS_PROPOSAL", "WANGA_INFRASTRUCTURE"
}

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate(root):
    catalog = load_json(root / "logic_wiki/data/articles.json")
    gate = load_json(root / "logic_wiki/data/readiness_gate.json")
    agents = load_json(root / "logic_wiki/data/agent_registry.json")
    articles = catalog.get("articles", [])
    sources = catalog.get("sources", [])
    errors, warnings = [], []
    article_ids = [a.get("id") for a in articles]
    source_ids = [s.get("id") for s in sources]
    if len(article_ids) != len(set(article_ids)) or any(not x for x in article_ids):
        errors.append("Duplicate or empty article IDs.")
    if len(source_ids) != len(set(source_ids)) or any(not x for x in source_ids):
        errors.append("Duplicate or empty source IDs.")
    aid, sid = set(article_ids), set(source_ids)
    for article in articles:
        for field in ("id", "title", "category", "kind", "status", "definition", "scope_note", "sources", "relations"):
            if field not in article:
                errors.append("Article %r missing required field %s." % (article.get("id"), field))
        if article.get("kind") not in ALLOWED_KINDS:
            errors.append("Article %r has unknown kind %r." % (article.get("id"), article.get("kind")))
        for ref in article.get("sources", []):
            if ref not in sid:
                errors.append("Article %s has dangling source reference %s." % (article.get("id"), ref))
        for ref in article.get("relations", []):
            if ref not in aid:
                errors.append("Article %s has dangling relation %s." % (article.get("id"), ref))
        if article.get("kind") != "ESTABLISHED_REFERENCE" and not article.get("scope_note"):
            errors.append("Non-reference article %s must declare scope_note." % article.get("id"))
    for source in sources:
        if not source.get("uri") or not source.get("status"):
            errors.append("Source %r missing URI or status." % source.get("id"))
    if not articles:
        errors.append("No wiki articles configured.")
    if not agents.get("agents"):
        errors.append("No agent contracts configured.")
    source_classes = sorted(set(s.get("type", "UNKNOWN") for s in sources))
    metrics_path = root / "logic_wiki/data/research_metrics.json"
    metrics = load_json(metrics_path) if metrics_path.exists() else {}
    observed = {
        "source_records": len(sources) + int(metrics.get("additional_source_records", 0)),
        "source_classes": len(set(source_classes) | set(metrics.get("additional_source_classes", []))),
        "logic_units_with_provenance": sum(1 for a in articles if a.get("sources")) + int(metrics.get("additional_logic_units_with_provenance", 0)),
        "composition_rules_with_contracts": int(metrics.get("composition_rules_with_contracts", 0)),
        "counterexample_cases": int(metrics.get("counterexample_cases", 0)),
        "test_cases": int(metrics.get("test_cases", 0)),
        "benchmark_suites": int(metrics.get("benchmark_suites", 0)),
        "independent_review_cycles": int(metrics.get("independent_review_cycles", 0)),
        "unresolved_dangling_source_refs": sum(1 for e in errors if "dangling source" in e),
        "unresolved_duplicate_stable_ids": sum(1 for e in errors if "Duplicate or empty" in e),
        "critical_core_contradictions": int(metrics.get("critical_core_contradictions", 0)),
        "deterministic_build": bool(metrics.get("deterministic_build", False)),
        "holdout_split": bool(metrics.get("holdout_split", False)),
        "mirror_review": bool(metrics.get("mirror_review", False)),
    }
    required = gate["thresholds"]
    checks = {
        "source_records": observed["source_records"] >= required["min_source_records"],
        "source_classes": observed["source_classes"] >= required["min_source_classes"],
        "logic_units_with_provenance": observed["logic_units_with_provenance"] >= required["min_logic_units_with_provenance"],
        "composition_rules_with_contracts": observed["composition_rules_with_contracts"] >= required["min_composition_rules_with_contracts"],
        "counterexample_cases": observed["counterexample_cases"] >= required["min_counterexample_cases"],
        "test_cases": observed["test_cases"] >= required["min_test_cases"],
        "benchmark_suites": observed["benchmark_suites"] >= required["min_benchmark_suites"],
        "independent_review_cycles": observed["independent_review_cycles"] >= required["min_independent_review_cycles"],
        "unresolved_dangling_source_refs": observed["unresolved_dangling_source_refs"] <= required["unresolved_dangling_source_refs"],
        "unresolved_duplicate_stable_ids": observed["unresolved_duplicate_stable_ids"] <= required["unresolved_duplicate_stable_ids"],
        "critical_core_contradictions": observed["critical_core_contradictions"] <= required["critical_core_contradictions"],
        "deterministic_build_required": (not required["deterministic_build_required"]) or observed["deterministic_build"],
        "holdout_split_required": (not required["holdout_split_required"]) or observed["holdout_split"],
        "mirror_review_required": (not required["mirror_review_required"]) or observed["mirror_review"],
    }
    report = {
        "date": datetime.date.today().isoformat(), "status": "PASS" if not errors else "FAIL",
        "article_count": len(articles), "source_count": len(sources), "source_classes": source_classes,
        "relation_edge_count": sum(len(a.get("relations", [])) for a in articles),
        "agent_contract_count": len(agents.get("agents", [])), "errors": errors, "warnings": warnings,
        "readiness_gate": gate["gate_id"], "readiness_gate_status": "CANDIDATE_RELEASE_READY_FOR_HUMAN_REVIEW" if all(checks.values()) and not errors else "NOT_READY_INTERNAL_CANDIDATE_ONLY",
        "readiness_thresholds_status": gate["status"], "observed": observed, "checks": checks,
        "missing_requirements": [k for k, passed in checks.items() if not passed],
        "important_limit": "Passing catalog validation does not establish semantic truth or intelligence. Readiness thresholds are provisional project policy.",
    }
    return catalog, gate, report

def render(root, out):
    catalog, gate, report = validate(root)
    articles = catalog["articles"]
    sources = {s["id"]: s for s in catalog["sources"]}
    by_id = {a["id"]: a for a in articles}
    out.mkdir(parents=True, exist_ok=True)
    article_dir = out / "articles"
    article_dir.mkdir(parents=True, exist_ok=True)
    categories = {}
    for a in articles:
        categories.setdefault(a["category"], []).append(a)
        rows = [
            "# " + a["title"], "",
            "**Stable ID:** %s  " % a["id"],
            "**Kind:** %s  " % a["kind"],
            "**Status:** %s" % a["status"], "",
            "## Definition", "", a["definition"], "",
            "## Scope and limitations", "", a["scope_note"], "",
            "## Sources", ""
        ]
        for ref in a.get("sources", []):
            s = sources[ref]
            rows.append("- [%s](%s) — %s (%s)." % (s["title"], s["uri"], s["id"], s["status"]))
        rows += ["", "## Related entries", ""]
        for ref in a.get("relations", []):
            rows.append("- [%s](%s.md)" % (by_id[ref]["title"], ref))
        rows += ["", "---", "Generated from versioned source records; status is not upgraded by generation.", ""]
        (article_dir / (a["id"] + ".md")).write_text("\n".join(rows), encoding="utf-8")
    index = {
        "schema_version": "logic-wiki-generated/1.0", "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "articles": [{"id": a["id"], "title": a["title"], "category": a["category"], "kind": a["kind"], "status": a["status"], "definition": a["definition"], "url": "articles/%s.md" % a["id"], "sources": a["sources"], "relations": a["relations"]} for a in articles],
        "sources": catalog["sources"], "readiness_gate": report
    }
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# WANGA Logic Wiki", "", "Generated: %s" % report["date"], "", "## Status", "",
          "- Articles: %s" % report["article_count"], "- Registered sources: %s" % report["source_count"],
          "- Relation edges: %s" % report["relation_edge_count"], "- Research agents: %s" % report["agent_contract_count"],
          "- First-model gate: **%s**" % report["readiness_gate_status"], "",
          "This is a source-linked research wiki. A reference does not automatically verify a claim.", ""]
    for category in sorted(categories):
        md += ["## " + category, ""]
        for a in sorted(categories[category], key=lambda x: x["title"].casefold()):
            md.append("- [%s](articles/%s.md) — %s (%s)." % (a["title"], a["id"], a["status"], a["kind"]))
        md.append("")
    md += ["## Research sources", ""]
    for s in catalog["sources"]:
        md.append("- [%s](%s) — %s." % (s["title"], s["uri"], s["status"]))
    (out / "INDEX.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    cards = []
    for a in articles:
        source_links = " ".join('<a href="%s">%s</a>' % (html.escape(sources[r]["uri"], quote=True), html.escape(sources[r]["title"])) for r in a["sources"])
        rel_links = " ".join('<a href="#%s">%s</a>' % (html.escape(r, quote=True), html.escape(by_id[r]["title"])) for r in a["relations"])
        cards.append('<article class="entry" id="%s" data-search="%s"><div class="meta">%s · %s</div><h2>%s</h2><p>%s</p><p class="scope"><b>Boundary:</b> %s</p><p><b>Sources:</b> %s</p><p><b>Related:</b> %s</p></article>' % (
          html.escape(a["id"], quote=True), html.escape((a["title"]+" "+a["category"]+" "+a["definition"]).casefold(), quote=True),
          html.escape(a["kind"]), html.escape(a["status"]), html.escape(a["title"]), html.escape(a["definition"]),
          html.escape(a["scope_note"]), source_links, rel_links))
    page_template = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>WANGA Logic Wiki</title>
    <style>body{font:16px/1.6 system-ui,sans-serif;max-width:1100px;margin:auto;padding:24px;background:#f6f7f3;color:#19251f}header,.entry{background:#fff;border:1px solid #d9dfd8;border-radius:12px;padding:18px;margin:14px 0}h1{font-size:2.4rem}input{width:100%;padding:12px;border:1px solid #aab5ab;border-radius:8px;font-size:1rem}.meta{font-size:.8rem;color:#27684f;text-transform:uppercase}.scope{color:#5e685f}a{color:#27684f}</style>
    </head><body><header><p>WANGA-LAB · RESEARCH ENCYCLOPEDIA</p><h1>Logic Wiki</h1><p>Versioned concepts, source-linked claims, logical relations and candidate fractal compositions.</p>
    <input id="q" placeholder="Search terms, relations, or status…" aria-label="Search wiki"><p id="status"></p><p>First-model gate: __GATE_STATUS__. Source references and project proposals have separate status.</p></header>__ARTICLE_CARDS__
    <script>const q=document.getElementById("q"),items=[...document.querySelectorAll(".entry")],status=document.getElementById("status");function filter(){let term=q.value.toLowerCase().trim(),n=0;for(const e of items){let show=!term||e.dataset.search.includes(term)||e.innerText.toLowerCase().includes(term);e.hidden=!show;if(show)n++}status.textContent=n+" entries shown"}q.addEventListener("input",filter);filter();</script></body></html>"""
    page = page_template.replace("__GATE_STATUS__", html.escape(report["readiness_gate_status"])).replace("__ARTICLE_CARDS__", "\n".join(cards))
    (out / "index.html").write_text(page, encoding="utf-8")
    report_path = out / "readiness-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    date_dir = root / "research/reports/logic-fractal"
    date_dir.mkdir(parents=True, exist_ok=True)
    lines = ["# Logic Fractal Research Cycle", "", "Date: %s" % report["date"], "",
      "## Corpus status", "- Wiki articles: %s" % report["article_count"], "- Source records: %s" % report["source_count"],
      "- Relation edges: %s" % report["relation_edge_count"], "- Agent contracts: %s" % report["agent_contract_count"],
      "- Structural validation: %s" % report["status"], "", "## First-model readiness",
      "- Gate: %s" % report["readiness_gate"], "- Status: %s" % report["readiness_gate_status"],
      "- Threshold type: %s" % report["readiness_thresholds_status"], "", "### Checks"]
    for name, passed in report["checks"].items():
        lines.append("- [%s] %s (observed: %s)" % ("x" if passed else " ", name, report["observed"].get(name)))
    lines += ["", "### Missing requirements"] + (["- " + x for x in report["missing_requirements"]] or ["- None detected by configured gate."])
    lines += ["", "## Errors"] + (["- " + x for x in report["errors"]] or ["- None."])
    lines += ["", "## Limitations", report["important_limit"], "Conversation material is only available to this build when exported or committed to the intake folder.", ""]
    report_md = date_dir / (report["date"] + ".md")
    report_md.write_text("\n".join(lines), encoding="utf-8")
    return report

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT_DEFAULT)
    p.add_argument("--out", type=Path, default=Path("logic_wiki/generated"))
    args = p.parse_args()
    root = args.root.resolve()
    out = args.out if args.out.is_absolute() else (root / args.out)
    try:
        report = render(root, out)
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status":"FAIL","error":str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps({"status":report["status"],"articles":report["article_count"],"sources":report["source_count"],"gate":report["readiness_gate_status"],"errors":report["errors"],"output":str(out)}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 2

if __name__ == '__main__':
    raise SystemExit(main())