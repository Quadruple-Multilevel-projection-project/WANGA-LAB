# Daily Diagram Reconciliation Protocol — v1

**Status:** SPECIFIED / NOT_YET_VERIFIED

## Objective

Produce one daily, evidence-backed view of diagram changes across GitHub, Wix and approved external model submissions. The process is reconciliation, not automatic overwrite.

## Inputs

- GitHub repository head, diagram files, contracts, pull requests and commit history.
- Wix Logical AI Atlas uploads or CMS items that have been explicitly designated as diagram sources.
- Grok candidate packets conforming to `DIAGRAM_INGEST_CONTRACT_V1.json`.
- Airtable Diagram Registry, Diagram Relationships, Diagram Audit Ledger and Diagram Agent Roster.
- Notion architecture decisions and unresolved review records.

## Run sequence

1. Capture a run ID, UTC/Asia-Jerusalem timestamps, repository commit and source coverage.
2. Discover new or modified source artifacts.
3. Preserve original bytes and calculate SHA-256 for each artifact.
4. Compare source snapshots with the previous run.
5. Parse only supported formats; preserve parser errors and source locations.
6. Normalize extracted graphs without discarding source-specific syntax.
7. Compare artifact identity, node/edge changes, layer classification and contract links.
8. Run applicable audit roles from the 30-role roster.
9. Record each gate result and evidence in the append-oriented audit ledger.
10. Route contradictions, novel claims and missing evidence to Human Review or ABSTAIN.
11. Prepare a GitHub branch/PR for accepted proposed changes.
12. Publish a daily report and mark incomplete sources explicitly.

## Required daily report

- Run ID and snapshot timestamp.
- Repository commit and source coverage.
- New, changed, removed and duplicate candidate artifacts.
- Broken links, orphan nodes, possible contradictions and drift findings.
- Audit gate outcomes with source references.
- Human review queue and decisions still pending.
- Proposed GitHub PRs and their status.
- Failed or unavailable connectors.
- Explicit statement if the run is partial.

## Merge policy

- No automatic merge to the canonical branch.
- No destructive deletion during deduplication.
- No silent replacement of a diagram from Wix or Grok over a GitHub source.
- New relations remain PROPOSED until their evidence is reviewed.
- A correction is a new event/version; do not erase earlier audit history.

## Scheduling and activation

The Logical AI Atlas Wix site exposes a Scheduled time trigger and a Send HTTP request action. A secure intermediary is required for authenticated Grok calls because the inspected Wix HTTP action schema has no custom Authorization-header field. The actual daily schedule, endpoint, secret handling and end-to-end test remain pending.

## Acceptance criteria for calling this operational

- At least one complete ingestion from each enabled source has been captured.
- SHA-256 values can be reproduced from the exact stored bytes.
- Parse and comparison results are repeatable from the recorded versions.
- Audit ledger entries link to their exact source artifacts.
- Human-review routing has been exercised.
- A PR has been prepared and reviewed without auto-merging.
- A daily report records both successful and unavailable sources.

Until these criteria are met, status remains **NOT_YET_VERIFIED**.
