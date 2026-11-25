# Algorithmic Genealogy V1

## Purpose

Algorithmic Genealogy is the repository-level representation of model/component ancestry before a candidate model, weight set, adapter, merge, distillation artifact, or fine-tuned derivative is promoted into the WANGA Model Fabric.

The implementation treats genealogy as an auditable provenance graph, not as a claim that all model behavior is deterministic.

## Canonical position

```
WANGA OS
  -> Global Work Manager
  -> Model Fabric
  -> Algorithmic Genealogy Gate
  -> Digital Model Agent
  -> Provider / Runtime
  -> Evidence & Provenance
  -> Drift Forensics
  -> Verification
  -> Human Gate
```

The gate is a **pre-integration control point**. It does not replace verification after execution.

## Core hypothesis

When model artifacts are composed from multiple ancestors, provenance and compatibility should be evaluated before automatic promotion. Conflicting ancestry, incompatible objectives, unexplained weight transformations, or insufficient evidence should block automatic promotion.

This is an engineering hypothesis to be tested by the repository, not an established theorem that drift is inevitable.

## Genealogy record

Each node records:

- stable artifact ID
- artifact kind
- parent artifacts
- transformation type
- weight/update provenance
- training/fine-tuning metadata when available
- validation evidence
- drift exposure
- compatibility declarations
- evidence status
- integrity hash

## Transformation vocabulary

- FROM_SCRATCH
- FINE_TUNE
- DISTILLATION
- DEPTH_UPSCALING
- MODEL_MERGE
- ADAPTER_COMPOSITION
- QUANTIZATION
- PRUNING
- CHECKPOINT_CONVERSION
- UNKNOWN_TRANSFORMATION

UNKNOWN_TRANSFORMATION is never treated as safe by default.

## Deterministic gate

The gate evaluates a fixed rule set:

1. schema validity
2. provenance completeness
3. parent existence
4. transformation compatibility
5. evidence sufficiency
6. integrity consistency
7. declared drift exposure
8. unresolved conflict count

The same input registry and policy version must produce the same decision.

Possible decisions:

- ACCEPT_FOR_EVALUATION
- HOLD_FOR_EVIDENCE
- ESCALATE_TO_RATIONAL_LOGIC
- BLOCK_PROMOTION

The gate must never manufacture missing provenance.

## Conflict handling

A conflict is an observed incompatibility between declared ancestry, transformations, metadata, integrity records, or evaluation evidence.

Conflicts are preserved as evidence.

They are not silently averaged away.

Unresolved conflicts route to Rational Logic / NTM escalation according to the existing WANGA work-manager contracts.

## Weight lineage

The registry records lineage metadata for weights; it does not require storing model weights in the genealogy database.

A weight lineage edge must identify:

```
parent checkpoint
    -> transformation
    -> child checkpoint
```

If a transformation is undocumented, the edge remains UNKNOWN_TRANSFORMATION.

## Evidence boundary

The following are distinct:

- provenance claim
- behavioral observation
- drift finding
- causal attribution
- verification result

A genealogy graph alone cannot establish causal attribution.

## Mathematical integrity note

The historical statement `C(22,2)+22=231` must not be encoded as a mathematical identity. The correct value is:

```
C(22,2) = 231
```

If a separate 22-node augmentation is required by an architecture variant, it must be modeled as a separate construction.

## Status

SPECIFIED -> PROTOTYPED

This document defines the architecture contract. Implementation and tests determine later status transitions.
