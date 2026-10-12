# WANGA Symbolic Logic Kernel V1

**Status:** BUILT AS A BOUNDED SYMBOLIC PROTOTYPE · TESTED BY UNIT TESTS WHEN CI RUNS · NOT GENERAL AI · NOT YET VERIFIED AS A PRODUCTION SYSTEM

This folder implements the first executable logic layer connected directly to the WANGA-LAB corpus. At each CLI `demo` or `run`, it validates and loads the repository's letter, gate, directed-transition, triple and page-definition registries. It injects only structural facts whose predicates are explicitly requested by the supplied rules. The engine performs deterministic symbolic matching and forward-chaining; checks evidence-reference eligibility; traces derivations and corpus-file provenance; flags contradictory positive/negative claims; checks scoped actions and explicit publication permission; compares threshold-based decisions; and validates exact corpus invariants.

It is intentionally **not** an LLM, natural-language understanding system, theorem prover, or complete implementation of the proposed 5-forward/5-return architecture. This is a bounded logic kernel that a language model can later call, while the kernel independently enforces specified rules.

## Run it

Requires Python 3.11+ and uses only the Python standard library.

```bash
cd logic_engine_v1
python logic_kernel.py counts
python logic_kernel.py demo
python logic_kernel.py run examples/site_update_case.json
python logic_kernel.py validate-corpus --repo-root ..
python logic_kernel.py demo --no-corpus    # isolate the symbolic rule demo
python -m unittest discover -s tests -v
```

## Engine components

1. **Evidence gate:** input claims only become rule-eligible if their epistemic status is `OBSERVED` or `TEST_FIXTURE` and all referenced evidence IDs exist. That checks data structure, not source authenticity or truth.
2. **Symbolic rule engine:** explicit Horn-style rules use variables such as `$ACTION`; each successful firing has a trace, premise IDs and rule ID.
3. **Validated corpus loading:** `load_corpus_context()` reads the 1,000 page definitions, 22 letter nodes, 231 unordered gates, 462 directed transitions and 1,540 unordered triples. It labels loaded records `CORPUS_STRUCTURE_NOT_SEMANTIC`; edge existence never establishes a gate's meaning.
4. **Contradiction handling:** same subject/predicate/object with opposing polarity triggers `REVIEW`. Facts involved in contradictions are not used as premises.
5. **Scope/action gate:** denies actions outside declared action/target scope; missing permission denies; incomplete evidence routes to review; publication requires separate explicit permission.
6. **Drift arithmetic:** the same score can be evaluated under two thresholds. This is a transparent calculation, not model drift discovery.
7. **Corpus validator:** checks the GitHub registry counts, unique IDs, directed reverse links, triple uniqueness and exact combinatorial formulas.
8. **Source-scoped semantic regression cases:** [`semantic_test_matrix.json`](semantic_tests/semantic_test_matrix.json) scopes the Sefer Yetzirah case to a particular displayed edition and marks the 221/231 scholarly reference as requiring full-text review. The tests do not promote derived output to `VERIFIED`.

## Epistemic contract

- An input record `OBSERVED` or `TEST_FIXTURE` is eligible only after reference checks. The engine does not authenticate the source.
- A rule-derived conclusion is always `DERIVED_NOT_VERIFIED`.
- A contradicted signature blocks automatic use and sends the run to `REVIEW`.
- A missing reference, unsupported assertion, unknown role or disabled rule is not silently repaired.
- An `ALLOW_WITHIN_DECLARED_SCOPE` result is not execution. An external executor must still enforce permission and verify the resulting system state.
- No result from this package demonstrates that hallucinations are eliminated.

## Input model

A bundle contains `evidence`, `claims` and `rules`. Each atom is a structured triple of `subject`, `predicate`, `object`, with optional Boolean `polarity`. Evidence IDs must be unique. Rules specify one or more antecedent atoms and one consequent atom.

Variables in rule patterns use a leading dollar sign (e.g. `$ACTION`). Repeated variables must bind to the same value. The engine runs deterministic forward-chaining until a fixed point or a configured round limit.

See `examples/site_update_case.json` for a synthetic website-change authorization scenario.

## Connection to the 1,000-page corpus

The corpus remains an evidence/source and mapping layer, not automatic semantics for each letter:
- K22/231 and 462 counts are structural.
- 1,540 means unordered sets of three distinct letters; 9,240 means ordered triples without repetition.
- The 221/231 textual variation remains source/version-specific.
- Four original weight-layer formulas still need to be recovered from source.
- Lie algebra, E8, Tonnetz, 10-degree-of-freedom and fractal embeddings remain research hypotheses until mappings, invariants and tests are specified.

## Architecture mapping

```text
SOURCE / CORPUS
   ↓ source/version/claim registry
STRUCTURAL NORMALIZATION
   ↓ typed atoms + evidence IDs
SYMBOLIC LOGIC KERNEL
   ↓ deterministic rule firings + trace
CONTRADICTION / SCOPE / PERMISSION GATES
   ↓ structured decision (never direct execution)
VERIFICATION RECORD
   ↓ pass / fail / review / unresolved
MAP VERSION UPDATE (future integration; not yet wired)
```

The kernel is the deterministic layer, not the probabilistic natural-language interface. A future LLM adapter may propose atoms or candidate rules; it must not bypass the kernel's evidence, contradiction and permission gates.
