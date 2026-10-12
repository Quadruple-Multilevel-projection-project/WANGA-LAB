#!/usr/bin/env python3
"""Bounded, privacy-aware GitHub ecosystem scan agent.

Scans only public repository contents into artifacts. Cross-repo discovery
requires an explicitly configured CROSS_REPO_READ_TOKEN. Private repository
names, file paths, and content are never copied to this report. This is a
collector/indexing agent, not an LLM or semantic-verification engine.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable, Mapping

API = "https://api.github.com"
USER_AGENT = "WANGA-Ecosystem-Research-Agent/1.0"
RELEVANCE = re.compile(
    r"logic|fractal|neural|agent|wanga|model|reason|research|orchestrat|"
    r"quantum|govern|ark|drift|knowledge|evidence|provenance|ontology|"
    r"capabilit|source|thought|ntm|mln|vitruvius",
    re.IGNORECASE,
)
DOC_PATH = re.compile(
    r"(^|/)[^/]*(readme|agents|architecture|research|logic|fractal|ntm|mln|"
    r"agent|model|orchestrat|provenance|evidence|manifest|schema|workflow|"
    r"capabilit|registry|thought|wiki)[^/]*(/|$)",
    re.IGNORECASE,
)


class GitHubScanError(RuntimeError):
    pass


def github_get(url: str, token: str, *, accept: str = "application/vnd.github+json") -> Any:
    request = urllib.request.Request(
        url,
        headers={
            "Accept": accept,
            "Authorization": f"Bearer {token}" if token else "",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = response.read()
            content_type = response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise GitHubScanError(f"GitHub API HTTP {exc.code}: {detail}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise GitHubScanError(f"GitHub API unavailable: {exc}") from exc
    if "application/json" in content_type or payload[:1] in (b"{", b"["):
        try:
            return json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise GitHubScanError("GitHub API returned malformed JSON") from exc
    return payload


def list_accessible_repositories(token: str, *, max_pages: int = 10) -> list[dict[str, Any]]:
    repositories: list[dict[str, Any]] = []
    for page in range(1, max_pages + 1):
        url = (
            f"{API}/user/repos?affiliation=owner%2Ccollaborator%2Corganization_member"
            f"&per_page=100&page={page}&sort=updated"
        )
        payload = github_get(url, token)
        if not isinstance(payload, list):
            raise GitHubScanError("Repository inventory endpoint did not return a list")
        repositories.extend(item for item in payload if isinstance(item, dict))
        if len(payload) < 100:
            break
    # Stable identity is full_name; preserve one item per repository.
    unique: dict[str, dict[str, Any]] = {}
    for repository in repositories:
        full_name = str(repository.get("full_name") or "").strip()
        if full_name:
            unique[full_name.casefold()] = repository
    return sorted(unique.values(), key=lambda item: str(item.get("full_name", "")).casefold())


def decode_readme(repository: Mapping[str, Any], token: str) -> tuple[str, str]:
    full_name = str(repository.get("full_name", ""))
    if not full_name:
        raise GitHubScanError("Repository response omitted full_name")
    branch = str(repository.get("default_branch") or "main")
    query = urllib.parse.urlencode({"ref": branch})
    payload = github_get(f"{API}/repos/{full_name}/readme?{query}", token)
    if not isinstance(payload, dict):
        raise GitHubScanError("README endpoint returned an unexpected payload")
    content = payload.get("content")
    encoding = payload.get("encoding")
    if encoding != "base64" or not isinstance(content, str):
        raise GitHubScanError("README response lacks base64 content")
    try:
        decoded = base64.b64decode(content).decode("utf-8", errors="replace")
    except ValueError as exc:
        raise GitHubScanError("README could not be decoded") from exc
    return decoded, str(payload.get("html_url") or repository.get("html_url", ""))


def relevant_paths(repository: Mapping[str, Any], token: str, *, max_paths: int = 40) -> list[str]:
    full_name = str(repository.get("full_name", ""))
    branch = str(repository.get("default_branch") or "main")
    encoded_branch = urllib.parse.quote(branch, safe="")
    payload = github_get(f"{API}/repos/{full_name}/git/trees/{encoded_branch}?recursive=1", token)
    if not isinstance(payload, dict) or not isinstance(payload.get("tree"), list):
        raise GitHubScanError("Repository tree endpoint returned an unexpected payload")
    paths = []
    for item in payload["tree"]:
        path = str(item.get("path") or "")
        if item.get("type") == "blob" and DOC_PATH.search(path):
            paths.append(path)
    return sorted(set(paths), key=lambda p: (0 if p.casefold().endswith("readme.md") else 1, p.casefold()))[:max_paths]


def summarize_readme(text: str, *, max_chars: int = 500) -> dict[str, Any]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    title = next((line.lstrip("# ").strip() for line in lines if line.startswith("#")), "")
    excerpt_lines: list[str] = []
    for line in lines:
        if line.startswith("#") or line.startswith("![") or line.startswith("<"):
            continue
        excerpt_lines.append(line)
        if sum(len(x) + 1 for x in excerpt_lines) >= max_chars:
            break
    excerpt = " ".join(excerpt_lines)
    excerpt = re.sub(r"\s+", " ", excerpt)[:max_chars]
    material = " ".join([title, excerpt])
    signals = sorted({match.group(0).casefold() for match in RELEVANCE.finditer(material)})
    return {
        "title": title[:180],
        "excerpt": excerpt,
        "relevance_signals": signals,
        "relevance_candidate": bool(signals),
        "semantic_status": "README_SURFACE_CUES_ONLY",
    }


def select_batch(items: list[dict[str, Any]], *, limit: int, run_number: int) -> tuple[list[dict[str, Any]], int]:
    if limit < 1:
        raise ValueError("limit must be >= 1")
    if not items:
        return [], 0
    batches_per_cycle = (len(items) + limit - 1) // limit
    batch_index = max(0, run_number - 1) % batches_per_cycle
    start = batch_index * limit
    selected = items[start:start + limit]
    next_cursor = (start + len(selected)) % len(items)
    return selected, next_cursor


def _public_record(repository: Mapping[str, Any], token: str) -> dict[str, Any]:
    full_name = str(repository.get("full_name") or "")
    private = repository.get("private")
    if private is not False:
        # Fail closed: unknown visibility is treated like private.
        return {"status": "SKIPPED_PRIVATE_OR_VISIBILITY_UNKNOWN"}
    safe = {
        "full_name": full_name,
        "html_url": repository.get("html_url", f"https://github.com/{full_name}"),
        "default_branch": repository.get("default_branch") or "",
        "updated_at": repository.get("updated_at"),
        "archived": bool(repository.get("archived", False)),
        "visibility": "public",
    }
    try:
        readme, readme_url = decode_readme(repository, token)
        safe["readme_url"] = readme_url
        safe["readme_sha256"] = __import__("hashlib").sha256(readme.encode("utf-8")).hexdigest()
        safe["readme"] = summarize_readme(readme)
    except (GitHubScanError, ValueError) as exc:
        safe["readme"] = {"status": "BLOCKED_OR_MISSING", "reason": str(exc)[:240]}
    try:
        paths = relevant_paths(repository, token)
        safe["relevant_paths"] = paths
        safe["relevant_path_count"] = len(paths)
    except (GitHubScanError, ValueError) as exc:
        safe["relevant_paths_status"] = "BLOCKED_OR_MISSING"
        safe["relevant_paths_error"] = str(exc)[:240]
    safe["scan_status"] = "SCANNED_PUBLIC_METADATA_AND_README"
    return safe


def build_scan(token: str, *, limit: int, run_number: int, current_repo: str = "") -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    cross_token_configured = bool(os.environ.get("CROSS_REPO_READ_TOKEN"))
    try:
        all_repos = list_accessible_repositories(token)
        mode = "CROSS_REPO_INVENTORY_AVAILABLE"
        inventory_error = None
    except GitHubScanError as exc:
        mode = "CURRENT_REPOSITORY_ONLY"
        inventory_error = str(exc)
        name = current_repo or os.environ.get("GITHUB_REPOSITORY", "")
        if not name or "/" not in name:
            raise GitHubScanError(
                "Cross-repo inventory is blocked and GITHUB_REPOSITORY is not set; "
                "configure CROSS_REPO_READ_TOKEN for a full sweep."
            ) from exc
        current = github_get(f"{API}/repos/{name}", token)
        if not isinstance(current, dict):
            raise GitHubScanError("Unable to read current repository metadata") from exc
        all_repos = [current]

    private_count = sum(1 for r in all_repos if r.get("private") is True)
    unknown_visibility_count = sum(1 for r in all_repos if r.get("private") is None)
    public_repos = [r for r in all_repos if r.get("private") is False]
    public_repos.sort(key=lambda item: str(item.get("full_name", "")).casefold())
    selected, next_cursor = select_batch(public_repos, limit=limit, run_number=run_number)
    records: list[dict[str, Any]] = []
    for repository in selected:
        records.append(_public_record(repository, token))
    output_records = [r for r in records if r.get("status") != "SKIPPED_PRIVATE_OR_VISIBILITY_UNKNOWN"]
    relevant = [r for r in output_records if (r.get("readme") or {}).get("relevance_candidate")]
    return {
        "schema_version": "wanga-ecosystem-scan/1.0",
        "generated_at_utc": now,
        "agent": "repository-inventory-and-material-collector",
        "status": "COMPLETED" if mode == "CROSS_REPO_INVENTORY_AVAILABLE" else "COMPLETED_WITH_SCOPE_BLOCKER",
        "scope": {
            "mode": mode,
            "cross_repo_token_configured": cross_token_configured,
            "repository_count_returned": len(all_repos),
            "public_repository_count": len(public_repos),
            "private_repository_count_redacted": private_count,
            "unknown_visibility_count_redacted": unknown_visibility_count,
            "readme_batch_limit": limit,
            "run_number": run_number,
            "selected_count": len(records),
            "next_cursor_public_repos": next_cursor,
            "inventory_error": inventory_error,
            "private_content_policy": "No private or unknown-visibility repository names, file paths, README excerpts or contents are emitted.",
        },
        "results": output_records,
        "summary": {
            "repositories_scanned": len(output_records),
            "relevant_candidate_count": len(relevant),
            "relevant_candidate_repositories": [r["full_name"] for r in relevant],
            "content_interpretation": "README cues and file-path names produce discovery candidates only; no semantic claim is verified.",
        },
        "access_gaps": [] if mode == "CROSS_REPO_INVENTORY_AVAILABLE" else [
            "Cross-repository GitHub inventory is unavailable without CROSS_REPO_READ_TOKEN with approved scopes. This run covers only the current repository.",
        ],
        "next_action": "Continue with the next deterministic public-repository batch; use the connected WANGA work loop for authorized private repositories and Library material.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="WANGA cross-repository public material collector")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--run-number", type=int, default=int(os.environ.get("GITHUB_RUN_NUMBER", "1")))
    parser.add_argument("--current-repo", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--out-dir", default="ecosystem-scan-output")
    args = parser.parse_args(argv)
    token = os.environ.get("CROSS_REPO_READ_TOKEN", "").strip()
    if not token:
        # GITHUB_TOKEN is deliberately not treated as an account-wide token.
        token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        print(json.dumps({"status": "BLOCKED", "reason": "NO_GITHUB_TOKEN", "private_content_published": False}))
        return 2
    try:
        report = build_scan(token, limit=args.limit, run_number=args.run_number, current_repo=args.current_repo)
    except (GitHubScanError, ValueError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc), "private_content_published": False}))
        return 2
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "ecosystem-scan-report.json"
    markdown_path = out_dir / "ecosystem-scan-report.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# WANGA GitHub Ecosystem Sweep",
        "",
        f"- Status: **{report['status']}**",
        f"- Scan mode: `{report['scope']['mode']}`",
        f"- Repositories returned: {report['scope']['repository_count_returned']}",
        f"- Public repositories in index: {report['scope']['public_repository_count']}",
        f"- Private repositories redacted: {report['scope']['private_repository_count_redacted']}",
        f"- Batch size: {report['scope']['selected_count']}",
        f"- Relevant candidates found: {report['summary']['relevant_candidate_count']}",
        "",
        "## Scanned public repositories",
    ]
    for item in report["results"]:
        readme = item.get("readme") or {}
        lines.append(f"- [{item['full_name']}]({item.get('html_url', '')}) — {readme.get('title') or 'README unavailable'}; relevance candidate={readme.get('relevance_candidate', False)}")
        if readme.get("excerpt"):
            lines.append(f"  - {readme['excerpt']}")
        if item.get("relevant_paths"):
            lines.append(f"  - Candidate paths: {', '.join(item['relevant_paths'][:12])}")
    if report["access_gaps"]:
        lines += ["", "## Access gaps"] + [f"- {gap}" for gap in report["access_gaps"]]
    lines += [
        "",
        "## Epistemic boundary",
        "This is a source-discovery report. README cues, repository names, and paths are not proof of semantic relationships, implementations, or correctness.",
        "Private or unknown-visibility repositories are redacted. No repository is modified and no Wix publication occurs in this workflow.",
        "",
    ]
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "mode": report["scope"]["mode"],
        "repositories_returned": report["scope"]["repository_count_returned"],
        "public_batch_scanned": report["scope"]["selected_count"],
        "private_repositories_redacted": report["scope"]["private_repository_count_redacted"],
        "relevant_candidates": report["summary"]["relevant_candidate_count"],
        "json_report": str(json_path),
        "markdown_report": str(markdown_path),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
