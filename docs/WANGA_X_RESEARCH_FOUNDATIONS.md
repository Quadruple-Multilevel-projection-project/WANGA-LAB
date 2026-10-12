# WANGA-X — Research Foundations for Evolving Dynamic Architecture

Status: RESEARCH FOUNDATION / DESIGN

## Purpose

WANGA-X uses established research directions as technical starting points and connects them through a requirement-driven neural-computation loop.

The central thesis is:

```
USER QUERY / SYSTEM REQUEST
            ↓
      REQUIREMENT
            ↓
REQUIRED NEURAL COMPUTATION
            ↓
NEURAL COMPUTATIONAL STRUCTURE
            ↓
         BLUEPRINT
            ↓
     NEURAL COMPUTER
            ↓
        EXECUTION
```

The important intermediate object is **required neural computation**. The research question is not merely which existing neural architecture best fits a task, but what neural computation is required by the query, and how that computation determines the Blueprint from which the neural computer is materialized.

## Research foundation A — High-Level Synthesis

HLS demonstrates a direct path from high-level algorithmic descriptions to generated hardware designs.

Google XLS provides a high-level hardware synthesis toolchain, a central IR, simulation/execution paths, and generation of synthesizable Verilog/SystemVerilog.

WANGA-X extraction:

`COMPUTATION DESCRIPTION → IR → GENERATED ARCHITECTURE → EXECUTION / VERIFICATION`

## Research foundation B — SODA

SODA demonstrates automated generation of specialized accelerators from high-level programming frameworks and supports design-space exploration.

WANGA-X extraction:

`HIGH-LEVEL COMPUTATION → SPECIALIZED ARCHITECTURE → DESIGN-SPACE EXPLORATION → GENERATED IMPLEMENTATION`

## Research foundation C — Requirement-to-Architecture synthesis

Architecture research investigates mapping requirements to architectural decisions and candidate architectures.

WANGA-X extraction:

`REQUIREMENT → REQUIRED COMPUTATION → ARCHITECTURAL CONSTRAINTS / CHOICES → BLUEPRINT CANDIDATE`

## Research foundation D — Dynamic Neural Networks

Dynamic Neural Network research establishes mechanisms in which neural-network structure or parameters can change rather than remaining completely fixed.

WANGA-X uses this as a foundation but changes the starting point:

`EXISTING NEURAL SYSTEM → ADAPT STRUCTURE / PARAMETERS`

versus the WANGA-X research hypothesis:

`USER QUERY → REQUIRED NEURAL COMPUTATION → BLUEPRINT → NEURAL SYSTEM`

The evolving system may change topology, modules, connections, routing, parameters/weights, resource allocation, and state representation as required by the derived computation.

## Research foundation E — Neural Architecture Search

NAS demonstrates automated generation/search of neural architectures.

WANGA-X extraction:

`REQUIRED NEURAL COMPUTATION → ARCHITECTURE SEARCH / REASONING → BLUEPRINT CANDIDATE`

The open research question is whether the required computation can become the primary determinant of the Blueprint rather than merely selecting a model from a predefined architecture search space.

## Research foundation F — HyperNetworks and generated parameters

HyperNetworks demonstrate that one neural network can generate parameters/weights for another network.

WANGA-X relevance:

`REQUIRED COMPUTATION → PARAMETER GENERATION]

This supports treating weights/parameters as potentially generated objects rather than permanently fixed artifacts.

## Research foundation G — Network Morphism and structural transformation

Network Morphism and related structural-transformation research demonstrate transformations between neural architectures while preserving or reusing learned behavior.

WANGA-X relevance:

`NEURAL SYSTEM_A → STRUCTURAL TRANSFORMATION → NEURAL SYSTEM_B]

This provides a foundation for controlled evolution of an existing computational structure.

## Research foundation H — Conditional computation

Conditional computation and related routing methods allow different parts of a neural system to be activated according to the required computation.

WANGA-X relevance:

`INPUT / REQUIREMENT → COMPUTATIONAL PATH SELECTION]

WANGA-X extends the question from selecting paths inside an existing network toward determining what computational structure should exist when the requirement itself changes.

## Research foundation I — Hardware-aware neural architecture

Hardware-aware NAS and neural/hardware co-design connect neural architecture choices with hardware constraints.

WANGA-X relevance:

`NEURAL COMPUTATION → NEURAL STRUCTURE ↔ COMPUTATIONAL RESOURCES]

This is a bridge between neural-system generation and computational-architecture generation.

## Research foundation J — Runtime / adaptive architecture

Runtime and adaptive architecture research provides mechanisms for changing system structure when conditions change.

WANGA-X extraction:

`CHANGED REQUIREMENT → NEW COMPUTATIONAL SPECIFICATION → NEW BLUEPRINT → NEW ARCHITECTURE`

## Unified WANGA-X layer

The research foundations are connected through one causal chain:

```
USER QUERY / SYSTEM REQUEST
             ↓
        RATIONAL LOGIC
             ↓
          REQUIREMENT
             ↓
REQUIRED NEURAL COMPUTATION
             ↓
    NTM ARCHITECTURE REASONING
             ↓
         BLUEPRINT / IR
             ↓
        MATERIALIZATION
             ↓
       NEURAL COMPUTER
             ↓
          EXECUTION
             ↓
     EVIDENCE / VERIFICATION
             ↓
     CHANGED REQUIREMENT
             ↓
 NEW REQUIRED NEURAL COMPUTATION
             ↓
       NEW BLUEPRINT
             ↓
RECOMPOSE / REBUILD / REPLACE
```

## Core research proposition

The proposed architectural paradigm is:

> **The user's query determines the required neural computation; the required neural computation determines the Blueprint; and the Blueprint determines the neural computer that performs the computation.**

This is the central WANGA-X architectural thesis.

## Architecture-state model

Each generated neural system is treated as a versioned computational state:

`N0 → N1 → N2 → ... → Nn`

where each state may contain:

`Architecture + Topology + Modules + Connections + Routing + Weights/Parameters + Resources + State`

A changed requirement can produce:

`Nk → Requirement' → Neural Computation' → Blueprint' → Nk+1`

## First prototype

The first prototype should remain virtual/software-defined.

Minimum experiment:

1. define multiple materially different user/system queries;
2. derive explicit requirements;
3. derive the required neural computation for each requirement;
4. generate corresponding computational structures;
5. generate a Blueprint for each structure;
6. materialize each Blueprint as an executable neural-computational graph;
7. execute controlled test inputs;
8. measure correctness and computational cost;
9. change the query/requirement;
10. derive the new neural computation;
11. generate a new Blueprint;
12. recompose, rebuild, or replace the neural system;
13. independently verify the resulting state.

## Research boundary

Existing research establishes important individual capabilities. This document records the proposed integration and causal ordering as the WANGA-X research hypothesis.

The repository must distinguish:

- **Existing foundation** — published or implemented technologies;
- **WANGA-X paradigm** — the proposed requirement → neural computation → Blueprint relationship;
- **Prototype** — implemented experimental mechanism;
- **Verification** — experimentally demonstrated behavior.

No claim of novelty, priority, or complete implementation is made until the corresponding evidence exists.

## Executable WANGA-X prototype

An experimental implementation is now merged into the repository: [WANGA-X Blueprint Engine V1](./WANGA_X_EXECUTABLE_BLUEPRINT_ENGINE_V1.md) and [package README](../wanga_x_v1/README.md). It implements requirement normalization, required-computation capability mapping, three candidate architecture strategies, dependency closure, Blueprint generation, structural verification and reversible hashed construction frames.

This implements the initial Blueprint-generation milestone, not the whole WANGA-X thesis. Neural weights are not synthesized or trained, and no live provider endpoint is created. If a requirement requires neural runtime materialization without a verified backend, the result remains blocked. Experimental success on structural tests is not empirical proof that requirement-derived architectures outperform a fixed baseline.
