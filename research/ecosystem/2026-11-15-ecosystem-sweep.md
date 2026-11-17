# WANGA Ecosystem Sweep — 2026-11-15

## Snapshot

- Accessible repositories: **63** (58 public, 5 nonpublic/private names redacted)
- Bounded batch: **10 public repositories scanned**
- Remaining public repositories: **38**
- No repository outside WANGA-LAB was modified.
- No private Library content or conversation text was published.

## Scanned repositories

| Repository | Default branch | README blob | Finding |
|---|---|---|---|
| `AmbassadorOv/Nanomathematics` | `master` | `e0fa7f84c366` | SOURCE_LOCATED_LOW_SIGNAL |
| `AmbassadorOv/multi-agent-orchestator` | `main` | `f41d34bb0019` | IMPLEMENTATION_DESCRIPTION_IN_README_NOT_RUNTIME_VERIFIED |
| `AmbassadorOv/ROBOTICS_TRIPARTITA_Logos` | `master` | `e0fa7f84c366` | DUPLICATE_README_BLOB_LOW_SIGNAL |
| `Quadruple-Multilevel-projection-project/skills` | `main` | `2246383e993f` | TOOLING_CANDIDATE_NOT_INTEGRATED |
| `tribal-archery/-logicl-neural-order` | `master` | `0ffc15fb869f` | ARCHITECTURE_CLAIMS_IN_README_NOT_RUNTIME_VERIFIED |
| `tribal-archery/MAM-parsed` | `main` | `fd3cb6f1ff1e` | DATASET_DESCRIPTION_SOURCE_AND_FORMAT_UNVERIFIED |
| `tribal-archery/Qdprojects` | `master` | `e0fa7f84c366` | DUPLICATE_README_BLOB_LOW_SIGNAL |
| `AmbassadorOv/python-genai` | `main` | `c5ba72e6d6b2` | EXTERNAL_PROVIDER_SDK_DOCUMENTATION_NOT_INTEGRATED |
| `AmbassadorOv/openai_tiktoken` | `main` | `ad8d88b13f73` | TOOLING_DOCUMENTATION_NOT_LOGIC_EVIDENCE |
| `AmbassadorOv/platform-samples` | `master` | `a2bb146a181b` | DIRECT_TEXTUAL_EVIDENCE_UNRELATED |

## Cross-repository observations

1. `tribal-archery/-logicl-neural-order` documents a provider-neutral NTM architecture, 28 reasoning modes and evidence/provenance controls. These remain README claims until code and tests are inspected.
2. `AmbassadorOv/multi-agent-orchestator` documents a generic three-agent classifier/retriever/reasoner pipeline. No WANGA integration or source-grounded semantic benchmark is established.
3. `tribal-archery/MAM-parsed` documents parsed Miqra/Masorah data and explicitly unstable JSON formats. No ingestion or reuse was performed.
4. Three repositories share the exact README blob SHA `e0fa7f84c36601e9895a7306f5b18dbaf7d09107`. This is duplicate README content, not repository identity.
5. Provider SDK, tokenizer and skills CLI repositories were recorded as tooling candidates only; no credentials were accessed and no adapters were configured.

## WANGA regional observation pipeline

Main commit [2412734756acd4cb22233fd1cfc4c116f69fdabe](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/commit/2412734756acd4cb22233fd1cfc4c116f69fdabe) adds eight regional JSON files containing 48 probe records. All records show `NOT_CONFIGURED`, an empty model field and no output hash or HTTP status. They are not model outputs and do not count as semantic benchmarks.

The current main-branch publisher used a direct `git push` from a scheduled workflow. This violates the repository's branch→PR→CI rule. PR [#146](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/pull/146) replaces that step with a review PR. It is open, based directly on current main, and Repository Integrity plus CodeQL passed. It removes the schedule, requires an explicit opt-in for external calls and does not write to main. No merge was performed.

## Logic Fractal readiness

- 17 source records / 11 source classes
- 28 provenance-linked logic units
- 2 active composition rules/contracts
- 0 source-grounded counterexamples
- 0 semantic test cases / 0 benchmark suites
- 0 independent reviews
- Holdout and MIRROR review: absent
- Core contradiction inventory: `NOT_MEASURED_NO_INVENTORY`

Typed candidate hash: `a16a83eae678b668aa02fc40f311aad34120dfcb7565e3e2ad69ead384b75904` — synthetic fixtures only, `NOT_YET_VERIFIED`.

## Limbo

PR #122 remains open/draft with `ACTION_REQUIRED` checks and tuning replay `NOT_RUN`. PR #138 has passing checks on its recorded head but is 29 commits behind current main. No new crash inputs were supplied; `NO_INPUTS` is not forensic coverage.

## Wix and Library boundary

Wix site context resolves as published, but live file read-back was not completed in this cycle. No catalog change was approved, so no Wix write was attempted. Three private Library files were read for analysis; two candidate structures remain private-review-only and were not copied into the public registry.

## Next

1. Verify PR #146 CI and keep publication review-gated.
2. Continue with the next ten repositories in `scan_cursor.json`.
3. Inspect NTM code/tests before integration.
4. Reconcile Limbo branches against current main and replay only with evidence.
5. Add reviewed source-grounded counterexamples, semantic cases, holdout and independent MIRROR review before any Alpha release.
