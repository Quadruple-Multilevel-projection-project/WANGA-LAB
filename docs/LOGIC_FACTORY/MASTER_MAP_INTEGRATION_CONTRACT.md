# AI231 / WANGA — Master Map Integration Contract
Version: 0.1.0
Status: INTEGRATION SPECIFICATION / PARTIALLY SOURCE-BOUND
Updated: 2026-11-18

## Purpose
Connect the existing map applications, map workbooks, diagram families, term registry, 14-gate index, and logical-factory orchestration through one stable routing contract. This document is an integration layer; it does not replace source books, source spreadsheets, or existing repositories.

## Source of truth and boundaries
- 175 numbered term records: `milaot-hahigayon/terms/001.md` … `175.md`.
- Gate-to-term ranges are authoritative only as indexed in `milaot-hahigayon/INDEX.md`.
- Retrieval and evidence rules: `milaot-hahigayon/ORCHESTRATOR.md`.
- Sentence extraction status: `milaot-hahigayon/sentences/INDEX.md`.
- Existing architecture link registry: `docs/ARCHITECTURE/VITRUVIUS_ORCHESTRATOR_LINK_MAP.md`.
- The actual books and spreadsheet files remain their own source artifacts. A filename or prior description does not establish that a file is currently present or verified.

## Fourteen-gate routing index
| Gate | Term records | Map route |
|---|---:|---|
| א | 001–004 | gate/א |
| ב | 005–018 | gate/ב |
| ג | 019–023 | gate/ג |
| ד | 024–036 | gate/ד |
| ה | 037–040 | gate/ה |
| ו | 041–051 | gate/ו |
| ז | 052–063 | gate/ז |
| ח | 064–079 | gate/ח |
| ט | 080–089 | gate/ט |
| י | 090–107 | gate/י |
| יא | 108–123 | gate/יא |
| יב | 124–132 | gate/יב |
| יג | 133–149 | gate/יג |
| יד | 150–175 | gate/יד |

These are registry routes, not substitute chapter interpretations. The sentence extraction index currently marks gates ט׳–י״ד EXTRACTED and gates א׳–ח׳ as a combined sentence/argument system whose extraction remains incomplete. Do not mark the first eight gates SOURCE-CHECKED until their source extraction is added.

## Map families and integration roles
1. Chapter maps: 13 individual maps for chapters 1–13, plus a dedicated chapter-14 synthesis map. Chapter-to-gate equivalence must be explicitly sourced; do not infer it from numbering.
2. Existing 13-diagram sequence: preserve as a distinct diagram family. Map each diagram to a chapter/gate only after source-backed relation checking.
3. Meta-maps: Place_Photograph_Complete-1.xlsx; Division_Reason_Photograph.xlsx; Terms_Logic_Photograph.xlsx; Logic_Photograph_Gaps.xlsx. Treat these as named artifact references pending confirmation of current file bytes and exact worksheet/sheet structure.
4. Term maps: one map per term record (175 total), with links to source, gate, chapter (when proven), related terms, relation evidence, and map dependencies.
5. Network map: Propagated Logic and XL Links, plus the Logical Map Clock change/dependency view.
6. Application registry: each map app must register app_id, repository/path or verified URL, map_family, source_artifacts, gate_ids, term_ids, inbound_links, outbound_links, version, status, and last_verified_commit. Unknown destinations remain UNRESOLVED; never fabricate URLs.

## Canonical map node and edge contract
Every node:
- node_id (stable; e.g. TERM-001, GATE-A, CHAPTER-01, MAP-PLACE)
- node_type (SOURCE | GATE | TERM | CHAPTER | MAP | APP | PIPELINE | AGENT | VALIDATION)
- source_ref and source_location
- gate_id and term_id when applicable
- epistemic_status (INDEXED | SOURCE-CHECKED | RELATION-CHECKED | VERIFIED | HYPOTHESIS | UNRESOLVED)
- version and change_event_id

Every edge:
- edge_id (stable)
- from_node, relation_type, to_node
- evidence_ref and evidence_location
- relation_status (PROPOSED | SOURCE-BACKED | VERIFIED | REJECTED)
- direction and dependency_policy
- created_by and change_event_id

No relation is upgraded to VERIFIED merely because two nodes share a label or appear in the same diagram.

## Three pipeline configurations
A. SERIAL / RETURN:
source snapshot → gate routing → term retrieval → relation checks → validation → return/readout. Each step consumes the previous immutable result.

B. PARALLEL 14-GATE:
dispatch independent gate workers against the same immutable source snapshot; each worker returns gate-scoped terms, relations, evidence and unresolved items; aggregator reconciles collisions without overwriting source records.

C. COMPARISON:
compare serial and parallel outputs against the same snapshot; identify omissions, contradictions, drift and unsupported edges; emit a comparison report. Comparison does not silently select a winner.

All three configurations share the same registries, source snapshot, gate identifiers, term identifiers, and validation vocabulary. Their results remain separately versioned.

## Orchestration routing
- OR-01: top-level Star Orchestrator; routes requests, does not author source facts.
- SRC-01: source locator and exact-text checker.
- TERM-175: term-record retrieval and identity preservation.
- GATE-01 … GATE-14: gate-scoped routing and analysis.
- SER-01: serial/return executor.
- PAR-01 … PAR-14: parallel gate workers.
- CMP-01: comparison and reconciliation.
- DRIFT-01: detects changed source, changed edges, and semantic drift.
- VAL-01: verifies evidence, status transitions and boundary conditions.
- DELTA-01: computes affected-map closure after a change.

These are role identifiers/specifications; they are not claims that autonomous agents have already been deployed.

## Logical Map Clock
The Logical Map Clock is a map-change sequence, not a wall-clock substitute and not a new semantic authority.
A map mutation emits a change event containing:
- change_event_id
- logical_map_sequence
- timestamp
- changed_node_ids / changed_edge_ids
- source_commit_or_artifact_version
- affected_map_ids
- pipeline_config
- validation_result

Update procedure:
1. Capture immutable before/after snapshots.
2. Identify changed nodes and edges.
3. Traverse reverse dependencies to calculate affected maps and apps.
4. Rebuild only affected map views; do not rewrite source records.
5. Run serial, parallel, and comparison checks as configured.
6. Mark downstream maps CURRENT only after validation; otherwise STALE or BLOCKED.
7. Preserve a traceable change event and return path to the originating source.

## Validation and stop rules
- INDEXED is not SOURCE-CHECKED.
- SOURCE-CHECKED is not RELATION-CHECKED.
- RELATION-CHECKED is not automatically VERIFIED.
- Missing source, ambiguous relation, or unsupported mapping => UNRESOLVED / ABSTAIN.
- Contradiction with a verified source => REJECTED / HALT for the affected path.
- No new source terms, invented weights, invented links, or fabricated app URLs.
- Gate 10 genus/species and boundary checks are applied only where the source relation requires them; do not generalize Gate 10 to every gate.
- A successful diagram render is not proof that its semantic edges are correct.

## Current integration state
- VERIFIED: repository exists and current user has push/admin permissions; 175-record index and gate ranges are present; term orchestrator and sentence extraction index are present.
- VERIFIED: sentence extraction index reports gates ט׳–י״ד EXTRACTED.
- UNRESOLVED: source-backed extraction for gates א׳–ח׳; exact chapter-to-gate correspondence; current bytes and worksheet schemas of the four named Excel artifacts; exact deployed URLs and repository paths for every map application; runtime wiring and execution of the three configurations.
- NOT CLAIMED: 189 diagrams created; apps connected; pipeline deployed; agents running; contract tagged or pushed.

## Existing registry links
- [175-term index](../milaot-hahigayon/INDEX.md)
- [Term orchestrator](../milaot-hahigayon/ORCHESTRATOR.md)
- [Sentence extraction index](../milaot-hahigayon/sentences/INDEX.md)
- [Vitruvius orchestrator link map](../docs/ARCHITECTURE/VITRUVIUS_ORCHESTRATOR_LINK_MAP.md)

## Action signature
Timestamp=2026-11-18T00:11:00+02:00
Contract_Start_Time=2026-11-17T20:29:00+02:00
Action_ID=AI231-MAP-INTEGRATION-001
SHA256=9a749131aebf3d047f3c4102d7e8ffd499791b4fdfdceea2ee2450989c233bda
