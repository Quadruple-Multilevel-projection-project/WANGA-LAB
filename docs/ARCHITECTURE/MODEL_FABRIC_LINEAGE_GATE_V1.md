# Model Fabric — Lineage Gate V1

## Interface

The lineage gate sits between candidate discovery/binding and enablement.

```
Candidate
  |
  v
Normalize
  |
  v
Classify
  |
  v
Algorithmic Genealogy
  |
  +---- conflict ----> Rational Logic / NTM escalation
  |
  +---- insufficient evidence ----> HOLD
  |
  v
Verification
  |
  v
Enablement
```

## Deterministic policy

Policy inputs are versioned:

- policy version
- registry version
- evidence requirements
- compatibility rules
- conflict rules

No model output is used as the sole authority for its own promotion.

## Rule classes

### R1 — Structural validity

Reject malformed genealogy records.

### R2 — Parent integrity

Reject missing or unverifiable parent references.

### R3 — Transformation disclosure

Hold or escalate undocumented transformations.

### R4 — Evidence sufficiency

Do not promote a candidate solely because it has a plausible description or a model-generated self-report.

### R5 — Conflict preservation

Conflicts become first-class records.

### R6 — Drift evidence

Known behavioral drift increases review requirements; it does not by itself prove root cause.

### R7 — Human gate

Final promotion remains a separate verification/human-governance stage.

## Decision record

Every decision must contain:

- candidate ID
- policy version
- registry hash
- rule results
- conflicts
- evidence references
- decision
- timestamp
- evaluator version
- deterministic decision hash

## Integration with existing WANGA priorities

P0: integrity and governance

P1: Rational Logic / NTM / execution

P2: evidence / forensics

P3: operational intake

P4: research composition

The lineage gate is not a second global orchestrator. Global Work Manager remains the canonical work planner.

## Neural-network integration boundary

Neural models may be used for:

- candidate discovery
- semantic normalization
- evidence extraction
- hypothesis generation
- structural comparison

They may not silently bypass the deterministic gate.

A model-generated confidence value is evidence metadata, not an authorization primitive.

## Test targets

Minimum test fixtures:

1. clean single-parent lineage
2. clean multi-parent merge
3. missing parent
4. undocumented transformation
5. conflicting compatibility declarations
6. known drift evidence
7. insufficient evidence
8. integrity mismatch
9. deterministic replay of the same registry

Status: SPECIFIED.
