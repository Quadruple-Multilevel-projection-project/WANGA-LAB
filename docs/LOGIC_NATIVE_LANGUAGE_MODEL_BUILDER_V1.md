# Logic-Native Language and Model Builder V1

**Date:** 2026-10-12  
**Status:** IMPLEMENTED AS AN EXPERIMENTAL PROTOTYPE; semantic correctness is NOT_YET_VERIFIED.

## Research question

Can WANGA express model structure as logic-native statements, instead of using text as the main object of computation, and can a model proposer construct those statements under deterministic critique?

The prototype formalizes the question as a bounded pipeline:
`task specification → proposed LNL → parser/compiler → structural critic → retry → symbolic execution → goal/provenance report`.

## GitHub systems inspected

| Project | Observed approach | Relevance to WANGA | Decision |
|---|---|---|---|
| [Nucleoid](https://github.com/NucleoidAI/Nucleoid) | Declarative logic language over structured objects and relationships; live graph reasoning | Strong reference for logic-native syntax and relationships | Use as a design reference only; do not copy its grammar or implementation |
| [PEIRCE](https://github.com/neuro-symbolic-ai/peirce) | LLM candidate generation followed by hard symbolic and softer critiques | Strong reference for a model-builder that proposes, tests, and revises formal candidates | Adopt the general candidate–critique–refine pattern; no source code copied; full repository license not found at inspected top-level path |
| [IBM Logical Neural Networks](https://github.com/IBM/LNN) | Neural components have interpretable weighted logical-formula meanings; inference and learning address logical constraints | Possible later path for learnable logic weights | Not a V1 dependency; the LNN README identifies Apache-2.0 |
| [PyNeuraLogic](https://github.com/LukasZahradnik/PyNeuraLogic) | Declarative logic programs with differentiable reasoning and learnable numeric parameters | Possible research path for learned weights after the semantics are formalized | Not a V1 dependency; repository license is MIT |

These are related systems, not proof that they implement WANGA's proposed 231-gate semantics. No third-party source code was copied into this implementation.

## What was implemented

- `logic_model_builder_v1/logic_native_language.py`: LNL/0.1 syntax, parsing, compiler, diagnostic reporting, model graph, source registry, and executable bundle.
- `logic_model_builder_v1/providers.py`: deterministic structured-spec provider and optional OpenAI-compatible model proposer.
- `logic_model_builder_v1/builder.py`: bounded candidate → compile/critic → retry pipeline and execution through the WANGA symbolic kernel.
- `logic_model_builder_v1/cli.py`: `compile`, `build`, `run`, and `demo` commands.
- `logic_model_builder_v1/examples/`: synthetic example in readable LNL and structured JSON.
- `logic_model_builder_v1/tests/`: regression tests for compile status, provenance, unbound variables, evidence gates, model retry, and execution goals.

## Semantics of LNL/0.1

- `model` declares model ID/version.
- `source` declares an evidence record and locator.
- `fact` declares a typed atomic relation plus status and evidence IDs.
- `rule` declares premises and a consequence; variables must be bound in the premises.
- `goal` declares a target relation to test after execution.
- `constraint` declares a supported compile-time constraint.

The grammar is intentionally small and typed. It is not a claim that arbitrary prose has a unique logical meaning. An LLM proposal remains a candidate until compiled and reviewed.

## Model proposer and critic

The default provider is deterministic and offline. It turns an already structured specification into LNL and is a baseline, not an AI model. Selecting `--provider llm` explicitly activates the OpenAI-compatible adapter when `WANGA_MODEL_BASE_URL` and `WANGA_MODEL_NAME` are configured. It proposes syntax only; the external deterministic compiler validates the output. Optional retry attempts receive the previous compiler critique. API credentials are not committed.

## Evidence and execution contract

- Raw facts cannot declare `VERIFIED` status.
- Facts must refer to declared source IDs where the evidence constraint is enabled.
- Rules must cite a declared source or be explicitly marked as a modelling assumption when the corresponding constraint is enabled.
- Consequent variables must be bound in rule premises.
- Compiled artifacts are `COMPILED_FOR_REVIEW`; model building yields `MODEL_BUILT_READY_FOR_REVIEW`.
- Runtime-derived claims keep `DERIVED_NOT_VERIFIED`.
- Reaching a goal shows that the bounded engine derived the requested atom under the supplied rules. It does not authenticate the premises or establish unrestricted real-world truth.

## WANGA relation

The model builder loads the corpus through the existing `logic_engine_v1` integration. Registry facts remain structural. The pair count, reverse-transition mapping and triple enumeration do not generate a semantic operator for a gate.

## Next research gates

1. Review each source-bearing LNL claim against exact text spans and editions.
2. Recover the original four mathematical-logical weight-layer definitions rather than inferring them from the 5+5 process stages.
3. Add a source-reviewed benchmark with positive, negative, boundary, ambiguous and contradictory cases.
4. Compare LNL candidate output from multiple configured models against the same deterministic compiler and benchmark.
5. Only after that, prototype learnable weights (for example, compare LNN/PyNeuraLogic as independent backends).
6. Add any external publishing executor as a separate approved action layer; model generation must not publish its own unreviewed results.

## Publication and CI state

- Live Wix documentation: [Logic-native language and model builder](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-native-model-builder.html).
- Implementation: [PR #96](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/pull/96), merged in commit `cbe964a245cbc5e0622a92ac2d79da7c3b750126`.
- The review checks passed: Logic-Native Model Builder V1, Repository Integrity and CodeQL Advanced.
- The LLM provider is a pluggable adapter only. No real model was called during CI, and no model endpoint or credential is configured in the repository.
