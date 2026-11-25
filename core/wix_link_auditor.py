"""Deterministic classification of local links in an authorized Wix site snapshot.

This module does not fetch URLs or infer that a Wix dynamic route is missing.
It compares normalized local paths with a supplied file inventory only.
"""
from __future__ import annotations

import posixpath
from enum import Enum
from urllib.parse import unquote, urlsplit


class LinkStatus(str, Enum):
    """Possible outcomes for a link found in a static HTML snapshot."""

    FOUND_STATIC = "FOUND_STATIC"
    MISSING_STATIC = "MISSING_STATIC"
    UNRESOLVED_DYNAMIC_ROUTE = "UNRESOLVED_DYNAMIC_ROUTE"
    EXTERNAL = "EXTERNAL"
    ANCHOR = "ANCHOR"
    INVALID_LOCAL_PATH = "INVALID_LOCAL_PATH"


class PublicationStatus(str, Enum):
    """Fail-closed result when Wix publication signals are compared."""

    CONSISTENT_PUBLISHED = "CONSISTENT_PUBLISHED"
    CONSISTENT_UNPUBLISHED = "CONSISTENT_UNPUBLISHED"
    STATUS_CONFLICT = "STATUS_CONFLICT"
    UNRESOLVED_MISSING_EVIDENCE = "UNRESOLVED_MISSING_EVIDENCE"
    UNRESOLVED_INVALID_EVIDENCE = "UNRESOLVED_INVALID_EVIDENCE"


def classify_publication_state(
    site_context_published: bool | None,
    page_inventory_published: bool | None,
) -> PublicationStatus:
    """Compare independent Wix publication signals without guessing.

    A conflict blocks any public/live status claim. Missing or malformed
    evidence remains unresolved rather than being coerced to False.
    """
    if site_context_published is None or page_inventory_published is None:
        return PublicationStatus.UNRESOLVED_MISSING_EVIDENCE
    if not isinstance(site_context_published, bool) or not isinstance(page_inventory_published, bool):
        return PublicationStatus.UNRESOLVED_INVALID_EVIDENCE
    if site_context_published != page_inventory_published:
        return PublicationStatus.STATUS_CONFLICT
    return (
        PublicationStatus.CONSISTENT_PUBLISHED
        if site_context_published
        else PublicationStatus.CONSISTENT_UNPUBLISHED
    )


def _canonical_inventory_path(value: str) -> str | None:
    """Normalize a site-inventory entry to a safe, site-root-relative path."""
    if not isinstance(value, str) or not value.strip():
        return None
    path = unquote(value.strip())
    normalized = posixpath.normpath(path.lstrip("/"))
    if normalized in ("", ".") or normalized == ".." or normalized.startswith("../"):
        return None
    return normalized


def normalize_root_relative_path(
    href: str,
    *,
    current_page: str = "/index.html",
) -> str | None:
    """Return a safe site-root-relative path for a local HTML href.

    Root-relative URLs such as /roadmap.html become roadmap.html.
    Relative URLs are resolved against the directory of current_page.
    Query strings and fragments are not part of the file path. External URLs,
    fragment-only links, empty paths, and paths escaping the site root return
    None.
    """
    if not isinstance(href, str) or not href.strip():
        return None

    parsed = urlsplit(href.strip())
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None

    path = unquote(parsed.path)
    if path.startswith("/"):
        candidate = path.lstrip("/")
    else:
        page = _canonical_inventory_path(current_page)
        if page is None:
            return None
        candidate = posixpath.join(posixpath.dirname(page), path)

    normalized = posixpath.normpath(candidate)
    if normalized in ("", ".") or normalized == ".." or normalized.startswith("../"):
        return None
    return normalized


def classify_static_link(
    href: str,
    site_file_inventory: set[str] | list[str] | tuple[str, ...],
    *,
    current_page: str = "/index.html",
    dynamic_route_prefixes: tuple[str, ...] = ("/post/",),
) -> LinkStatus:
    """Classify a local link without falsely marking Wix dynamic routes missing."""
    if not isinstance(href, str) or not href.strip():
        return LinkStatus.INVALID_LOCAL_PATH

    parsed = urlsplit(href.strip())
    if parsed.scheme or parsed.netloc:
        return LinkStatus.EXTERNAL
    if not parsed.path:
        return LinkStatus.ANCHOR if parsed.fragment else LinkStatus.INVALID_LOCAL_PATH

    normalized = normalize_root_relative_path(href, current_page=current_page)
    if normalized is None:
        return LinkStatus.INVALID_LOCAL_PATH

    inventory = {
        path for entry in site_file_inventory
        if (path := _canonical_inventory_path(entry)) is not None
    }
    if normalized in inventory:
        return LinkStatus.FOUND_STATIC

    for prefix in dynamic_route_prefixes:
        canonical_prefix = _canonical_inventory_path(prefix)
        if canonical_prefix and (
            normalized == canonical_prefix
            or normalized.startswith(canonical_prefix.rstrip("/") + "/")
        ):
            return LinkStatus.UNRESOLVED_DYNAMIC_ROUTE

    return LinkStatus.MISSING_STATIC


class NavigationStatus(str, Enum):
    """Evidence-aware classification of page navigation coverage."""

    NAVIGATION_PRESENT = "NAVIGATION_PRESENT"
    ISOLATED_PAGE_CANDIDATE = "ISOLATED_PAGE_CANDIDATE"
    NO_NAVIGATION_EXPECTED = "NO_NAVIGATION_EXPECTED"
    UNRESOLVED_INSUFFICIENT_CONTEXT = "UNRESOLVED_INSUFFICIENT_CONTEXT"
    UNRESOLVED_INVALID_EVIDENCE = "UNRESOLVED_INVALID_EVIDENCE"


def classify_navigation_presence(
    navigation_link_count: int | None,
    site_html_page_count: int | None,
) -> NavigationStatus:
    """Classify navigation presence without treating absence alone as a defect.

    A page with no navigation links in a multi-page site is only an isolated-page
    candidate. A one-page site may legitimately have no navigation. Missing or
    malformed counts fail closed.
    """
    if navigation_link_count is None or site_html_page_count is None:
        return NavigationStatus.UNRESOLVED_INSUFFICIENT_CONTEXT

    for value in (navigation_link_count, site_html_page_count):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            return NavigationStatus.UNRESOLVED_INVALID_EVIDENCE

    if site_html_page_count < 1:
        return NavigationStatus.UNRESOLVED_INVALID_EVIDENCE
    if navigation_link_count > 0:
        return NavigationStatus.NAVIGATION_PRESENT
    if site_html_page_count == 1:
        return NavigationStatus.NO_NAVIGATION_EXPECTED
    return NavigationStatus.ISOLATED_PAGE_CANDIDATE

def audit_page_metadata(
    html: str,
    *,
    expected_canonical: str | None = None,
) -> dict[str, str | int | None]:
    """Audit title, description and canonical metadata in a supplied HTML snapshot.

    This function performs no network requests. A canonical URL is considered
    PRESENT only when exactly one absolute HTTPS URL is found and, when an
    expected URL is supplied by the orchestrator, it matches that exact URL.
    """
    from html.parser import HTMLParser

    class MetadataParser(HTMLParser):
        def __init__(self) -> None:
            super().__init__(convert_charrefs=True)
            self.title_count = 0
            self.title_chunks: list[str] = []
            self.in_title = False
            self.descriptions: list[str] = []
            self.canonicals: list[str] = []

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            values = {key.lower(): (value or "") for key, value in attrs if key}
            tag = tag.lower()
            if tag == "title":
                self.title_count += 1
                self.in_title = True
            elif tag == "meta" and values.get("name", "").lower() == "description":
                self.descriptions.append(values.get("content", ""))
            elif tag == "link":
                relations = set(values.get("rel", "").lower().split())
                if "canonical" in relations:
                    self.canonicals.append(values.get("href", ""))

        def handle_endtag(self, tag: str) -> None:
            if tag.lower() == "title":
                self.in_title = False

        def handle_data(self, data: str) -> None:
            if self.in_title:
                self.title_chunks.append(data)

    if not isinstance(html, str):
        return {
            "title_status": "UNRESOLVED_INVALID_INPUT",
            "title": None,
            "description_status": "UNRESOLVED_INVALID_INPUT",
            "description": None,
            "canonical_status": "UNRESOLVED_INVALID_INPUT",
            "canonical_href": None,
            "canonical_count": 0,
        }

    parser = MetadataParser()
    parser.feed(html)
    parser.close()
    title = " ".join("".join(parser.title_chunks).split())

    if parser.title_count == 0:
        title_status = "MISSING"
    elif parser.title_count > 1:
        title_status = "DUPLICATE"
    elif not title:
        title_status = "EMPTY"
    else:
        title_status = "PRESENT"

    if not parser.descriptions:
        description_status = "MISSING"
    elif len(parser.descriptions) > 1:
        description_status = "DUPLICATE"
    elif not parser.descriptions[0].strip():
        description_status = "EMPTY"
    else:
        description_status = "PRESENT"

    canonical = parser.canonicals[0] if parser.canonicals else None
    if not parser.canonicals:
        canonical_status = "MISSING"
    elif len(parser.canonicals) > 1:
        canonical_status = "DUPLICATE"
    else:
        parts = urlsplit(canonical or "")
        if (
            parts.scheme.lower() != "https"
            or not parts.netloc
            or parts.username
            or parts.password
        ):
            canonical_status = "INVALID"
        elif expected_canonical is not None and canonical != expected_canonical:
            canonical_status = "MISMATCH"
        else:
            canonical_status = "PRESENT"

    description = (
        parser.descriptions[0].strip()
        if len(parser.descriptions) == 1
        else None
    )
    return {
        "title_status": title_status,
        "title": title or None,
        "description_status": description_status,
        "description": description,
        "canonical_status": canonical_status,
        "canonical_href": canonical,
        "canonical_count": len(parser.canonicals),
    }
