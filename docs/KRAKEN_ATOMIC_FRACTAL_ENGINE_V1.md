# KRAKEN Atomic Fractal Engine — Architecture Proposal v1.0

**Status:** PROPOSED ARCHITECTURE — not yet implemented or experimentally validated  
**Scope:** WANGA-LAB / Cabinet shared technical brief  
**Purpose:** Define the smallest reusable semantic-logical unit and show how repeated units compose into a crystal-like structure without losing their contracts.

## 1. Core proposition

The Kraken engine is to be designed from small, typed, independently testable atomic units. Each unit carries its own local definition, relations, boundary conditions, provenance, and validation result. Larger structures are composed by connecting these units through explicit, typed interfaces.

The intended efficiency mechanism is not “small is always faster.” It is **bounded local complexity + reuse + compositional verification**: a change should require rechecking the affected unit and its dependency neighborhood, while unaffected verified units can retain their prior evidence if their dependencies and contract hashes have not changed.

## 2. Three-sphere atomic unit

For the first engineering proposal, represent each atomic unit with three mutually constrained spheres:

1. **Core sphere — identity / invariant:** what the unit is; stable identifier, primitive, type, and invariant.
2. **Relation sphere — interfaces / dependencies:** what it connects to; typed inputs, outputs, relations, preconditions, and dependency references.
3. **Boundary sphere — admissible scope / stop conditions:** where it applies, upper and lower limits, exclusions, termination, and REVIEW / ABSTAIN / HALT behavior.

These are three views of one atomic unit, not three independent agents and not three claims of physical spheres. The exact domain semantics of the three spheres remain a design definition to be ratified by the project owner.

### Atomic contract (minimum record)

- atom_id and atom_version
- core_type and invariant
- typed_ports and relation_types
- scope_upper, scope_lower, exclusions
- preconditions and postconditions
- provenance (source, path, commit, span/hash)
- validation_state: CANDIDATE / TESTED / VERIFIED / REVIEW / ABSTAIN / HALT
- contract_hash and dependency_hashes
- change_impact_set

No atom is VERIFIED merely because it type-checks or because another model agrees with it.

## 3. Fractal composition

Atoms compose into cells; cells compose into lattices; lattices compose into Kraken structures and higher-level WANGA systems.

At each level:
- preserve child atom IDs and versions;
- expose only declared interfaces;
- validate parent constraints against child contracts;
- propagate a changed dependency to its transitive dependents;
- do not silently rewrite a child invariant;
- isolate incompatible branches as explicit conflicts;
- use deterministic ordering and content-addressed snapshots where practical.

A parent contract is valid only if its composition rules and all required child contracts pass the parent's declared checks. Parent validity does not automatically prove every possible semantic interpretation.

## 4. Crystal-like arrangement

“Crystal” is an architectural analogy for a repeatable, structured arrangement: stable local units, declared adjacency/relations, and repeatable composition rules. It is not a claim that the software is a physical crystal or that quantum/atomic behavior has been demonstrated.

A lattice record should specify:
- lattice_id and version;
- atom/cell membership;
- adjacency and relation graph;
- symmetry/repetition rules, if any;
- boundary conditions;
- permitted transformations;
- invariants that must survive transformations;
- validation coverage and unresolved gaps.

## 5. Relationship to the five-sphere semantic place model

Keep the levels distinct to avoid a terminology collision:
- The **three-sphere atom** is the proposed smallest executable/contract-bearing unit: Core, Relation, Boundary.
- The previously discussed **five-sphere semantic place model** is a higher-level semantic description of a word/concept and its enclosing context.

A five-sphere semantic concept may be represented by or mapped onto one or more three-sphere atoms, but the mapping must be explicit and tested. Do not collapse the two models or assume a one-to-one mapping without a specification.

## 6. Relationship to Kraken-36 and existing WANGA components

The project context describes Kraken-36 as 18 Inner Cyan + 18 Outer Mag, with 126 TensorCells. Treat these as project-specified design parameters pending implementation-level verification. This proposal does not infer that each TensorCell is already an atomic unit. A mapping document must define whether:
- a TensorCell contains one atom or several;
- the 36 Kraken elements are roles, processing nodes, or structural positions;
- atom-to-cell and cell-to-Kraken interfaces are typed and testable.

Candidate integration points identified in the WANGA-LAB architecture include:
- `logic_fractal/fragment_composer.py` — candidate composition;
- `formal_reasoning/typed_fragment.py` — typed checks;
- `ark_swarm/coordinator.py` — orchestration and benchmark coordination;
- `ark_swarm/swarm_state.py` — state records;
- `logic_engine_v1/logic_kernel.py` — symbolic logic kernel;
- `governance/kernel.py` — governance review.

These are integration candidates, not evidence that the atomic Kraken engine is already implemented.

## 7. Efficiency model — hypotheses, not promised gains

Expected benefits to test:
- local edits trigger narrower revalidation when dependency hashes prove the rest unchanged;
- reusable atoms reduce repeated specification and implementation work;
- typed interfaces reduce integration mismatches;
- provenance and explicit boundaries reduce semantic drift and debugging time;
- hierarchical composition makes larger systems manageable.

Potential costs:
- atom metadata and contract checks add overhead;
- excessively small atoms increase orchestration and interface traffic;
- dense dependency graphs can cause large revalidation cascades;
- poorly chosen boundaries can fragment a task and reduce end-to-end performance.

Therefore, the optimization target is not minimum atom size. It is the **optimal granularity** that minimizes total cost:
`C_total = C_build + C_coordination + C_validation + C_rework + C_runtime`.

The preferred atom size is the one that minimizes measured total cost while maintaining semantic accuracy and invariant preservation.

## 8. Required benchmark

Compare at least three granularities (coarse / medium / fine) on the same workload and hardware/model allocation. Keep the task set and quality threshold identical.

Measure:
- verified tasks per unit cost and time;
- token and tool-call overhead;
- composition success rate;
- contradiction and interface mismatch rate;
- change-impact size;
- number of components requiring revalidation after a local edit;
- regression rate and human correction count;
- semantic boundary violations;
- new task classes enabled by composition.

Use a control implementation without atomic decomposition and a treatment implementation with it. Report confidence intervals and sample sizes. Do not publish a percentage gain until measured.

## 9. Cabinet instructions for every model

Every participating model must:
1. Read this document and the unified cabinet diagram before proposing Kraken changes.
2. State its capability/tool declaration and assigned scope.
3. Treat Core / Relation / Boundary as the current proposed three-sphere schema, not as experimentally established fact.
4. Keep the three-sphere atom distinct from the five-sphere semantic-place model.
5. Extract only evidence from assigned repository paths; include path, commit/ref, and exact supporting span where available.
6. Label each statement SOURCE / IMPLEMENTED / PROPOSED / HYPOTHESIS / TESTED / VERIFIED.
7. Never invent Kraken mappings, physical claims, weights, timing, performance percentages, or completed implementation.
8. Report contradictions and missing definitions without silently resolving them.
9. Prefer bounded tasks: one atom, interface, test, or dependency neighborhood for limited-capability models; cross-layer integration and independent audit for stronger models.
10. Return results in the handoff format below.

### Model handoff format

`MODEL | CAPABILITY | ROUND | SCOPE | TOOLS`  
`FINDING_ID | STATUS | PATH@REF | ATOM/CELL | EVIDENCE | GAP/CONFLICT | NEXT_ACTION`

If no supported finding exists, state: `NO NEW EVIDENCE`.

## 10. Acceptance gates

Do not mark the Kraken atomic engine IMPLEMENTED until the repository contains:
- a versioned atom schema;
- deterministic serialization and contract hashing;
- atom validator and boundary tests;
- composition implementation;
- dependency/change-impact logic;
- lattice/cell mapping specification;
- negative tests for incompatible interfaces and semantic tails;
- benchmark results against a baseline.

**Current conclusion:** The atomic-fractal approach is a plausible architecture for improving long-horizon maintainability, reuse, and local verification. Whether it improves throughput depends on granularity, graph topology, overhead, and workload; this must be established experimentally.
