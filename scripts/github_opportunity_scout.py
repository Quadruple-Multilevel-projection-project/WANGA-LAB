#!/usr/bin/env python3
"""Read-only GitHub opportunity discovery for AI231/WANGA."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

QUERIES = [
    ("agent operations, evaluation and guardrails", "agent observability evaluation guardrails sandbox orchestration"),
    ("multi-agent orchestration and durable workflows", "multi-agent workflow orchestration durable execution"),
    ("AI verification, testing and drift control", "LLM agent verification testing drift detection"),
    ("robotics and embodied AI", "open source robotics embodied AI simulation"),
    ("open research infrastructure and interoperability", "AI research infrastructure interoperability open source"),
]
ORG_CONTEXT = "AI231/WANGA: agent factory, logical processor, verification, robotics, public-benefit research; revenue-first, paid validation, positive contribution margin."
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"

def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)

seen = {}
errors = []
for label, terms in QUERIES:
    query = urllib.parse.urlencode({"q": terms + " fork:false", "sort": "updated", "order": "desc", "per_page": 12})
    try:
        data = get("https://api.github.com/search/repositories?" + query)
        for repo in data.get("items", []):
            full_name = repo.get("full_name")
            if not full_name:
                continue
            item = {
                "name": full_name,
                "url": repo.get("html_url"),
                "description": repo.get("description"),
                "stars": repo.get("stargazers_count"),
                "language": repo.get("language"),
                "license": (repo.get("license") or {}).get("spdx_id"),
                "pushed_at": repo.get("pushed_at"),
                "topics": repo.get("topics", []),
                "discovery_tracks": [label],
            }
            if full_name in seen:
                seen[full_name]["discovery_tracks"].append(label)
            else:
                seen[full_name] = item
    except Exception as exc:
        errors.append({"track": label, "error": str(exc)})

items = sorted(seen.values(), key=lambda x: (len(x["discovery_tracks"]), x["stars"] or 0, x["pushed_at"] or ""), reverse=True)
out = Path("reports/opportunity-scout")
out.mkdir(parents=True, exist_ok=True)
stamp = datetime.now(timezone.utc).isoformat()
payload = {"generated_at": stamp, "organization_context": ORG_CONTEXT, "source": "GitHub repository search API", "read_only": True, "candidates": items[:30], "errors": errors}
(out / "candidates.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
lines = ["# AI231 GitHub Opportunity Scout", "", f"Generated: {stamp}", "", f"Scope: {ORG_CONTEXT}", "", "This is a discovery shortlist, not an endorsement. Review license, maintenance, security, fit, dependencies and deployment constraints before adoption.", ""]
for i, item in enumerate(items[:15], 1):
    lines += [f"## {i}. [{item['name']}]({item['url']})", item.get("description") or "No repository description.", f"- Stars: {item['stars']} | Language: {item['language']} | License: {item['license']}", f"- Last push: {item['pushed_at']} | Tracks: {', '.join(item['discovery_tracks'])}", ""]
if not items:
    lines += ["No candidate repositories were returned.", ""]
if errors:
    lines += ["## Search errors", *[f"- {e['track']}: {e['error']}" for e in errors], ""]
(out / "daily-report.md").write_text("\n".join(lines), encoding="utf-8")
print(f"candidates={len(items)} errors={len(errors)} generated_at={stamp}")
