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

    path = unquote(parsed.path.replace("\\\\", "/"))
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
