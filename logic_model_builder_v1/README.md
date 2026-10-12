# WANGA Logic-Native Language and Model Builder V1

**Status: BUILT AS AN EXPERIMENTAL LANGUAGE/COMPILER AND MODEL-PROPOSAL PIPELINE.** The deterministic provider and symbolic execution path are testable without a model endpoint. LLM-driven proposals require an explicitly configured OpenAI-compatible endpoint. Models compile to review status; they are not automatically verified or published.

## The idea: logic as an executable language

LNL does not try to turn every statement into free-form prose. In its core syntax, each statement is typed as a source, fact, rule, goal, or constraint. The compiler maps each expression into structured relations, executable rules, graph nodes/edges, provenance links, and testable goals.

This is a **logic-native representation language**, not a claim that ordinary human language is already fully formal logic or that every aspect of meaning can be reduced to the current grammar.

## Architecture

1. **Specification input** — a structured task, sources, candidate facts, goals, and constraints.
2. **Model proposer** — either an offline structured-spec baseline, or an optional configured language model which proposes LNL.
3. **LNL compiler** — parses statements and compiles facts/rules to the existing WANGA kernel bundle and an auditable model graph.
4. **Hard critic** — rejects missing source IDs, unsupported constraints, raw facts marked VERIFIED, and unbound rule variables.
5. **Feedback loop** — if compilation fails, diagnostics are sent to the proposer for a bounded retry (maximum 5).
6. **Symbolic execution** — the compiled artifact is passed to `logic_engine_v1`, optionally loading the checked WANGA corpus.
7. **Goal and provenance report** — returns reached/unreached goals, derivation trace, source file references, and explicit epistemic limits.

## Quick start

Requires Python 3.11+; no extra packages are needed for the template provider.

```bash
# Build and run the synthetic example through the structured baseline.
python -m logic_model_builder_v1.cli demo

# Compile the readable LNL file.
python -m logic_model_builder_v1.cli compile logic_model_builder_v1/examples/site_change.lnl --out /tmp/site-model.json

# Build from a structured JSON specification and execute it.
python -m logic_model_builder_v1.cli build logic_model_builder_v1/examples/site_change_spec.json --provider template --execute --out /tmp/model-build.json

# Use a configured language model to propose LNL candidates (makes an external model request).
export WANGA_MODEL_BASE_URL="http://localhost:11434/v1"
export WANGA_MODEL_NAME="your-local-model"
# Set WANGA_MODEL_API_KEY only when the selected endpoint requires one.
python -m logic_model_builder_v1.cli build logic_model_builder_v1/examples/site_change_spec.json --provider llm --execute --out /tmp/model-build-llm.json

# Run the unit tests.
python -m unittest discover -s logic_model_builder_v1/tests -v
```

The `llm` provider is never selected by default. No API credentials are stored in the repository. A model endpoint is called only when the user explicitly chooses `--provider llm`.

## LNL v0.1 example

```text
model site_change_logic version=0.1 description="Synthetic site-change model"
source E_REQUEST uri="fixture://site-change/request" status=TEST_FIXTURE
fact C_REQUEST request.action(typo_fix) status=TEST_FIXTURE evidence=E_REQUEST
rule R_SCOPE_PERMISSION source=E_POLICY:
  request.action($action) AND scope.allows($action) AND permission.grants($action) => action.candidate_allowed($action)
goal action.candidate_allowed(typo_fix)
constraint require_evidence
constraint no_unbound_rule_vars
constraint no_automatic_verified_status
constraint require_rule_sources_or_explicit_assumption
```

The source and fact statements form typed records. The rule uses a variable (`$action`) that must be bound by its premises. The goal is a query the resulting model attempts to derive.

## External models reviewed (design references only)

- **[Nucleoid](https://github.com/NucleoidAI/Nucleoid)** — a logic language with structured objects/relationships and declarative graph execution. Its README identifies Apache-2.0. WANGA borrows the high-level idea of declarative relationships, not its code or grammar.
- **[PEIRCE](https://github.com/neuro-symbolic-ai/peirce)** — a research framework where LLMs propose candidate explanations/models which can be refined with symbolic and soft critiques. We use the candidate–critique–refine pattern as a design reference; no PEIRCE source code is copied. A repository license was not found in the inspected top-level path, so re-use of its implementation has not been assumed.
- **[IBM Logical Neural Networks](https://github.com/IBM/LNN)** — a neuro-symbolic framework where components correspond to weighted logical formulae. Potential future research for learnable logic parameters; not a dependency in this prototype. README identifies Apache-2.0.
- **[PyNeuraLogic](https://github.com/LukasZahradnik/PyNeuraLogic)** — differentiable logic programs with learnable numeric parameters. Potential future experiment for learning weights; not a dependency in this prototype. The repository license is MIT.

## What this is — and is not

- Built: a small declarative language; parser/compiler; model graph; source/reference checks; variable-safety checks; a bounded candidate/critic/refine loop; an optional LLM provider interface; and integration with the WANGA symbolic kernel.
- Not built: a new foundation model trained from scratch, open-ended autonomous discovery of correct logical rules, arbitrary natural-language semantics, formal proof of all derived claims, live Wix/GitHub publishing by the model, or evidence that hallucinations have been eliminated.
- The current synthetic example is a fixture. A goal reached by the symbolic rules means that the declared program derives it; it is not an independent proof that its premises reflect real-world truth.

## Mathematical boundary

The kernel can use the WANGA dataset's 22 vertices, 231 unordered pairs, 462 directed transitions, and 1,540 unordered triples as structural data. Those counts do not themselves assign semantics to a letter pair. The documented 221/231 textual variant is retained, and the original four weight-layer formulas must be recovered from source before being used as executable semantics.

## Tests

The CI workflow runs Python compilation, corpus integrity checks, existing symbolic-kernel tests, model-builder tests, and the end-to-end synthetic demo.

## Live research page

Read the Hebrew project overview on [Wix](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-native-model-builder.html). Implementation PR #96 was merged after the Logic-Native Model Builder, Repository Integrity, and CodeQL checks passed. The LLM endpoint adapter remains opt-in and unconfigured by default.
