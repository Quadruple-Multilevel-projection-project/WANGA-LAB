# WANGA-X — Requirement-Driven, Reversible Computational Architecture

WANGA-X defines the computational architecture as a requirement-derived and time-addressable object.

The system does not begin with a fixed computational architecture and force changing requirements into it. The current computational requirements determine the architecture that should be constructed.

## Core loop

```text
REQUIREMENT
    ↓
REASON / SPECIFY COMPUTATION
    ↓
ARCHITECTURE BLUEPRINT
    ↓
FRAME-BY-FRAME MATERIALIZATION
    ↓
EXECUTION
    ↓
OBSERVE / VERIFY
    ↓
NEW OR CHANGED REQUIREMENT
    ↓
NEW BLUEPRINT
    ↓
REBUILD / RECOMPOSE / REPLACE
```

## Architecture as an editable construction timeline

A WANGA-X build is represented as an ordered sequence of recoverable construction states ("frames").

Each frame records the architectural state reached at that point. A frame can be inspected before construction continues.

Conceptually:

```text
F0 → F1 → F2 → F3 → F4 → ARCHITECTURE-A
          ↑
        PAUSE
          ↓
     INSPECT / VERIFY
          ↓
   ROLLBACK TO F2
          ↓
   CHANGE REQUIREMENT
          ↓
   NEW BLUEPRINT
          ↓
   F2' → F3' → F4' → ARCHITECTURE-B
```

The film analogy is intentional: the construction process is a sequence of editable computational states. Stopping at a frame permits inspection and, where required, a change of the construction trajectory rather than forcing completion of an obsolete architecture.

## Reversible construction primitives

The research architecture should expose explicit operations:

- **PAUSE** — stop materialization at a defined frame.
- **SNAPSHOT** — preserve the exact architectural state.
- **INSPECT** — evaluate the state and its evidence.
- **ROLLBACK** — restore a previous verified state.
- **EDIT** — modify the requirement, Blueprint, or selected architectural components.
- **RECOMPOSE** — assemble a revised architecture from reusable compatible parts.
- **REBUILD** — materialize the revised Blueprint.
- **VERIFY** — validate the new state before continuation or activation.
- **COMMIT** — designate a verified state as an executable architecture version.

## Why this is architectural, not an auxiliary layer

Reversibility is part of the construction model itself. The system does not merely execute a static architecture and keep external logs about it. The architecture-generation process has a state history that can be traversed, inspected, corrected, and continued.

The resulting abstraction is:

**Requirement → Architecture State Sequence → Executable Architecture**

rather than:

**Fixed Architecture → Workload → Adaptation**

## Relation to WANGA-LAB

WANGA-X is intended to become the architectural principle connecting:

- Rational Logic — determines and constrains computational requirements.
- Neural Thinking Machine — explores and reasons over candidate computational structures.
- Model Fabric — supplies models and computational resources.
- Evidence / Provenance — preserves construction and execution state.
- Drift Forensics — detects meaningful changes in behavior or requirements.
- Verification — validates architectural states and transitions.

WANGA-X is therefore not treated as an additional bolt-on layer. It changes the architectural assumption under which the other WANGA-LAB components operate.

## Research status

This document defines the architectural hypothesis and target mechanism.

It does not claim that the complete mechanism has already been implemented or experimentally validated.

The next technical milestone is a minimal virtual-processor prototype demonstrating:

1. requirement input;
2. Blueprint generation;
3. frame-based architecture materialization;
4. pause/snapshot;
5. rollback;
6. requirement change;
7. revised Blueprint;
8. replacement or recomposition;
9. independent verification of the resulting architecture.

Performance targets remain experimental until measured.

## Executable reversible Blueprint frames

The first prototype is available in [`wanga_x_v1/engine.py`](../wanga_x_v1/engine.py). Each run records F0 requirement capture, F1 normalized requirement, F2 required-computation derivation, F3 candidate ranking, F4 Blueprint generation and F5 structural verification. Each frame is linked to its parent's hash; rollback adds a new branch frame referencing an older state and does not edit the prior history.

Current boundary: rollback is demonstrated over Blueprint metadata/state references. It does not rollback or snapshot actual neural weights or a deployed machine, because neural runtime materialization is not implemented.
