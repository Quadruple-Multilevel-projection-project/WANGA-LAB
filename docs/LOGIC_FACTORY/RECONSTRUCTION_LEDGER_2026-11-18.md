# Logic Factory Reconstruction Ledger
Date: 2026-11-18
Status: BASELINE RECOVERED / RECONSTRUCTION IN PROGRESS
Canonical repository: Quadruple-Multilevel-projection-project/WANGA-LAB

## 1. Recovered baseline (repository-verified)
- The 175-term index exists at `milaot-hahigayon/INDEX.md`; term records are numbered 001–175 and grouped across gates א–יד.
- `milaot-hahigayon/ORCHESTRATOR.md` routes term retrieval and references the master map contract and machine-readable registry.
- `milaot-hahigayon/sentences/INDEX.md` records gates ט׳–י״ד as EXTRACTED and gates א׳–ח׳ as incomplete.
- `docs/LOGIC_FACTORY/MASTER_MAP_INTEGRATION_CONTRACT.md` and `docs/LOGIC_FACTORY/map_registry.v1.json` already define map families, edge evidence, three pipeline configurations, agent roles, and the Logical Map Clock.
- The three supplied repositories are accessible with push/admin permissions in this GitHub connection: `AmbassadorOv/WANGA-LAB.-01`, `Quadruple-Multilevel-projection-project/Qualia`, and `Quadruple-Multilevel-projection-project/WANGA-LAB`.

## 2. Artifact inventory — do not collapse families
The planned reconstruction contains distinct families:
1. 13 legacy diagrams — preserve their original identity and content.
2. 14 chapter maps — chapters 1–13 individually, plus one synthesis map for chapter 14.
3. 4 meta-maps — Place, Division-vs-Boundary, Terms/Logic, and Limits/Gaps.
4. 175 term maps — one map per indexed term.
5. 1 integrated network/master map — Propagated Logic, XL Links, dependency closure, and Logical Map Clock.

Planned total: 207 map artifacts when the master network map is counted; the 13 legacy diagrams and 14 chapter maps are separate families. This is an inventory target, not a claim that these artifacts have been generated.

## 3. Map data model
Every node must preserve:
- stable node_id and node_type;
- exact source_ref and source_location;
- original gate_id / term_id / chapter_id without inferred equivalence;
- original wording and role in context;
- epistemic status;
- version and change_event_id.

Every edge must preserve:
- stable edge_id;
- source node, typed relation, target node;
- exact evidence reference and location;
- relation status (PROPOSED, SOURCE-BACKED, VERIFIED, REJECTED);
- scope and dependency policy;
- provenance and change event.

Allowed relation types include SOURCE_SUPPORTS_CLAIM, FORMAL_DERIVATION, DATA_DEPENDENCY, IMPLEMENTATION_CALL, VALIDATION_CHECK, EDITORIAL_LINK, and HYPOTHESIS_LINK. An edge is never promoted because two labels look similar or two nodes share a diagram.

## 4. Rebuild order
A. Freeze and inventory the 13 legacy diagrams and four meta-map source workbooks.
B. Recover exact source text for chapters 1–13 and verify chapter 14's synthesis scope; keep chapter IDs distinct from gate IDs.
C. Generate 14 chapter maps with source-linked nodes and typed edges.
D. Generate 175 term maps from records 001–175; each map links back to its exact term record and gate.
E. Add the four meta-maps as separate map families and connect them only through evidenced edges.
F. Reconcile all families into the master network map.
G. Configure SERIAL_RETURN, PARALLEL_14_GATE, and COMPARISON against the same immutable source snapshot.
H. Run reference integrity, dangling-edge, duplicate-ID, source-coverage, contradiction, and deterministic replay checks.
I. Compute reverse dependency closure on every source or map mutation; mark affected maps CURRENT, STALE, or BLOCKED.
J. Publish only after validation; retain rejected and unresolved candidates.

## 5. Current blockers — explicit, not inferred
- Source extraction for gates א׳–ח׳ is incomplete in the repository index.
- Chapter-to-gate equivalence is unresolved and must not be inferred from numbering.
- The current bytes and worksheet schemas for the four named Excel workbooks have not been verified in this repository inspection.
- Exact deployed URLs and repository paths for every external map application are not yet inventoried.
- The three pipeline configurations are specified, not demonstrated as deployed runtime executions.
- Gmail search found WANGA/GitHub activity and a Logic Sandbox Reminder, but did not establish a recoverable list of Gmail/Google Groups or their membership/configuration. Gmail label enumeration returned an API 400 error; no labels or groups were modified.
- Repeated GitHub Actions notifications report failures for the Logic Fractal Wiki Research, Vitruvius Research Index, and AI231 Agent Runtime Catalog workflows. Their logs must be inspected before claiming CI is healthy.

## 6. Gmail and external workspace boundary
Do not create, rename, delete, or change membership of a Google Group based only on email subjects or mailing-list notifications. First recover the authoritative group address, owners, members, purpose, and linked repository/app from an actual Groups directory or explicit configuration record. Gmail labels are not Google Groups.

For Notion, Figma, Airtable, Canva, Wix, and other map applications, register only exact connected workspace IDs, page/file/base IDs, and verified URLs. A mention or an email reference is not proof of a live integration.

## 7. Completion criteria
A map family is COMPLETE only when:
- its source inventory is present and versioned;
- every source-backed node has exact source location;
- every edge has a type, evidence, and status;
- unresolved relations remain visibly unresolved;
- map render and machine-readable data agree;
- dependency invalidation and return-to-origin are tested;
- a reproducible validation receipt is committed.

No diagram render, generated file, successful CI run, or attractive visualization alone establishes semantic correctness.

## 8. Action boundary
This ledger records the recovered state and execution order. It does not claim that 207 maps, Gmail groups, plugins, apps, agents, or runtime pipelines have been built or connected.
