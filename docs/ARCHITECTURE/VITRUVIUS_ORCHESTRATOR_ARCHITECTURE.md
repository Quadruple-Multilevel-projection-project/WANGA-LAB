# Vitruvius Orchestrator Architecture

Status: ARCHITECTURE SPECIFICATION
Version: 0.1.0

## Role

Vitruvius is the highest architectural orchestration layer immediately preceding the rational-logic model layer.

Its function is to maintain the whole architectural composition context and to connect the project's accumulated lineage knowledge to the selection of candidate models for the rational-logic core.

Vitruvius does not replace the rational logic layer. It does not define the private implementation of Rational Logic. It provides the architectural selection and integration boundary above it.

## Position

    KNOWLEDGE / RESEARCH LAYERS
              ↓
    ARCHITECTURE FAMILIES
              ↓
    WANGA LINEAGE SYSTEM
              ↓
    LINEAGE MARRIAGE / INTEGRATION
              ↓
    WANGA POLITEIA
              ↓
    VITRUVIUS ORCHESTRATION
              ↓
    MODEL SELECTION FOR LOGIC
              ↓
    RATIONAL LOGIC MODEL LAYER
              ↓
    NEURAL / ALGORITHMIC GOVERNANCE

## Primary responsibilities

1. Maintain the whole-system architectural view.

   Vitruvius represents the current relationship among research objects, lineage families, architectures, models, integrations, descendants, evidence, and validation states.

2. Maintain architectural genealogy as selection context.

   The layer uses the recorded ancestry and descendants of ideas, methods, models, and architectures as contextual knowledge for future composition. It preserves the distinction between documented ancestry and inferred similarity.

3. Reconstruct architectural families.

   Vitruvius must be able to place an architecture in its family history: origin, inherited structure, revisions, branches, merges, superseded forms, and descendants.

4. Connect lineage knowledge to candidate-model space.

   The layer turns the accumulated history of the project into a candidate space of models that may be considered for specific logical roles.

5. Represent composition compatibility.

   Compatibility is a first-class architectural relation with explicit states:

   - COMPATIBLE
   - CONDITIONALLY_COMPATIBLE
   - INCOMPATIBLE
   - UNKNOWN

   Compatibility remains scoped to the evidence and context that produced it.

6. Maintain the model-selection boundary.

   Vitruvius is the boundary at which candidate models are identified and selected for participation in the rational-logic layer. The logical core remains a distinct downstream layer.

7. Preserve the governance context.

   The selected models are understood as functional governors of specific logical responsibilities. Their designation is architectural and functional, not a claim about human authority.

8. Maintain recursive continuity.

   Every new logical model, integration, validation result, or descendant can become new lineage knowledge and therefore new input to future Vitruvius states.

## Core objects

- ARCHITECTURE
- ARCHITECTURE_FAMILY
- LINEAGE
- LINEAGE_EVENT
- INTEGRATION_EVENT
- MODEL
- MODEL_FAMILY
- COMPATIBILITY_OBSERVATION
- CANDIDATE_MODEL_SET
- MODEL_SELECTION
- GOVERNANCE_ROLE
- LOGIC_HANDOFF
- VALIDATION_RECORD
- DESCENDANT

## Selection knowledge

A candidate model should be represented together with its lineage context rather than as an isolated model identifier.

Relevant context includes:

    ORIGIN
    ANCESTRY
    DESCENDANTS
    INHERITED_COMPONENTS
    INTEGRATION_HISTORY
    COMPATIBILITY_HISTORY
    CONFLICT_HISTORY
    VALIDATION_HISTORY
    CURRENT_ARCHITECTURAL_ROLE
    OPEN_QUESTIONS

## Model-selection output

The Vitruvius layer produces a documented architectural selection context for the downstream logic layer:

    candidate models
          ↓
    lineage context
          ↓
    compatibility context
          ↓
    architectural constraints
          ↓
    model selection
          ↓
    LOGIC HANDOFF

The existence of a selection context does not by itself establish that the selected model is correct. Correctness remains a property requiring the applicable validation process.

## Relationship to WANGA Politeia

WANGA Politeia provides the governance and whole-system knowledge context.

Vitruvius is the specialized orchestration layer that operates immediately before the rational-logic model boundary.

Conceptually:

    POLITEIA
       ↓
    "What is the whole system and how are its parts related?"
       ↓
    VITRUVIUS
       ↓
    "Which documented architectural/model structures should compose
     the next logical layer?"
       ↓
    RATIONAL LOGIC

## Relationship to the lineage system

The WANGA Lineage System stores developmental genealogy.

Vitruvius reads that genealogy as architectural selection context.

Therefore:

    LINEAGE HISTORY
          ↓
    LINEAGE KNOWLEDGE
          ↓
    POLITEIA WHOLE-SYSTEM VIEW
          ↓
    VITRUVIUS ARCHITECTURAL ORCHESTRATION
          ↓
    LOGIC MODEL CANDIDATES

## Recursive architectural loop

    CURRENT ARCHITECTURE
          ↓
    LINEAGE OBSERVATION
          ↓
    NEW KNOWLEDGE
          ↓
    VITRUVIUS REASSESSMENT
          ↓
    MODEL-SPACE UPDATE
          ↓
    FUTURE LOGIC COMPOSITION
          ↓
    NEW ARCHITECTURAL DESCENDANT
          ↺

## Precision boundary

Because Vitruvius sits directly above the rational-logic layer, every transition entering the logic layer must preserve:

- provenance
- identity
- lineage
- scope
- compatibility state
- validation state
- unresolved uncertainty

The architecture must never silently turn a lineage relationship, analogy, or prediction into a logical fact.

## Link strategy

This document intentionally provides stable named nodes for later link attachment.

Recommended link classes:

    [LINEAGE]
    [FAMILY]
    [ARCHITECTURE]
    [MODEL]
    [INTEGRATION]
    [EVIDENCE]
    [VALIDATION]
    [DESCENDANT]
    [LOGIC_HANDOFF]

The corresponding links should be added only when the referenced artifacts or source records are verified.

## Design principle

Vitruvius is the architectural bridge between the project's accumulated developmental memory and its rational-logic model layer.

Its essential role is not to create every model itself, but to preserve enough whole-system architectural knowledge that model selection can be made in the context of lineage, composition, compatibility, and validated history.

## Forensic research / Codex extraction boundary

The daily Vitruvius research process includes a bounded forensic extraction layer:

    DE ARCHITECTURA
          ↓
    SOURCE / EDITION DISCOVERY
          ↓
    BOOK + CHAPTER INVENTORY
          ↓
    UNITS → RELATIONS → COMPOSITIONS
          ↓
    COMPOSITIONS OF COMPOSITIONS
          ↓
    STRUCTURAL REPRESENTATION TESTS
    GRAPH / HYPERGRAPH / DAG / TREE / RELATION_MATRIX
          ↓
    VITRUVIUS LOGIC KERNEL CANDIDATES
          ↓
    PROVENANCE / VERIFICATION GATE

The candidate kernel uses modern labels for extracted structures:

    UNITS → RELATIONS → ORDER → ARRANGEMENT → MODULE
    → PROPORTION → SYMMETRY → COMPOSITION → TRANSFORMATION → VALIDATION

These labels are formalization primitives, not historical quotations. A source claim, a transparent derivation, a structural inference, and a WANGA implementation remain separate evidence classes.

The daily queue also isolates two forensic claims:

- chapter-count claim ("50 chapters")
- "32-core" claim

Neither claim may inherit support from WANGA-internal material or from structural resemblance. Negative findings and unresolved states remain first-class outputs.

Comparative work is partitioned into independent Vitruvius ↔ Maimonides and Vitruvius ↔ WANGA tracks. The comparative layer cannot upgrade historical provenance or verification status.

## Coverage invariant

A corpus-level conclusion requires book-level coverage across Books I–X or an explicit CORPUS_COVERAGE_GAP record. Concentrating on Books I, III, and VI is permitted as a research priority but not as evidence that the remaining books have been exhausted.
