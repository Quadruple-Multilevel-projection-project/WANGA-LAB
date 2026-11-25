# AI231 Robotics Collaboration — Metadata Remediation Draft

Date: 2026-11-24  
Status: DRAFT_ONLY / PRODUCTION_BLOCKED  
Site: AI231 Robotics Collaboration  
Site ID: `d8dcc187-d8fe-4e3c-b7a4-9e46f020349e`  
Live URL: https://headless-nkogaqagpcv-beywolf5-1408.wix-site-host.com/

## Scope and permission

Read-only inspection used Wix headless `files.list/read`. No Wix file was changed, uploaded, published, or deleted. This artifact is a repository draft only. Production work requires explicit approval for this exact site, the exact files below, and the publication scope.

## Verified before-state

The authorized headless inventory returned exactly three files and `hasMore=false`:

| File | Bytes | Title | Description | Viewport | Canonical |
|---|---:|---|---|---|---|
| `index.html` | 14,709 | AI231 Robotics Collaboration — Partner Network | Present | Present | Missing |
| `about.html` | 22,857 | Who We Are \| AI231 — Logic-First Initiative | Present | Present | Missing |
| `agents.html` | 10,775 | AI231 Agent Foundry \| Digital Agent Network | Present | Present | Missing |

Additional verified observations:
- `sitemap.xml` is absent from the inventory.
- `robots.txt` is absent from the inventory.
- All three pages have a viewport declaration.
- All three pages have a meta description.
- The internal navigation references among `index.html`, `about.html`, and `agents.html` resolve to files in the same inventory.
- The About page contains English and Hebrew sections; the Hebrew section includes `lang="he"` and RTL direction markup.
- No image elements were found in the three inspected pages; image-alt testing is therefore not applicable to this snapshot.
- External destination availability, visual mobile rendering, Core Web Vitals, search ranking and conversion behavior were not tested.

## Proposed after-state — draft only

1. Add one absolute canonical link inside each page's `<head>`:
   - `index.html`: `https://headless-nkogaqagpcv-beywolf5-1408.wix-site-host.com/`
   - `about.html`: `https://headless-nkogaqagpcv-beywolf5-1408.wix-site-host.com/about.html`
   - `agents.html`: `https://headless-nkogaqagpcv-beywolf5-1408.wix-site-host.com/agents.html`
2. Add a root `sitemap.xml` containing exactly those three public canonical URLs. Omit `lastmod` until a reliable page modification timestamp is available.
3. Add a root `robots.txt` with:
   ```text
   User-agent: *
   Allow: /
   Sitemap: https://headless-nkogaqagpcv-beywolf5-1408.wix-site-host.com/sitemap.xml
   ```
4. Preserve all existing titles, descriptions, page content, language attributes, styles and scripts. Do not introduce structured-data claims or change partnership/product claims in this metadata-only patch.

## Acceptance tests required before any release

- Read back all three complete HTML files and confirm one correct canonical URL per page.
- Fetch `/sitemap.xml` and confirm HTTP 200 and exactly three canonical URLs.
- Fetch `/robots.txt` and confirm HTTP 200 and the sitemap declaration.
- Confirm the three internal navigation targets still resolve.
- Run a mobile viewport/browser check and an accessibility scan; a viewport meta tag alone is not proof of responsive behavior.
- Verify external destinations separately before labeling them healthy.
- Compare the after-state against this before-state and record exact file sizes, hashes, tool result and preview URL.

## Rollback and status

No production mutation occurred, so there is no live rollback to perform. Discard this draft or revert its dedicated repository commit to roll it back. If a later, separately approved release occurs, restore the three original HTML snapshots and remove the added `sitemap.xml` and `robots.txt` to reverse the proposed change.

**Acceptance:** PASS for the evidence-backed draft artifact only; UNRESOLVED for preview rendering, live route checks and production publication.  
**Next action:** obtain explicit approval for this exact site and metadata-only scope before creating a Wix preview or publishing anything.
