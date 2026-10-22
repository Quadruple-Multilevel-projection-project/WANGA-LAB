# WANGA MASTER RESEARCH CONTRACT V1

**Status:** PROPOSED — REVIEW_ONLY  
**Branch:** `review/wanga-master-research-contract-v1`  
**Intended role:** Research and evidence-control contract for WANGA-LAB / PCE / Sefer HaLogic work  
**Authority boundary:** This document is subordinate to `docs/MASTER_PROJECT_INSTRUCTIONS_V1.md`. It does not replace that file or silently change repository-wide invariants.  
**Promotion rule:** Do not treat this proposal as active policy until reviewed, tested where applicable, and accepted through the repository's normal review process.

## 1. Purpose and scope

Unify source provenance, textual extraction, relationship mapping, dynamic-logic analysis, verification, unresolved-item handling, configuration eligibility, and weight governance.

This contract covers:
- Sefer HaLogic and related source-grounded research;
- the PCE (Particle Calculus Engine) rules supplied by the project owner;
- the halakhic-source citation and quotation register;
- SOURCE_LINEAGE and drift records;
- unresolved questions and verification gates;
- proposed configuration and weight-generation boundaries.

This contract does **not** certify that any quotation, attribution, source lineage, architecture, or runtime capability is true merely because it is listed here.

## 2. Epistemic order

Use this dependency order as a research workflow, not as a claim that every stage is already complete:

```text
SOURCE
  -> SOURCE_LINEAGE
  -> EXTRACTION
  -> RELATIONS
  -> DYNAMIC_LOGIC
  -> VERIFICATION
  -> CONFIGURATION_REVIEW
  -> WEIGHTS_REVIEW
```

A downstream stage must retain references to its upstream evidence. If a prerequisite is absent, contradictory, or not yet checked, mark the item `UNRESOLVED`, `BLOCKED`, or `REVIEW_ONLY`; do not fill the gap with an invented fact or weight.

**Project terminology:** The research objective is dynamic logic. Do not silently rename it “formal logic” or treat the source system as a closed, immutable mathematical system.

## 3. Evidence classes

Use these classes to distinguish what is observed from what is inferred:

- `OBSERVATION` — directly observed in a cited artifact or repository state.
- `RAW_EVIDENCE` — source text, scan, metadata, or other preserved evidence.
- `EXTRACTED` — transcribed or structured from a named source, with location recorded.
- `DERIVED` — follows from explicitly identified inputs and a reproducible derivation.
- `INFERENCE` — reasoned conclusion that is not directly stated by the source.
- `HYPOTHESIS` — proposal requiring further evidence.
- `REPRESENTATION_ONLY` — a schema, mock, diagram, or model that does not itself prove the represented system exists.
- `CONFLICT` — incompatible readings, attributions, states, or evidence.
- `UNRESOLVED` — required evidence or a decision is missing.
- `VERIFIED_RESULT` — passed a specified verification procedure whose evidence is recorded.

Never promote `INFERENCE`, `HYPOTHESIS`, or `REPRESENTATION_ONLY` to `VERIFIED_RESULT` without a documented verification procedure.

## 4. Source and lineage requirements

Every source-derived claim must preserve, where available:

```text
source_id
source_name
source_type
edition_or_version
author_or_attributed_author
source_location
page_or_folio
stable_url
retrieval_date
source_artifact_hash
transcription_method
transcriber_or_process
lineage_id
parent_record_ids
evidence_class
```

Lineage must represent evidenced transmission or derivation, not a guessed historical sequence. Record the exact basis for a teacher–student or text-to-text relationship. If evidence is absent, preserve the relation as `UNRESOLVED`; do not infer lineage from chronology, similarity, or consensus alone.

Preserve source wording and variant readings. Normalize only in a separate field; never overwrite the diplomatic/source transcription.

## 5. Research record schema

Minimum common fields:

```text
record_id
source_id
source_name
source_type
source_location
quote
claim_or_ruling
state_label
evidence_class
verification_status
verification_method
verification_confidence
verification_date
verification_notes
source_url
lineage_id
parent_record_ids
unresolved_ids
record_created_at
record_updated_at
```

Domain-specific records may add fields, but must not remove provenance or verification fields. Use stable IDs; do not recycle an ID after a record is withdrawn or corrected.

## 6. Controlled vocabulary — verification_status

Only the following values are valid for `verification_status`:

| Code | Meaning |
|---|---|
| `VERIFIED_PRIMARY` | Exact claim or quotation checked against a primary source text. |
| `VERIFIED_SCAN` | Checked against an identified scan or facsimile. |
| `VERIFIED_DIGITAL` | Checked against a named digital text repository. |
| `VERIFIED_MULTIPLE` | Independently checked against multiple identified witnesses; list each witness. |
| `PARTIAL_VERIFICATION` | Source found, but the full claim or quotation has not been checked word-for-word. |
| `SOURCE_FOUND` | Candidate source located; quotation/claim not yet checked. |
| `RESEARCH_ONLY` | Appears only in project research material currently available. |
| `SECONDARY_SOURCE_ONLY` | Supported only by a secondary source. |
| `UNVERIFIED` | Verification has not been performed. |
| `DISPUTED` | Conflicting witnesses, readings, or attributions exist. |
| `MISATTRIBUTED` | Evidence indicates the attribution is incorrect. Preserve the evidence. |
| `SOURCE_MISSING` | No source has yet been located. |
| `QUOTE_MISMATCH` | Located source does not match the registered quotation. |
| `BLOCKED` | Verification cannot proceed; record the blocking reason. |

A source being present in an uploaded workbook is not, by itself, evidence of primary-source verification. A link to a general homepage is not proof that the exact passage was checked.

## 7. Controlled vocabulary — verification_method

Allowed values:

```text
PRIMARY_TEXT
PRINTED_EDITION
SCANNED_EDITION
SEFARIA_CHECK
HEBREWBOOKS_CHECK
WIKISOURCE_CHECK
LIBRARY_CATALOG
SCHOLARLY_REFERENCE
MANUAL_COMPARISON
CROSS_REFERENCE
RESEARCH_DOCUMENT
ORAL_REPORT
NOT_VERIFIED
```

When relevant, record the exact edition, URL, folio/page, access date, and comparison scope in `verification_notes`. A method code alone does not establish that the method was successfully completed.

## 8. Controlled vocabulary — verification_confidence

Allowed values:

- `HIGH`
- `MEDIUM`
- `LOW`
- `UNKNOWN`

Confidence is a researcher's assessment of the evidence quality, not a substitute for verification status. Never use confidence to conceal a missing source or unresolved contradiction.

## 9. verification_notes

`verification_notes` is free text. It should explain the evidence and the remaining limitation, for example:

- “Compared against the identified printed edition, folio/page recorded.”
- “Checked against a scan on HebrewBooks; edition and page still need confirmation.”
- “Found in the research workbook; primary source not yet located.”
- “Variant readings occur between witnesses; both transcriptions retained.”
- “Quotation is abbreviated relative to the source.”
- “Similar wording found, but not an exact match.”
- “Attribution is uncertain; no direct evidence of authorship found.”
- “Blocked because the referenced scan is unavailable.”

Do not write “verified” without naming what was checked and where.

## 10. Halakhic-source register

The following names are **candidate register entries supplied in project notes**, not a declaration that their quotations have been verified. Keep each distinct work/passage as a separate record and attach exact passage text and a stable passage-level link only after checking.

Suggested initial records:
- Talmud Bavli, Sanhedrin 7b
- Rambam, Mishneh Torah, Hilkhot Sanhedrin 4:14
- Rambam, Mishneh Torah, Hilkhot Sanhedrin 4:15
- Kesef Mishneh on the relevant Rambam passage
- Radbaz on the relevant Rambam passage
- Radbaz, Responsa, part 3, responsum 510 (citation as supplied; verify numbering)
- Tur, Choshen Mishpat 8
- Rosh, Sanhedrin 1:3
- Rashba, Responsa, part 7, responsum 518 (citation as supplied; verify numbering)
- Rivash, responsum 271 (citation as supplied; verify numbering)
- Maharik, shoresh 84
- Meiri, Sanhedrin 7b
- Sefer HaChinukh, mitzvah 491 (citation as supplied; verify numbering/edition)
- Sefer Hasidim, siman 1115 (citation as supplied; verify numbering/edition)
- Maharshdam, Choshen Mishpat, responsum 1
- Chatam Sofer, Choshen Mishpat, responsum 19
- Arukh HaShulchan, Choshen Mishpat 8:2
- Rabbi Yosef Yedid Halevi, *VeLevi Amar* (edition and passage locator required)
- Chazon Ish, *Kovetz Igrot*, vol. 1, letter 23 (edition and pagination required)

All supplied citation numbers are provisional until checked against a named edition. Do not invent missing quotation text; use an explicit missing-value marker and keep the record unresolved.

## 11. PCE rules supplied by the project owner

The following rule labels are preserved as **owner-supplied requirements**. Their implementation and enforceability must be verified separately:

```text
RULE_01 LATTICE IMMUTABLE
RULE_02 DRIFT IS DATA
RULE_03 NO INTERPRETATION
RULE_04 EXECUTED OR BLOCKED
RULE_05 UNKNOWN INPUT = BLOCK
RULE_06 EVERYTHING LOGGED
RULE_07 CONSENSUS != TRUTH
RULE_08 LINEAGE REQUIRES EVIDENCE
RULE_09 IM_HAKOLEL
RULE_10 AUTHORITY OVERRIDE
RULE_11 AUTO REVOCATION
RULE_12 EXECUTOR IS TOOL
```

These labels do not authorize an agent to override repository access controls, safety/security controls, source evidence, or the repository's canonical project instructions. Any authority-revocation or override mechanism requires a defined scope, evidence, audit trail, and tested implementation.

## 12. Drift and contradiction handling

`DRIFT` is evidence to preserve, not noise to delete. For every detected change, retain:

```text
drift_id
source_record_before
source_record_after
changed_span_or_relation
source_lineage
detection_method
classification
impact
verification_status
resolution_status
```

Keep competing readings until evidence resolves them. Do not silently reconcile incompatible claims. A correction must create an auditable revision linked to the prior record.

## 13. UNRESOLVED register

Every open question must contain:

```text
unresolved_id
description
blocking_stage
required_evidence
owner_or_responsible_process
status
created_at
last_reviewed_at
resolution_evidence
```

Permitted lifecycle values:

```text
OPEN
IN_PROGRESS
BLOCKED
RESOLVED
REJECTED_WITH_EVIDENCE
```

Example shape only (not a factual finding): an unexplained letter-count discrepancy would be assigned an ID, linked to its source records, and remain `OPEN` until the required evidence is captured.

Any reported unresolved count (including the project-notes figure of 34) must be reconciled against the current unresolved register before it is presented as current repository state.

## 14. Stage gates

Do not treat a gate as passed merely because its name exists in a document.

1. `SOURCE_LINEAGE_COMPLETE` — all in-scope records have traceable source lineage or an explicit, accepted exception.
2. `RELATION_EXTRACTION_COMPLETE` — all in-scope relations have evidence references and unresolved relations are accounted for.
3. `LOGICAL_CLOSURE_COMPLETE` — the defined scope has passed its stated contradiction, counterexample, and closure checks.
4. `VERIFICATION_COMPLETE` — every required claim has an accepted status and the evidence is retained.
5. `CONFIGURATION_ALLOWED` — configuration changes have passed review, dependency checks, and applicable tests.
6. `WEIGHTS_ALLOWED` — a separately approved contract permits weight creation and every prerequisite gate is satisfied.

If a gate has not been tested, its state is `NOT_VERIFIED`, not `TRUE`.

## 15. Weight governance

```text
WEIGHTS = NOT_CREATED
```

This is the safe default for this proposal. Do not create, infer, or backfill numeric weights from consensus, confidence, intuition, or missing data. Any future weight system requires a separately approved specification, explicit source/derivation for every value, reproducibility, and an audit trail. Open unresolved items block weight promotion unless an approved scope-specific exception documents why the item is non-blocking.

## 16. Configuration and deployment boundary

The allowed default state for this document is:

```text
CONTRACT_STATUS = PROPOSED
CONFIGURATION = REVIEW_ONLY
WEIGHTS = NOT_CREATED
DEPLOYMENT = NOT_AUTHORIZED_BY_THIS_DOCUMENT
```

No source register or architecture description should be presented as deployed capability without independent repository/runtime evidence. Use the repository's existing branch, test, review, and promotion workflow. Do not commit directly to `main` for this proposal.

## 17. Audit and completion report

Every implementation or research run should report:

```text
OBSERVED
CHANGED
TESTED
VERIFIED
UNRESOLVED
BLOCKED
NEXT_ACTION
```

Cite repository paths, commit IDs, source locations, and test outputs where applicable. Distinguish “file created” from “contract accepted,” “code exists” from “code executed,” and “source located” from “quotation verified.”

## 18. Acceptance checklist

- [ ] Parent contract compatibility reviewed.
- [ ] Terminology and scope reviewed by the project owner.
- [ ] Source and lineage fields mapped to existing schemas without duplicate authorities.
- [ ] Controlled vocabularies validated in schema/tests.
- [ ] Existing records migrated without inventing missing values.
- [ ] Unresolved register reconciled with repository state.
- [ ] Tests cover missing sources, quote mismatches, conflicting witnesses, and blocked gates.
- [ ] Review approved before promotion to canonical project policy.

**Current decision:** `REVIEW_ONLY`. This file consolidates requirements for review; it does not assert that the listed gates have passed or that source citations have been verified.
