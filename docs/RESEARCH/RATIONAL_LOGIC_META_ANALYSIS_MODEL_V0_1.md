# Rational Logic Meta-Analysis — Rule-Space Model v0.1

Status: CANDIDATE / RESEARCH MODEL
Purpose: define the object of analysis before implementing schemas or code.

## 1. Central distinction

The object under investigation is not the book of logic, and it is not a software architecture.

The proposed object is a **rule-space of possible rational configurations**.

The Maimonidean logical corpus is treated as a source corpus from which an analytical vocabulary can be extracted. That vocabulary is then used to inspect bounded regions of the rule-space.

```text
                         RULE-SPACE
                enormous / combinatorial / open
                             │
              ┌──────────────┴──────────────┐
              │                             │
       possible configurations        observed cases
              │                             │
              └──────────────┬──────────────┘
                             │
                   ANALYTICAL OPERATORS
                             │
                 extracted from sources
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
      distinction         relation          condition
          │                  │                  │
       subject            predicate          scope
       object             contrast           time
       class              dependency         exception
       role               implication        context
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                    STRUCTURAL TESTING
                             │
          contradiction / compatibility / transformation
                             │
                       REPRESENTATION
                             │
                 only after semantics are fixed
```

## 2. What the rule-space means

A configuration is not assumed to be a sentence, proposition, syllogism, legal rule, or text.

At the present stage it is a bounded arrangement of distinctions and relations that can be tested.

Candidate dimensions include:

- entities / subjects;
- predicates / properties;
- relations;
- roles;
- conditions;
- scopes;
- temporal position;
- source attribution;
- modality;
- exceptions;
- implicit premises;
- explicit premises;
- transformations;
- ordering;
- level of description;
- literal vs non-literal presentation;
- teaching simplification;
- deliberate concealment;
- derived consequences.

These are **candidate dimensions**, not established ontological atoms.

## 3. The seven causes of apparent contradiction

The seven causes should be represented as **analytical mechanisms** rather than as seven primitive objects.

### C1 — Different authors / attributed positions

A contradiction can arise when a compilation combines positions belonging to different authorities without explicit attribution.

Analytical operation: SAME_TEXT? -> NO; SAME_AUTHOR? -> NO.

### C2 — Revision / change of position

The same author may hold one position and later revise it.

Analytical operation: SAME_AUTHOR? -> YES; SAME_TIME/EDITION? -> NO.

### C3 — Non-literal / layered expression

Two statements can conflict under one reading while not conflicting under another representational level.

Analytical operation: READING_LEVEL_1 != READING_LEVEL_2.

The model must not assume in advance that one level is correct.

### C4 — Hidden condition or changed subject

A condition may be omitted, or the subject/reference class may change.

Analytical operation: VISIBLE_RULE(A) != FULL_RULE(A | CONDITION).

This is particularly important for later test cases involving graded eligibility or status-dependent rules. Such cases are validation fixtures, not evidence for C4.

### C5 — Pedagogical simplification

A preliminary formulation may be intentionally simplified so that a difficult concept can first be understood, and only later refined.

Analytical operation: TEACHING_FORM_1 -> REFINED_FORM_2.

The early statement must not automatically be classified as error.

### C6 — Deep derivational separation

Two statements may appear compatible until additional valid premises are introduced and consequences are derived.

Analytical operation: P1 + A1 -> C1; P2 + A2 -> C2; C1 CONTRADICTS C2.

This requires multi-step derivation and therefore cannot be reliably detected by local text comparison alone.

### C7 — Deliberately concealed tension

A source may distribute or conceal incompatible premises so that the reader must perform a deeper investigation.

This is a **hypothesis about authorial construction** unless the source itself provides evidence for intentional concealment.

Analytical operation: P1 + P2 -> TENSION; TEXT_PRESENTATION -> OBSCURES(TENSION)?

The final predicate must remain uncertain unless independently supported.

## 4. The atomic analytical vocabulary

The word atomic here means **minimum extracted analytical unit for a particular method**, not metaphysical atom.

Candidate extraction units:

```text
SOURCE
  ↓
PASSAGE
  ↓
CLAIM
  ↓
TERM / EXPRESSION
  ↓
DISTINCTION
  ↓
RELATION
  ↓
CONDITION
  ↓
TRANSFORMATION
  ↓
CONSEQUENCE
```

The extraction method must be allowed to change. If a supposed primitive disappears under a different extraction procedure, it is not yet a stable primitive.

## 5. The mega-analysis

The intended system therefore operates as:

```text
RULE-SPACE
    ↓
select bounded configuration
    ↓
extract observable structure
    ↓
apply candidate analytical operators
    ↓
derive consequences
    ↓
compare configurations
    ↓
locate compatibility / contradiction / transformation
    ↓
classify explanation
    ↓
validate against source and perturbations
```

This is not a claim that the complete rule-space is enumerable.

The research problem is to construct **bounded, reproducible traversals** through the space.

## 6. Evidence discipline

| State | Meaning |
|---|---|
| SOURCE | directly present in a source |
| OBSERVATION | directly retrieved or measured |
| EXTRACTION | structurally extracted from source material |
| CANDIDATE | proposed analytical structure |
| INFERENCE | derived interpretation |
| HYPOTHESIS | testable but unverified |
| VALIDATED | survived defined tests |
| REPRESENTATION | formal encoding of already-defined semantics |
| IMPLEMENTATION | executable realization |

No implementation state upgrades a hypothesis into evidence.

## 7. Required validation

1. **Source perturbation** — does a different passage extraction change the result?
2. **Context perturbation** — does adding/removing relevant context change the classification?
3. **Subject perturbation** — does changing the reference class expose a hidden condition?
4. **Temporal perturbation** — does chronology change the apparent contradiction?
5. **Reading-level perturbation** — does changing interpretation level change the result?
6. **Attribution perturbation** — does attribution resolve the conflict?
7. **Derivation replay** — can another run reproduce the same derived consequence?

## 8. What is explicitly not assumed

The following are not yet axioms:

- that the seven causes are exhaustive for all contradictions;
- that every contradiction has exactly one cause;
- that every cause is independent;
- that subject, relation, condition, etc. are universal ontological primitives;
- that the rule-space is finite;
- that all source structures can be represented as a single graph;
- that later legal/social examples prove anything about the original source.

## 9. First formal research question

Can the seven causes be converted from a textual taxonomy into a **testable operator system** while preserving source attribution, uncertainty, overlapping causes, and cases that remain unresolved?

Only after this question is answered should a machine schema or implementation be promoted to a canonical representation.