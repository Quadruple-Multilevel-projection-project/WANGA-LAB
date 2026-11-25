# WANGA Naming–Place–Distinction–Number Contract v1.0

**Status:** SPECIFIED — normative design contract; runtime enforcement NOT_YET_VERIFIED  
**Applies to:** Thinking Language, Thought Mapping, Logic Kernel, Fractal Composer, Kraken workload interfaces, model/agent adapters, measurement and evidence pipelines.

## 1. Governing rule

A numeric value MUST NOT be treated as self-grounding. Before a value is created, compared, aggregated, or used to make a decision, the system must establish:

1. **Identity / distinction:** what entity, event, property, or relation is being referred to?
2. **Name / type:** what stable identifier and qualitative type distinguish it?
3. **Place / context:** in what bounded context, observer position, substrate, and protocol is it defined?
4. **Unit / comparison basis:** what unit and equivalence rule make comparison legitimate?
5. **Persistence:** what criterion establishes that the referent remains the same across observations or state transitions?

The contract expresses the ordering as:

`DISTINGUISH → NAME/TYPE → DEFINE PLACE → DEFINE COMPARISON + UNIT → MEASURE/NUMBER`

This is a logical and epistemic dependency rule for WANGA representations. It does not assert that physical reality is created by human language, nor settle mathematical Platonism.

## 2. Naming is not an arbitrary label

A name is a typed, provenance-bearing identity handle. It must resolve to:
- entity or relation ID;
- qualitative kind / role;
- source and exact evidence span where available;
- Place/context definition;
- valid relations and scope;
- persistence rule;
- status: SOURCE, SPECIFIED, DERIVED, TESTED, VERIFIED, HYPOTHESIS or UNKNOWN.

Names such as Alpha, Beta, Aqua, Terra, Sol and Flora are examples of symbolic identifiers only. Their causal roles must be explicitly defined in a domain schema; labels alone do not establish causation.

## 3. Place tuple

A measurement context is represented by a versioned Place record. Initial schema:

- `place_id`
- `referent_id`
- `observer_or_base` (including observer position where relevant)
- `substrate_state`
- `protocol_id` (Π)
- `boundary_or_closure` (κ)
- `persistence_criterion` (ρ)
- `time_window`
- `unit_system`
- `comparison_class`
- `uncertainty_model`
- `source_refs`
- `verification_status`

A Place record may be incomplete. Missing required fields MUST produce UNKNOWN / ABSTAIN, not invented defaults. The tuple is a proposed WANGA schema and must be refined by domain and experiment.

## 4. Qualitative relations before scalar values

The representation layer must preserve typed relations before scalarization. Supported relation types may include:
- causes / enables / constrains / prevents;
- material / formal / efficient / final-cause roles;
- part-of / contains / overlaps / precedes;
- depends-on / transforms-into / measured-by;
- necessary-condition / sufficient-condition.

Every relation requires a domain, direction, scope, provenance and evidence status. Causal labels are not inferred from proximity or correlation alone.

## 5. Numeric derivation gate

A number may be emitted only if all required preconditions pass:
- referent identity is stable;
- Place is defined for the task;
- unit is explicit;
- comparison class is valid;
- protocol and substrate metadata are sufficient;
- persistence and uncertainty criteria are declared;
- source lineage is retained.

The output must carry a measurement receipt:
`{referent_id, place_id, protocol_id, unit, value, uncertainty, timestamp, source_refs, verification_status}`.

If two observations differ in Place, protocol, substrate, unit, or comparison class, they MUST NOT be compared as measurements of “the same thing” until a justified normalization or equivalence mapping is supplied.

## 6. Computation and optimization

The system must distinguish:
- **structural representation:** names, types, boundaries and relations;
- **numeric evaluation:** measurements or derived quantities;
- **execution cost:** actual operations, latency, memory and compute;
- **semantic compression:** reduced representation size without loss of required distinctions.

Do not assume that named relational representations are automatically cheaper. Complexity must be measured against an equivalent task, same acceptance criteria, and a declared baseline. A reduction in the number of represented paths is valid only if omitted paths are demonstrably irrelevant under the task contract.

## 7. Quantum and physical-science boundary

WANGA may use distinction, naming and Place as an interpretive and modeling framework for quantum experiments. It must not state as established physics that:
- measurement is literally naming;
- wavefunction collapse is literally a language transition;
- superposition is eliminated by semantic distinction;
- the uncertainty principle is dissolved by incomplete naming;
- dark matter or dark energy are measurement artifacts;
- the framework resolves the quantum measurement problem.

Those are hypotheses or philosophical interpretations unless derived mathematically, operationalized into testable predictions, and supported by reproducible experiments. Quantum state formalism and empirical predictions must not be discarded merely because an interpretation is contested.

## 8. Contract enforcement

The Thinking Language compiler and Logic Kernel must:
1. reject numeric fields with missing referent/unit/context when those are required;
2. preserve qualitative relation types during transformations;
3. detect invalid comparisons across incompatible Place records;
4. require evidence and uncertainty metadata for empirical claims;
5. distinguish source facts, formal derivations, hypotheses and interpretations;
6. return ABSTAIN or HALT when a required grounding field is absent or contradictory;
7. log the exact failed precondition.

LOCK is permitted only after schema validation, invariant checks and evidence checks pass.

## 9. Required tests

- Same referent, same Place, same protocol: repeatability test.
- Same referent, changed protocol: comparability must be flagged.
- Same label, different referent: identity collision must be rejected.
- Different qualitative causal types with equal scalar value: type distinction must remain.
- Missing unit or comparison class: numeric derivation must ABSTAIN.
- Missing persistence criterion: cross-time identity must remain UNKNOWN.
- Cross-observer results: preserve observer/base metadata and test justified equivalence.
- Quantum interpretation examples: separate empirical prediction from ontology; no unsupported claim of solving measurement.

## 10. Acceptance status

This contract is **SPECIFIED**. It is not evidence that the compiler or runtime already enforces it. Implementation requires schemas, compiler checks, tests, failure logs and independent review.
