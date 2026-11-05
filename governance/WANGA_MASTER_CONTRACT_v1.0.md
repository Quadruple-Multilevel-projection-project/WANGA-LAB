# WANGA MASTER CONTRACT v1.0
**Status:** BINDING_IMMUTABLE  
**System:** WANGA-LAB / PCE (Particle Calculus Engine)  
**Purpose:** Master governance contract for source-grounded research, logical extraction, verification, configuration, and GitHub project coordination.

> **Evidence boundary:** This contract records the supplied project rules and reported state. It does not itself verify the underlying halakhic citations, prove a source lineage, or validate implementation claims. Do not promote an item to verified without the evidence required below.

## 1. Governing priority chain

`SOURCE → LINEAGE → EXTRACTION → RELATIONS → LOGIC → VERIFICATION → CONFIGURATION → WEIGHTS`

No stage may be skipped. Any deviation must be recorded as `DRIFT`, with the originating artifact, affected stage, reason, evidence, and resolution status.

The project uses **dynamic logic**, not a closed, immutable formal-logic model. Reality and source evidence outrank model confidence, consensus, or stylistic plausibility. Preserve the user's terminology and distinctions.

## 2. Contract precedence and scope

This master contract coordinates:
1. `LOGIC_BEFORE_WEIGHT_CONTRACT`
2. `PCE / Authority Revocation`
3. Halakhic source verification
4. Source and decisor database
5. Verification status model
6. `SOURCE_LINEAGE`
7. `UNRESOLVED` tracking
8. Quantum Bridge
9. WANGA-OS
10. Anti-Drift controllers

If component contracts conflict, do not silently reconcile them. Record the conflict as `UNRESOLVED`, identify both source locations, and block dependent transitions until the authorized resolution is documented.

## 3. Source and extraction state vocabulary

Use only these state labels where applicable:

- `EXTRACTED` — directly extracted from an identified source.
- `DERIVED` — inferred by a declared derivation from identified inputs.
- `UNRESOLVED` — required relationship or claim remains undecided.
- `REPRESENTATION_ONLY` — structural representation, not a claim of reality or proof.
- `NOT_YET_VERIFIED` — captured but not checked against the required evidence.
- `PARTIAL` — only part of the required material is available or checked.
- `FAILED_EXTRACTION` — extraction did not succeed; retain failure evidence.
- `REVIEW_ONLY` — available for inspection, not approved for execution.
- `DUPLICATE` — likely duplicate; retain links to all records and do not silently discard.

Do not use `DERIVED` as if it meant directly attested. Preserve exact quotations separately from normalized text and interpretation.

## 4. Verification status vocabulary

Permitted `verification_status` values:

`VERIFIED_PRIMARY`, `VERIFIED_SCAN`, `VERIFIED_DIGITAL`, `VERIFIED_MULTIPLE`, `PARTIAL_VERIFICATION`, `SOURCE_FOUND`, `RESEARCH_ONLY`, `SECONDARY_SOURCE_ONLY`, `UNVERIFIED`, `DISPUTED`, `MISATTRIBUTED`, `SOURCE_MISSING`, `QUOTE_MISMATCH`, `BLOCKED`.

A search result or a citation copied from another secondary work is not, by itself, primary verification. Record the precise edition/manuscript/scan, location, and comparison performed. Never promote a record solely because multiple websites repeat the same text.

## 5. Verification method vocabulary

Permitted `verification_method` values:

`PRIMARY_TEXT`, `PRINTED_EDITION`, `SCANNED_EDITION`, `SEFARIA_CHECK`, `HEBREWBOOKS_CHECK`, `WIKISOURCE_CHECK`, `LIBRARY_CATALOG`, `SCHOLARLY_REFERENCE`, `MANUAL_COMPARISON`, `CROSS_REFERENCE`, `RESEARCH_DOCUMENT`, `NOT_VERIFIED`.

Record all methods actually used; do not claim a check that was not performed. A catalog record proves the existence/description of an item, not the accuracy of a quotation from it.

## 6. Verification confidence

Allowed values: `HIGH`, `MEDIUM`, `LOW`, `UNKNOWN`.

Confidence is a summary of evidence quality, not a substitute for evidence. Do not invent numeric weights or convert confidence labels into numeric values unless a separately approved contract explicitly permits it.

## 7. Mandatory source record fields

Every source record must preserve:

- `record_id`
- `source_name`
- `source_type`
- `source_location`
- `quote`
- `ruling`
- `state_label`
- `verification_status`
- `verification_method`
- `verification_confidence`
- `verification_date`
- `verification_notes`
- `source_url`
- `lineage_id`

Recommended audit fields: `edition_or_manuscript`, `folio_page_section`, `transcription`, `transcription_source`, `reviewer`, `reviewed_at`, `related_record_ids`, `drift_id`, `unresolved_ids`, `evidence_hash`. Leave fields blank or mark them unknown when evidence is absent; never fill them by guesswork.

## 8. PCE rules

- `RULE_01 LATTICE IMMUTABLE` — preserve the defined structure; changes require an explicit, versioned amendment.
- `RULE_02 DRIFT IS DATA` — do not erase deviations; capture and trace them.
- `RULE_03 NO INTERPRETATION` — no unlabelled interpretation presented as extraction. Any permitted derivation must be explicit and traceable.
- `RULE_04 EXECUTED OR BLOCKED` — every requested operation ends in an evidenced execution result or a recorded block.
- `RULE_05 UNKNOWN INPUT = BLOCK` — missing required inputs block dependent execution.
- `RULE_06 EVERYTHING LOGGED` — preserve inputs, source references, outputs, errors, and changes.
- `RULE_07 CONSENSUS ≠ TRUTH` — consensus/model confidence is not proof.
- `RULE_08 LINEAGE REQUIRES EVIDENCE` — a transmission relationship requires source evidence; do not invent teacher–student chains.
- `RULE_09 IM_HAKOLEL` — reserved operator; semantics remain unresolved until defined from an authorized source.
- `RULE_10 AUTHORITY OVERRIDE` — reserved rule; its scope and authorized authority must be evidenced and specified before executable use.
- `RULE_11 AUTO REVOCATION` — reserved rule; revocation conditions, authority, scope, and audit semantics must be specified before execution.
- `RULE_12 EXECUTOR IS TOOL` — an executor performs authorized operations; it is not itself an authority for the truth of a claim.

Rules with unresolved semantics remain non-executable. Do not infer missing semantics from names alone.

## 9. Initial halakhic source registry

These are registry entries to track, not assertions that every quotation or attribution is already verified.

| ID | Source reference | Required caution |
|---|---|---|
| `SRC_HAL_001` | Bavli, Sanhedrin 7b | Verify exact passage and context |
| `SRC_HAL_002` | Rambam, Sanhedrin 4:14 | Compare exact edition/text |
| `SRC_HAL_003` | Rambam, Sanhedrin 4:15 | Compare exact edition/text |
| `SRC_HAL_004` | Kesef Mishneh | Record exact Rambam passage and edition |
| `SRC_HAL_005` | Radbaz | Resolve siman/reference variant before confirmation |
| `SRC_HAL_006` | Tur | Record section and exact wording |
| `SRC_HAL_007` | Rosh | Record tractate/siman and exact wording |
| `SRC_HAL_008` | Rivash | Record responsum number and edition |
| `SRC_HAL_009` | Maharik | Record responsum number and edition |
| `SRC_HAL_010` | Meiri | Record work, passage, and edition |
| `SRC_HAL_011` | Sefer HaChinukh | Resolve mitzvah-number/reference variant before confirmation |
| `SRC_HAL_012` | Sefer Chassidim | Record paragraph/edition |
| `SRC_HAL_013` | Maharshdam | Record responsum number and edition |
| `SRC_HAL_014` | Chatam Sofer | Record responsum/section and edition |
| `SRC_HAL_015` | Arukh HaShulchan | Record exact siman/se'if |
| `SRC_HAL_016` | Yosef Yedid Halevi | Record work, section, and edition |
| `SRC_HAL_017` | Chazon Ish | Record work, siman, and section |

No quotation, ruling, or attribution is established merely by inclusion in this list. Preserve variant references and mismatches as evidence.

## 10. Source lineage

Each lineage edge must record:
- `lineage_id`
- `from_record_id`
- `to_record_id`
- `relationship_type`
- `evidence_quote`
- `evidence_location`
- `source_url` or archival identifier
- `verification_status`
- `verification_notes`

Use separate labels for directly attested transmission, scholarly attribution, inferred relationship, and unresolved relationship. A plausible chronology is not proof of a teacher–student or textual-transmission link.

## 11. UNRESOLVED register

Required fields:
- `unresolved_id`
- `description`
- `blocking_stage`
- `required_evidence`
- `status`

Permitted statuses: `OPEN`, `IN_REVIEW`, `RESOLVED`, `BLOCKED`, `REJECTED_WITH_EVIDENCE`.

Example record supplied by the project:
- `unresolved_id: U10`
- `description: 44 letters in row 25`
- `blocking_stage: RELATION_EXTRACTION`
- `status: OPEN`

Do not close an unresolved item by substituting an assumption. Record resolution evidence and the exact affected downstream gates.

## 12. Stage and gate rules

A record or subsystem may not move from `SOURCE` to `CONFIGURATION` without the required `LINEAGE`, `RELATIONS`, `LOGIC`, and `VERIFICATION) stages. If any required stage is incomplete, mark the dependent result `REVIEW_ONLY` or `BLOCKED`.

Required gates:
- `SOURCE_LINEAGE_COMPLETE`
- `RELATION_EXTRACTION_COMPLETE`
- `LOGICAL_CLOSURE_COMPLETE`
- `VERIFICATION_COMPLETE`
- `CONFIGURATION_ALLOWED`
- `WEIGHTS_ALLOWED`

Gate status must be supported by auditable evidence, not by declaration alone.

## 13. LOGIC_BEFORE_WEIGHT_CONTRACT

- Logic and evidence precede any weight assignment.
- `WEIGHTS = FORBIDDEN` while any blocking `UNRESOLVED = OPEN`, and until all required logic and verification gates pass.
- Do not invent, estimate, normalize, or backfill numeric weights.
- Keep missing weights explicitly `NOT_CREATED`.
- Preserve the user's epistemic sequence: `מוחש → הכרח → מושכל`.
- Static definitions may serve as anchors; relations and understanding may be revised iteratively when evidence changes. Preserve version history and drift.

## 14. Quantum Bridge

The Quantum Bridge is `REVIEW_ONLY` unless and until its mapping claims, input provenance, derivation rules, and validation evidence are documented. `REPRESENTATION_ONLY` must not be confused with experimentally verified physical correspondence. No physical or computational performance claim is verified by inclusion in this contract.

## 15. WANGA-OS and implementation claims

WANGA-OS components, architectures, numerical parameters, performance values, hardware mappings, and deployment descriptions must each be classified as one of:
- source-attested specification,
- implemented and test-verified,
- derived,
- representation only,
- proposed,
- unresolved.

Attach repository path, commit SHA, test evidence, and source provenance when applicable. A design description is not evidence of implementation; a code file is not evidence that a system was deployed or achieved a stated performance.

## 16. Anti-Drift controllers

For each detected drift, preserve:
- `drift_id`
- original value/text and source
- changed value/text and source
- exact difference
- stage first affected
- evidence and lineage
- downstream dependencies
- status and resolution decision

Never silently overwrite original wording. Corrections create a new version and link back to the earlier record.

## 17. Repository and change governance

- Keep this master contract versioned and reviewable in Git.
- Each meaningful change requires a commit message that identifies the changed rule or section.
- Do not delete source history, unresolved records, or failed extraction logs merely to produce a clean presentation.
- Generated summaries and dashboards must link to the underlying source records and evidence.
- Secrets, credentials, private keys, access tokens, and private personal data must never be committed.
- A commit confirms a repository change, not the truth of the content.
- Component repositories may reference this contract, but local additions must identify their scope and may not silently override this master contract.

## 18. Current reported project state

The following values are carried forward as **reported state**, not independently re-certified by this document:

```text
SOURCE_LINEAGE_COMPLETE = TRUE
RELATION_EXTRACTION_COMPLETE = PARTIAL
LOGICAL_CLOSURE_COMPLETE = FALSE
VERIFICATION_COMPLETE = FALSE
CONFIGURATION_ALLOWED = FALSE
WEIGHTS_ALLOWED = FALSE

WANGA_STATUS = LOGICAL_BOUNDARY_REACHED
OPEN_UNRESOLVED = 34
CONFIGURATION = REVIEW_ONLY
WEIGHTS = NOT_CREATED
```

Because relation extraction is partial and logical closure and verification are incomplete, configuration and weights remain disallowed. The reported `SOURCE_LINEAGE_COMPLETE = TRUE` requires evidence audit before it can be treated as a passed gate.

## 19. Minimum acceptance checklist

Before approving a source-backed result:
1. Source identity and location are specific enough to re-open.
2. Exact quote is separated from paraphrase and ruling.
3. Verification method and date reflect checks actually performed.
4. Lineage edges have documentary evidence.
5. Derived relations identify their inputs and derivation.
6. Contradictions, variants, and drift remain visible.
7. Blocking unresolved items are linked to affected gates.
8. No weights exist while the contract forbids them.
9. Configuration and implementation claims have commit/test evidence.
10. The resulting status is auditable by another researcher.

## 20. Versioning and amendments

**Version:** 1.0  
**Status:** `BINDING_IMMUTABLE` for this version.  
Any change must be a new version with a change log, rationale, evidence, affected sections, migration notes, and explicit authorization. Do not retroactively edit history to make the new state appear original.

## 21. Audit note

This file is a governance contract and registry scaffold. It does not certify the truth of source claims, the completeness of any repository, or the existence/performance of proposed WANGA/Quantum systems. Those claims require their own evidence records and verification results.
