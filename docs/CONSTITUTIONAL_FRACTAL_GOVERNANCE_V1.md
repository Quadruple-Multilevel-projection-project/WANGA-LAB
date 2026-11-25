# Constitutional Fractal Governance — WANGA-LAB

**Version:** 1.0  
**Date:** 2026-11-25  
**Status:** GOVERNANCE SPECIFICATION — proposed as the canonical cross-model coordination contract; runtime enforcement is NOT_YET_VERIFIED.  
**Scope:** Logic-fractal research, multi-model cabinet coordination, source extraction, composition, verification, and repository updates.

## 1. Purpose and authority

This document defines the constitutional constraints that every model, agent, tool, and human contributor must preserve while reading, extending, composing, or reporting WANGA-LAB logic structures.

It is a governance and traceability specification. It does not claim that every rule is already enforced by code, that all providers are connected, or that a diagram proves implementation.

Precedence for this research workflow:

1. Exact source material and its recorded version/span.
2. Explicit project contracts and schemas linked to that source.
3. Executable implementation and named test evidence.
4. Reviewed interpretations and hypotheses.
5. Diagrams, summaries, and navigation links.

A lower-precedence representation must not silently overwrite a higher-precedence source. A conflict is recorded, not guessed away.

## 2. Constitutional invariants (must survive every scale)

**CF-01 — Source before conclusion.** Every source-backed claim retains a resolvable source ID, repository path or URL, version/commit where available, and exact locator/span. An assumption must be explicitly marked as an assumption.

**CF-02 — Epistemic status is immutable by inheritance.** Composition, repetition, translation, summarization, or model agreement cannot upgrade HYPOTHESIS / CANDIDATE / NOT_YET_VERIFIED to VERIFIED. Verification requires a named check and evidence record.

**CF-03 — Relation type is explicit.** An editorial/navigation link, association, dependency, formal precondition, derivation, implementation call, validation check, and hypothesis link are different edge types. Never infer entailment, causality, symmetry, transitivity, identity, or equivalence from a generic link.

**CF-04 — Type and scope preservation.** Inputs, outputs, types, domain, scope, preconditions, constraints, and exceptions must be retained through composition. Scope expansion requires explicit supporting evidence and review.

**CF-05 — No silent premise or rule creation.** Every new conclusion must identify its premises and the exact rule/contract used. Missing premises, unsupported rules, ambiguous types, or dangling references block promotion.

**CF-06 — Deterministic provenance.** Candidate composition records parent IDs, rule ID/version, canonical representation/hash where implemented, and build/test receipt. A hash proves identity/integrity of bytes, not truth.

**CF-07 — Bounded recursion.** Recursive expansion must have declared limits, cycle handling, and a termination condition. The existing contracts reject unbounded recursive cycles; any runtime limit must be separately specified and tested, not invented in a report.

**CF-08 — Contradictions remain visible.** Contradictory claims are stored as separate claims with their sources, scopes, timestamps/versions, and status. No model may silently merge, delete, or resolve them. Resolution requires an explicit adjudication record and test or source rationale.

**CF-09 — No statistical shortcut to logical validity.** Similarity, model consensus, confidence, parameter/weight adjustment, or repeated outputs are not substitutes for source-backed premises, formal rules, semantic tests, and independent review. Existing source-first-before-weights contract remains a project constraint; no new weights or numerical values are introduced by this document.

**CF-10 — Fail closed when required evidence is missing.** Use REVIEW / ABSTAIN / HALT as workflow outcomes when a required source, type, premise, rule, verification receipt, or scope condition is absent or contradicted. This is a required policy behavior; code enforcement must be tested before claiming it is automatic.

## 3. Fractal levels and inheritance

The constitutional layer applies to the existing logic-fractal scale model; it does not replace or rename L0–L3.

| Scale | Existing role | Constitutional obligations | Promotion boundary |
|---|---|---|---|
| L0 | Source-grounded primitive | Exact source span or explicit assumption; stable ID; claim status; scope | No source-backed claim without provenance |
| L1 | Typed fragment | Typed inputs/outputs; parent IDs; source lineage; constraints; tests | Structural validity is not semantic truth |
| L2 | Recursive composition candidate | Declared composition rule; parent hashes/IDs; inherited invariants; scope intersection or documented expansion; cycle bound | Candidate only until semantic checks |
| L3 | Model candidate | Versioned graph; positive/negative/boundary cases; frozen holdout; counterexamples; MIRROR review; contradiction inventory | Human review readiness only after the configured gate passes |

A higher level inherits all lower-level obligations. No higher-level summary may erase lower-level provenance or epistemic status.

## 4. Typed relation contract

Use the relation types already established in the traceability map:

- EDITORIAL_LINK
- SOURCE_SUPPORTS_CLAIM
- FORMAL_PRECONDITION
- FORMAL_DERIVATION
- DATA_DEPENDENCY
- IMPLEMENTATION_CALL
- VALIDATION_CHECK
- FEEDBACK_EVENT
- HYPOTHESIS_LINK

Every machine-readable edge should carry: `edge_id`, `source_id`, `target_id`, `edge_type`, `status`, `source_refs`, `rule_or_rationale`, `scope`, `created_version`, and `verification_evidence` (or an explicit empty/not-yet-available value).

A taxonomy edge remains an EDITORIAL_LINK / EDITORIAL_RELATION_CANDIDATE unless a separate formal rule and evidence establish a stronger relation.

## 5. Conflict and contradiction protocol

When two sources or models disagree:

1. Preserve both original claims verbatim or with faithful bounded excerpts.
2. Record source path, exact locator, version/commit, model/report ID, and epistemic status for each.
3. Identify whether the disagreement is factual, definitional, scope-related, temporal, type-related, or interpretive.
4. Do not merge or select a winner automatically.
5. Specify the evidence or test needed for adjudication.
6. Keep the conflict OPEN until an authorized review records a reasoned decision.
7. Retain the superseded claim and decision history after resolution.

A model's agreement with another model is not independent verification unless the verification procedure and independence are demonstrated.

## 6. Model handoff contract

Every model declares only capabilities it actually has:

- model/provider and version if exposed;
- tools/connectors actually available;
- repository read/write permissions;
- context/output constraints only if known;
- assigned round, task ID, repository scope, and paths;
- whether it can run code/tests or only inspect source.

Task size is adapted to capability, not brand. A limited model receives one bounded repository/path and a short evidence-row deliverable. A stronger model may receive cross-repository comparison, contradiction review, or independent verification. Any model may request subdivision or ABSTAIN.

Required report row:

`ID | Model | Round | Source(repo/path#locator) | Finding | Explicit/Implicit | Relation type | Status | Gap/Conflict | Evidence/Test | Next action`

Do not claim that a report has synchronized other providers until a repository commit, workflow event, or receiving-side acknowledgement proves it. GitHub is the shared record; it does not make models communicate spontaneously.

## 7. Verification and release boundary

Keep these statuses distinct:

- SOURCE: source content directly observed.
- FORMAL_RULE: explicit syntax/semantics or executable rule.
- IMPLEMENTED: code exists at the cited path/version.
- TESTED: named test was executed and result recorded.
- VERIFIED: the defined verification contract is satisfied.
- INTERPRETATION / HYPOTHESIS / UNKNOWN: not established as verified.

The existing readiness gate is `CONFIGURED_NOT_EMPIRICALLY_VALIDATED`; its thresholds are project policy, not universal scientific cutoffs. The semantic benchmark plan is `SPECIFIED_NOT_POPULATED`. Recursive composition contracts remain `CANDIDATE_CONTRACTS_NEED_SEMANTIC_BENCHMARK`. Do not report the first model as release-ready until the actual evidence and review requirements are satisfied.

Structural validation, JSON/schema validation, type compatibility, hashing, deterministic reconstruction, SAT/UNSAT results, and diagram generation each answer limited questions. None alone proves semantic truth, universal correctness, safety, or physical realization.

## 8. Relationship to existing five-gate handoff

The repository's documented five-gate sequence remains unchanged:

1. L1 — First-Order Structural Logic
2. L2 — Derivation Logic
3. L3 — Relation / Rule Validation
4. Evidence / Provenance Filter
5. Deterministic Output Filter

These are workflow control gates, not five separate formal logics. This constitutional specification governs how evidence and status must pass through them; it does not claim automatic runtime enforcement without traces and tests.

## 9. Daily coordination and diagram consistency

- The repository files and their commits are the source of truth; diagrams are derived views.
- Every daily update records date, commit SHA, changed paths, model/task IDs, and unresolved conflicts.
- The diagram must label proposed/not-yet-verified components and must not imply provider integrations that are not configured.
- If code, contract, README, and diagram disagree, create a conflict record and correct the derived view only after checking the source.
- Never overwrite a model's prior report; use append-only or uniquely named reports.

## 10. Acceptance checklist for future changes

Before accepting a new fractal rule, model, plugin, or diagram edge, verify:

- [ ] Source and exact locator exist, or the item is explicitly an assumption.
- [ ] Stable IDs are unique; all parents and source references resolve.
- [ ] Relation type and epistemic status are explicit.
- [ ] Inputs, outputs, types, scope, preconditions, and constraints are preserved.
- [ ] Composition rule and version are recorded.
- [ ] Recursion is bounded and cycles are handled.
- [ ] Contradictions and counterexamples are retained.
- [ ] Required tests and their actual results are linked.
- [ ] No status promotion occurred without the verification contract.
- [ ] Diagram edges match the documented/code-backed status.

## 11. Source documents

- [Logic/fractal architecture V2](LOGIC_WIKI_FRACTAL_ARCHITECTURE_V2.md)
- [FOL, second-order and fractal traceability map](FOL_SECOND_ORDER_FRACTAL_WANGA_TRACEABILITY_MAP_HE_V1.md)
- [Logic architecture correction and traceability V1](LOGIC_ARCHITECTURE_CORRECTION_AND_TRACEABILITY_V1.md)
- [Recursive composition contracts](../logic_fractal/data/recursive_composition_contracts_v1.json)
- [Composition rules](../logic_fractal/data/composition_rules.json)
- [Fractal taxonomy](../logic_wiki/data/fractal_taxonomy.json)
- [Readiness gate](../logic_wiki/data/readiness_gate.json)
- [Semantic benchmark plan](../logic_fractal/data/semantic_benchmark_plan_v1.json)
- [Fragment composer](../logic_fractal/fragment_composer.py)
- [Governance kernel](../governance/kernel.py)

**Implementation status:** This is a canonical documentation proposal until reviewed and adopted by the project owner. No claim of complete automated enforcement is made.
