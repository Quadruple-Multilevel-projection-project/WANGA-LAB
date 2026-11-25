# Diagram Intelligence Hub — v1

**Status:** SPECIFIED / NOT_YET_VERIFIED  
**Repository:** WANGA-LAB  
**Purpose:** Maintain a source-grounded, cross-platform system that inventories diagrams, extracts their structures, compares versions, audits relationships and prepares a daily reconciliation report.

## System boundary

- **GitHub / WANGA-LAB:** canonical source for source files, contracts, version history and accepted changes.
- **Wix / Logical AI Atlas:** intake and presentation surface for diagrams and review outcomes.
- **Grok:** external candidate extractor/reviewer. Grok output is untrusted candidate data until independently audited.
- **Airtable:** operational registries for diagrams, relationships, agent roles and audit events.
- **Notion:** durable architecture notes, decisions and handoff documentation.

A link between platforms is a specified interface until an end-to-end test proves it is live.

## Pipeline

1. Ingest an artifact without modifying the source.
2. Capture source URL, source identifier, version/commit and exact-byte SHA-256.
3. Parse the artifact into a typed intermediate representation.
4. Preserve source syntax and extracted interpretation separately.
5. Compare nodes, edges, labels, contracts, versions and provenance.
6. Run independent audit roles and record evidence.
7. Route unresolved contradictions, novelty or impact to human review.
8. Publish accepted changes through a GitHub pull request.
9. Generate a daily snapshot and unresolved-findings report.

## Four architecture layers

1. Language & Contract
2. Analytics & Visualization
3. KRAKEN
4. Orchestration & Product

Keep the following systems distinct: 14 logic gates / 175 logic terms; 231 Hebrew letter-pair gates; five phonetic articulation groups. A cross-layer mapping requires an explicit, versioned contract.

## Core invariants

- No automatic LOCK from model confidence or a manually supplied score.
- No fabricated weights, coordinates, topology rules, λp or κ formulas.
- Every extracted claim and relation must carry a source and evidence location.
- Preserve original artifacts; corrections create new versions/events.
- Contradictions are recorded, not silently reconciled.
- Diagrams do not prove deployed runtime behavior.
- No secrets in GitHub, Airtable, Notion or diagram payloads.
- Human approval is required before canonical changes are merged.

## Files

- [Grok collaboration handoff](GROK_COLLABORATION_HANDOFF_V1.md)
- [Diagram ingest contract](DIAGRAM_INGEST_CONTRACT_V1.json)
- [Daily reconciliation protocol](DAILY_RECONCILIATION_PROTOCOL_V1.md)
- [30-role agent roster](DIAGRAM_AGENT_ROSTER_V1.json)
- [Master architecture map](DIAGRAM_INTELLIGENCE_HUB_MASTER_V1.mmd)

## Current implementation state

- Existing: repository diagram index, master link map, diagram catalog, model handoff protocol and machine-readable registry.
- Existing: Airtable Diagram Registry, Diagram Relationships, Diagram Audit Ledger and Diagram Agent Roster tables.
- Existing: Wix site with scheduled trigger, webhook trigger and outbound HTTP action available in its installed automation catalog.
- Not yet verified: Grok API connection, secure proxy, active Wix automation, active daily schedule, 30 agent runtimes and automated GitHub PR creation.

## Decision labels

- `EXISTING`: artifact or component exists.
- `SPECIFIED`: design or contract exists; runtime may not.
- `PROPOSED`: candidate awaiting approval.
- `NOT_YET_VERIFIED`: insufficient test evidence.
- `VERIFIED`: reproducible test evidence, version and acceptance result are linked.
- `SIMULATED`: simulated/emulated only.
- `ABSTAIN` / `SANDBOX`: missing evidence or unresolved safety/consistency condition.
