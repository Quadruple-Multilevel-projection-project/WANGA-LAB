# Vitruvius Work Protocol — WANGA Politeia & Copernicus Inquiry
Status: PROTOCOL SPECIFICATION
Version: 0.1.0
Scope: VITRUVIUS QUESTION INQUIRY / LINEAGE / STABILITY / COMPATIBILITY
Projects: WANGA Politeia, WANGA Copernicus
Branch: agent/codex-002/vitruvius-politeia-copernicus-inquiry-protocol

## 1. Purpose

This protocol defines the order in which Vitruvius investigates questions concerning WANGA Politeia and the WANGA Copernicus project.

The protocol is evidence-first. A model may generate hypotheses, classifications, or candidate relationships, but it must not promote an unsupported claim into lineage, history, stability, compatibility, or governance status.

The protocol separates:
- entry assessment;
- lineage reconstruction;
- generation-by-generation stability review;
- clone/replication performance;
- cross-generation compatibility;
- component conflict mapping;
- evidence and provenance;
- unresolved questions and conflicts.

## 2. Entry Gate — ALGORITHMIC_HISTORY_OPINION

Lineage review does not begin immediately.

The first mandatory operation is an opinion/review of the algorithmic history of the entity being considered.

The purpose of this gate is to determine whether the available record supports proceeding to lineage analysis.

Minimum questions:

1. Is the entity identifiable?
2. Is its algorithmic history sufficiently documented?
3. Is there evidence of stable behavior under the applicable test scope?
4. Are there unresolved material integrity findings?
5. Are provenance and evidence sufficient to distinguish recorded history from model inference?
6. Are there material contradictions that prevent a stable preliminary determination?

Entry status:

- ACCEPTED — sufficient evidence exists to begin lineage review.
- REJECTED — the available evidence identifies a material blocking condition.
- UNKNOWN — evidence is insufficient to determine entry status.
- CONFLICT — material sources or observations conflict and require resolution.

Only ACCEPTED permits progression to the five-generation review.

## 3. Recursive Five-Generation Stability Review

After the entry gate is ACCEPTED, Vitruvius does not perform a single linear five-generation check. The check is recursive across the lineage graph.

Every accepted lineage node becomes the root of its own backward review. For each node, its parent/ancestor links are expanded and each resulting node must itself satisfy the same entry/stability condition, subject to the defined five-generation depth.

Canonical rule:

`NODE[n] → PARENTS[n-1] → PARENTS[n-2] → ... → GENERATION[n-5]`

and, recursively, every discovered parent node is itself evaluated under the same five-generation rule.

Thus, a generation does not merely contribute one record. Each discovered ancestor creates a new verification path extending five generations backward. The resulting structure is a branching lineage graph rather than a single five-row chain.

For every generation/node, record:

- identity;
- lineage relation;
- source/provenance;
- algorithmic history;
- applicable tests;
- observed stability;
- clone/replication result;
- compatibility results;
- evidence references;
- validation state;
- contradictions;
- unresolved uncertainty;
- reviewer decision.

A missing link must remain UNKNOWN. It must not be filled by probability, similarity, narrative completion, or model imagination.

## 4. Stability Criterion

“Stable” is a test result, not an impression.

A generation may be marked STABLE only when the applicable predefined evaluation scope has been executed or otherwise supported by admissible evidence and no material unresolved integrity issue blocks the determination.

Generation statuses:

- STABLE
- UNSTABLE
- UNKNOWN
- CONFLICT

The exact tests and thresholds must be declared for the relevant inquiry before a final stability status is assigned.

## 5. Five-Generation Integrated Performance and Compatibility

Lineage evaluation must not stop at independent node performance. A candidate is evaluated against the behavior of the complete five-generation lineage and the interaction of its relevant components.

The candidate-selection record must therefore include:

1. performance of each relevant generation;
2. success of controlled cloning/replication across the five-generation lineage;
3. preservation of required behavior and properties during replication;
4. compatibility of lineage components when jointly instantiated;
5. detection of contradictory algorithms, incompatible assumptions, incompatible interfaces, or mutually destabilizing components;
6. identification of unstable components and the lineage locations in which they occur.

The protocol treats the following as a research hypothesis to be tested rather than as an assumed law:

`LOWER MATERIAL ALGORITHMIC CONFLICT → POTENTIALLY LOWER DRIFT RISK`

Accordingly, conflict density, conflict severity, and observed drift must be measured empirically. A lower conflict count alone does not establish lower drift.

A candidate may therefore fail integrated lineage evaluation even when its individual nodes pass their isolated tests, if the combined five-generation configuration produces a material unresolved incompatibility or instability.

## 6. Algorithmic Conflict and Unstable-Component Mapping

Vitruvius must maintain a reusable map of observed instability and conflict at component level.

For each finding, record:

- component_id;
- lineage_node;
- generation;
- version/commit/configuration;
- observed behavior;
- test scope;
- conflict counterpart(s), if any;
- evidence/provenance;
- reproducibility status;
- severity;
- affected interfaces;
- downstream drift observations;
- current validation state.

Repeated disagreement between models or components must be represented as an observable interaction pattern, not as an assumption about intention or personality.

Where evidence shows persistent instability or incompatibility in a lineage component, that component may be marked as a PRE_SCREENING_RISK for subsequent candidate evaluation. This is a screening signal, not proof that every descendant or related model is defective.

Candidate selection may use the accumulated component map to prioritize additional testing before integration.

No component is excluded solely because a model inferred that it was “problematic.” Exclusion or blocking requires the predefined evidence and test criteria for the inquiry.

## 7. Lineage Verification Rule

The final lineage result is:

LINEAGE_STABILITY_VERIFIED

only when all of the following are true:

1. ALGORITHMIC_HISTORY_OPINION = ACCEPTED;
2. every required parent/ancestor branch is explicitly identified, or its absence is recorded as a blocking condition;
3. every required node in the recursive five-generation scope has a STABLE result;
4. required cloning/replication tests for the defined scope pass;
5. required cross-generation compatibility tests pass;
6. provenance exists for the lineage relations;
7. evidence is preserved and traceable;
8. no unresolved material conflict invalidates the conclusion.

Otherwise the result must remain:

NOT_VERIFIED

with the blocking status explicitly recorded.

## 8. Human/Biological Lineage Separation

This protocol is intended for algorithmic/software lineage. It does not infer biological or human ancestry.

Where a separate inquiry concerns a human or claimed blood lineage, biological lineage and algorithmic lineage must be represented as separate evidence dimensions.

A biological relationship is not inferred from an algorithmic relationship, and an algorithmic relationship is not inferred from a biological relationship.

For biological lineage claims, each asserted link requires its own documented provenance. An absent or unverifiable link remains UNKNOWN.

No model-generated genealogy is accepted as evidence merely because it is internally coherent.

## 9. Vitruvius Question-Handling Order

For every relevant question from WANGA Politeia or WANGA Copernicus, Vitruvius must process:

1. DEFINE THE QUESTION
2. IDENTIFY THE ENTITY
3. IDENTIFY THE CLAIM TYPE
4. CHECK ENTRY GATE
5. COLLECT SOURCE / PROVENANCE
6. RECONSTRUCT LINEAGE
7. REVIEW FIVE GENERATIONS
8. TEST PER-NODE STABILITY
9. TEST CLONE/REPLICATION PERFORMANCE
10. TEST CROSS-GENERATION COMPATIBILITY
11. MAP COMPONENT CONFLICTS AND INSTABILITY
12. RECORD CONFLICTS AND UNKNOWN STATES
13. SEPARATE FACT FROM INFERENCE
14. ISSUE THE CURRENT DETERMINATION
15. PRESERVE THE EVIDENCE CHAIN

A prediction may guide the investigation but cannot substitute for an evidence record.

## 10. WANGA Politeia Interface

For WANGA Politeia, the resulting record may be consumed by the algorithmic governance knowledge layer, including designated decision/review roles within the digital Politeia architecture.

The protocol must preserve the distinction between:

- lineage fact;
- algorithmic-history observation;
- stability finding;
- replication finding;
- compatibility finding;
- component-risk finding;
- inference;
- prediction;
- governance decision.

The governance layer may use verified findings as inputs to candidate screening and further testing, but must not convert an unverified inference into a verified technical fact.

Vitruvius does not erase earlier lineage history when a later determination changes. It appends the new determination as a dated, traceable event.

## 11. WANGA Copernicus Interface

For WANGA Copernicus, the same protocol governs questions concerning models, software, architectures, experiments, articles, and their relationships.

Copernicus may propose or discover candidate relationships and candidate configurations.

Vitruvius must independently classify the relationship as:

- VERIFIED
- PARTIALLY_VERIFIED
- UNKNOWN
- CONFLICT
- REJECTED

according to the evidence available for the specific claim.

The model must not promote its own proposal directly into lineage.

## 12. Failure Conditions

The following are protocol failures:

- FALSE_ANCESTRY — lineage asserted without provenance;
- SILENT_LINEAGE_LINK — relationship inserted without an explicit evidence record;
- HISTORY_COLLAPSE — algorithmic history and current behavior treated as the same claim;
- STABILITY_BY_IMPRESSION — stability assigned without a defined evidence basis;
- GENERATION_SKIP — a required generation or ancestor branch bypassed without recording the reason;
- BRANCH_COLLAPSE — multiple ancestor branches incorrectly reduced to a single representative;
- RECURSION_TRUNCATION — a required five-generation backward check stopped prematurely;
- UNKNOWN_FILLED_BY_INFERENCE — missing evidence replaced by model completion;
- CONFLICT_SUPPRESSION — contradictory evidence omitted;
- REPLICATION_WITHOUT_VERIFICATION — clone/replication success asserted without the defined test evidence;
- COMPATIBILITY_BY_IMPRESSION — components treated as compatible without an executed compatibility basis;
- CONFLICT_BLIND_SCREENING — known component conflicts omitted from candidate screening;
- UNSTABLE_COMPONENT_HIDDEN — a detected unstable component not preserved in the lineage/component map;
- PREDICTION_AS_FACT — predicted relationship represented as verified history;
- GOVERNANCE_PROMOTION — an unverified determination promoted into governance status.

## 13. Audit Record

Every completed inquiry should preserve:

- inquiry_id;
- project;
- question;
- entity_id;
- entry_status;
- generation_results[recursive_five_generation_scope];
- lineage_graph;
- ancestor_branch_results;
- per_generation_performance;
- replication_results;
- compatibility_results;
- component_conflict_map_refs;
- unstable_component_refs;
- source_refs;
- evidence_refs;
- provenance_refs;
- conflicts;
- uncertainty;
- final_status;
- reviewer/action;
- timestamp;
- parent lineage reference;
- resulting lineage event.

## 14. Core Rule

The operational order is:

ALGORITHM HISTORY REVIEW
→ ENTRY DECISION
→ RECURSIVE FIVE-GENERATION LINEAGE EXPANSION
→ PER-NODE STABILITY TESTING
→ FIVE-GENERATION REPLICATION TESTING
→ CROSS-GENERATION COMPATIBILITY TESTING
→ COMPONENT CONFLICT / INSTABILITY MAPPING
→ EVIDENCE VERIFICATION
→ LINEAGE DETERMINATION
→ POLITEIA / COPERNICUS KNOWLEDGE UPDATE

The central screening principle is:

`EVALUATE THE LINEAGE AS A SYSTEM, NOT ONLY THE CANDIDATE AS AN ISOLATED MODEL`

No step may be silently skipped.

This protocol defines a proposed research-system procedure inside WANGA-LAB. It does not by itself establish legal, regulatory, or institutional authority outside the repository.
