# Axiomatic Hierarchy and Keystone Review

**Status:** SPECIFIED / NOT_YET_VERIFIED

## Purpose

Provide a repeatable way to distinguish rules from meta-rules and assumptions about the rule system. “Keystone” is a candidate classification, not an axiom granted by intuition or unusual wording.

## Three review levels

1. **Object level (L1):** explicit facts, symbols, predicates, and rules within a declared domain.
2. **Derivation level (L2):** permitted inference steps, variable binding, rule composition, and proof obligations over L1.
3. **Meta level (L3):** assumptions about interpretation, rule selection, consistency, closure, source authority, and applicability boundaries.

A statement may occupy different levels in different formalizations. Record the chosen level and justify it; do not infer the level from vocabulary alone.

## Keystone candidate test

For a proposed element K, record:
- stable ID and exact source locator;
- literal source span and hash where available;
- formal role and dependencies;
- the structure expected to depend on K;
- a baseline evaluation with K;
- ablation: remove K;
- perturbation: replace K with a plausible alternative;
- counter-reading and boundary cases;
- results, reviewer, and reproducibility details.

A collapse under ablation is evidence of structural dependency in that specific representation. It does **not** prove that K is universally true, unique, or ontologically necessary. A structure that collapses because the implementation hard-coded K is a circular test and must be reported as such.

## Decision states

- `CANDIDATE`: a hypothesis awaiting tests.
- `STRUCTURALLY_DEPENDENT`: ablation changes the specified output under recorded conditions.
- `SOURCE_SUPPORTED`: the source supports the recorded wording/claim, subject to its context.
- `FORMALLY_VALID`: the declared derivation passed the stated formal checks.
- `VERIFIED`: only when the named verification procedure passed and its evidence is archived.
- `REJECTED` or `INCONCLUSIVE`: the candidate fails or evidence is insufficient.

Do not collapse these states into one confidence score.
