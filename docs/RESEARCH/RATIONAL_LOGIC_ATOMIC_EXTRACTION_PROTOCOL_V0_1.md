# Atomic Extraction Protocol — Rational Logic v0.1

## Goal

Extract analytical units from rational-logic sources without prematurely turning textual terminology into fixed ontology.

## Pipeline

```text
SOURCE
→ PASSAGE
→ ATTRIBUTION
→ OBSERVATION
→ EXTRACTION
→ CANDIDATE OPERATOR
→ TEST CASE
→ PERTURBATION
→ VALIDATION
→ REPRESENTATION
```

## Extraction record

For each passage, record:

1. source identifier;
2. exact passage boundaries;
3. speaker/author attribution when available;
4. textual statement;
5. explicit subject;
6. explicit predicate;
7. explicit condition;
8. explicit scope;
9. temporal markers;
10. explicit relation;
11. stated transformation;
12. apparent conflict, if any;
13. candidate cause/operator;
14. alternative candidate causes;
15. confidence/status;
16. unresolved questions.

## Rule

Do not fill an absent field with a guessed value.

Use UNKNOWN, not an inferred value, when the source does not establish it.

## Multi-cause cases

A single apparent contradiction may map to more than one candidate cause.

Do not force a one-to-one classification:

CONFLICT -> {C1, C4}

is admissible.

The system must preserve the possibility that later validation removes one or both candidates.

## Atomicity test

A unit is provisionally atomic only if:

- it can be independently cited;
- changing its extraction boundary produces a detectable effect;
- its relation to neighboring units can be stated;
- its provenance remains intact;
- an alternative extraction can be compared.

If these conditions fail, mark the unit COMPOSITE_OR_UNRESOLVED.

## Promotion rule

```text
TEXTUAL TERM
    ↓
EXTRACTED UNIT
    ↓
REPEATED OBSERVATION
    ↓
CANDIDATE STRUCTURAL ROLE
    ↓
PERTURBATION
    ↓
VALIDATED ROLE
```

A term never becomes a primitive merely because it occurs frequently.

## Output boundary

The protocol intentionally stops before JSON/Python.

The next stage is a representation specification defining object semantics and edge semantics. Only after that stage should machine schemas be introduced.