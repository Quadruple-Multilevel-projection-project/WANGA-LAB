# WANGA-LAB — AI AGENT HANDOFF NOTICE

## MANDATORY START

Before performing any action, read `docs/NEXT-MODEL-HANDOFF-KRAKEN.md`.

This notice is an execution boundary, not an optional suggestion.

## FIVE-GATE EXECUTION PIPELINE

Every substantive claim, proposed change, generated artifact, and repository modification must pass these gates in order:

```
L1 — FIRST-ORDER STRUCTURAL LOGIC
        ↓
L2 — DERIVATION LOGIC
        ↓
L3 — RELATION / RULE VALIDATION
        ↓
EVIDENCE / PROVENANCE FILTER
        ↓
DETERMINISTIC OUTPUT FILTER
```

A later gate cannot repair failure at an earlier gate. Do not skip a gate.

## L1 — FIRST-ORDER STRUCTURAL LOGIC

Extract before interpreting. Preserve subject, predicate, relation, participants, participant roles, internal propositions, sentence boundaries, and source location.

Do not reduce structured statements to a bag of concepts.

Do not replace `A —R→ B` with `A = B` unless the source explicitly establishes identity.

## L2 — DERIVATION LOGIC

A conclusion requires explicit premises, a defined rule, and valid application.

Do not invent or silently assume transitivity, identity, causality, equivalence, symmetry, functionality, partition, or other rule properties.

If the derivation cannot be established: `NOT_YET_VERIFIED`.

## L3 — RELATION / RULE VALIDATION

Validate the relation itself and the operations permitted on it. Do not silently promote a source-internal relation into an external ontological claim.

## EVIDENCE / PROVENANCE FILTER

Maintain the distinction:

```
SOURCE → EXTRACTED → FORMALIZED → DERIVED → MAPPED → TESTED → VERIFIED
```

Never silently convert:

- SOURCE → FACT
- INTERPRETATION → FACT
- HYPOTHESIS → FACT
- MAPPING → IDENTITY
- SEMANTIC SIMILARITY → PROVENANCE
- CODE EXISTS → VERIFIED BEHAVIOR

Every transition requires evidence.

If evidence is missing: `NOT_YET_VERIFIED`.

If determination is not possible: `I DON'T KNOW.`

## CONTRADICTIONS

Never hide contradictions. Preserve conflicting source statements and their provenance. Do not silently select one or manufacture a reconciliation.

If unresolved: `I DON'T KNOW.`

## METAPHYSICAL / SOURCE-INTERNAL MATERIAL

Preserve metaphysical, philosophical, symbolic, or Kabbalistic source claims as source-internal claims unless independent evidence establishes an external factual claim.

Do not erase them. Do not promote them.

## DETERMINISTIC OUTPUT FILTER

Only after the previous gates pass, inspect the final output as a string.

Apply deterministic rules for cross-domain contamination, logic gaps, unsupported or invented claims, unsupported attribution, and unsupported verification.

If a rule is triggered: `BLOCK`.

Do not conceal the failure.

## REPOSITORY SAFETY

Before modifying anything:

1. Inspect current repository state.
2. Inspect relevant files.
3. Inspect relevant branches, issues, and PRs.
4. Identify the source supporting the change.
5. Make the smallest justified change.
6. Test the change.
7. Report only what actually happened.

Never restart existing work, invent repository state or provenance, create duplicate tasks, close or merge unauthorized work, or claim verification that did not occur.

## FAILURE / STOP CONDITIONS

Stop immediately for permission denial, missing required source, ambiguous repository state, unresolved merge conflict, unclear test/CI failure, missing derivation rule, or missing verification evidence.

Use:

```
BLOCKED — [category]: [exact issue]
```

Then stop.

## HANDOFF RULE

An agent that does not understand this protocol must not modify the repository.

Required response:

```
BLOCKED — LOGICAL PROTOCOL NOT UNDERSTOOD
```

## REQUIRED REPORTING

Report only:

```
ACTION
SOURCE
TRANSFORMATION
EVIDENCE
RESULT
VERIFICATION
STATUS
```

Permitted statuses:

```
BUILT
SPECIFIED
PROTOTYPED
TESTED
VERIFIED
PLANNED
HYPOTHETICAL
NOT_YET_VERIFIED
OPEN
BLOCKED
```

Do not use `VERIFIED` unless verification actually occurred.

## FINAL RULE

When uncertain:

```
STOP.
STATE THE UNCERTAINTY.
I DON'T KNOW.
```
