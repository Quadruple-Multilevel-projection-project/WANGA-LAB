# Limbo Cartography Core

**Deployment status:** INITIAL PACKAGE · VERIFY THROUGH CI  
**Epistemic status:** SPECIFIED / IMPLEMENTATION CANDIDATE  
**Scope:** Record source-backed structural failure points, run explicit structural checks, and preserve logic-bundle candidates with provenance.

## Operating contract

Limbo Cartography Core is an operational, cumulative forensic map of system crash points. It preserves each incident as a separate record and connects it to source evidence, affected component, observed state, prior incidents, subsequent changes, and retest outcomes. It is not a research repository or a substitute for implementation.

It does not infer that a system is in terminal collapse merely because a record exists. It does not promote a candidate Keystone to a verified axiom through a placeholder test. The package keeps source material, observations, interpretations, hypotheses, implementations, tests and verification outcomes separate. Missing inputs produce explicit empty/no-input states rather than fabricated coordinates.

## Execution

From this directory, using Python 3.12 or later:

    python -m pip install pytest jsonschema
    python engine/deterministic_executor.py
    python engine/drift_validator.py
    python -m pytest -q tests
    python engine/seismic_detector.py
    python engine/history_link_validator.py
    python engine/axiomatic_stress_tester.py
    python engine/tuning_candidate_builder.py
    python engine/iterative_map_builder.py
    python engine/logic_bundle_builder.py
    python engine/drift_validator.py

The daily workflow for this package is activated at the parent repository's .github/workflows/daily-limbo-cartography-agent.yml, because GitHub Actions only discovers workflow files under the repository-root .github/workflows/ directory. The copy under this package documents the portable standalone layout.

## Input boundaries

- Add source-grounded candidate incident records only under cartography/inbox/limbo_points/.
- Add source-backed change and retest events only under cartography/inbox/history_events/.
- Add candidate Keystone test cases only under cartography/inbox/keystone_cases/.
- Add candidate logic bundles only under cartography/inbox/logic_bundles/.
- Never use generated output directories as input. This prevents output-to-input feedback loops.
- Raw private conversation exports must not be placed in this public repository.
- A passing schema or unit test is not proof of source truth or semantic validity.

## Iterative forensic map

The source of truth is the append-only `cartography/reality_matrix.json`. Each cycle rebuilds `cartography/iterative_crash_map.json` deterministically from the registered crash points, linked history events, and recorded configuration candidates. The graph includes explicit predecessor, affected-incident, change/retest, and configuration-to-incident links; a recorded link is not causal proof or semantic entailment.

The map keeps a rolling 20-year monitoring-horizon setting while retaining older history: no automatic pruning is permitted. Its state estimate reports the latest recorded crash point, follow-up/retest status, registered counts, and provenance. It does not label the whole system stable or collapsing when coverage is absent. Trend estimates remain unavailable until source-coverage metadata is recorded. An empty matrix produces `NO_REGISTERED_POINTS` and `INSUFFICIENT_EVIDENCE`, not a clean bill of health.

## Cumulative history and tuning

The reality matrix preserves each recorded incident as a separate entry. Later changes and retests are appended as history events linked to the affected incident IDs; prior incident records are not rewritten to make a later result appear cleaner. Each event must carry source URI, exact locator, source version/hash when available, language, permission scope, and an authorized public excerpt or summary.

The history validator checks incident and event references, parent-event chronology, and duplicate IDs. The tuning-candidate builder emits a bounded candidate only when a source-backed change event has a linked passing retest for the same component and incident. Such output remains CANDIDATE_REPLAY_REQUIRED; a passing software test is not a real-system replay or semantic verification.

An empty incident inbox returns NO_INPUTS. An incident map with no follow-up events returns NO_FOLLOW_UP_EVENTS. Neither state is reported as successful forensic coverage. No real crash record or tuning candidate is added without source evidence.

## Status vocabulary

- OBSERVED: a sourced event was recorded.
- STRUCTURALLY_TESTED: declared structural checks ran and their result was captured.
- VERIFIED: accepted only with explicit verification procedure and evidence refs.
- DRAFT_UNVERIFIED: a bundle was preserved without a verification claim.
- NO_INPUTS: no candidate records were available to inspect.
- FAILED: a declared validation failed.

The initial reality matrix is empty. No real-world collapse event, Keystone, or clean logic bundle is asserted by the scaffold itself.
