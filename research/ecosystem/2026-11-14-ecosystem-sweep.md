# WANGA Repository Ecosystem Sweep — 2026-11-14

## Snapshot

- Owner affiliation: 38 repositories
- Collaborator affiliation: 13 repositories
- Organization-member affiliation: 25 repositories
- De-duplicated accessible repositories: **63**
- Public: **58**; nonpublic/private: **5** (names and content redacted)
- Bounded content batch: **10 repositories scanned**; **48 public repositories remain**
- All ten scanned repositories exposed admin/push permission in this connector snapshot. No repository outside WANGA-LAB was modified.

## Scanned batch

| Repository | Default branch | README/docs result | Finding |
|---|---|---|---|
| `Quadruple-Multilevel-projection-project/WANGA-LAB` | `main` | README and current catalog read | 28 articles, 17 source records, 11 source types, 111 editorial links |
| `Quadruple-Multilevel-projection-project/ai-agent-terraform` | `main` | README read | AI infrastructure; README warns main is outdated |
| `Quadruple-Multilevel-projection-project/AI231.meta.io` | `main` | README and agent-network charter read | 2,000 roles is a target; 231 gates/15,625 topology are proposals |
| `Quadruple-Multilevel-projection-project/ARK-KERNEL-OVERSIGHT` | `main` | Minimal README | No substantive evidence located in this batch |
| `Quadruple-Multilevel-projection-project/-logicl-neural-order` | `master` | README and `De architecture` read | Experimental PyTorch implementation; 231 nodes, 42 gates, 120 epochs; no test evidence observed |
| `Quadruple-Multilevel-projection-project/MNM` | `master` | Minimal README | Low-signal; no substantive documentation located |
| `Quadruple-Multilevel-projection-project/Qualia` | `main` | README and economy proposal read | Strategic proposal; legal enforceability remains conditional |
| `AmbassadorOv/O-Ms` | `main` | Minimal README | No relevant evidence located |
| `Quadruple-Multilevel-projection-project/globalSpeed` | `master` | README read | Media-speed browser extension; unrelated to WANGA logic |
| `Quadruple-Multilevel-projection-project/glowing-octo-waddle` | `main` | README returned 404 | Access/content gap; no inference from repository name |

Exact paths, blob SHAs, update timestamps, permissions and next actions are stored in `repository_inventory.json` and `project_findings.json`.

## Cross-project observations

1. **AI infrastructure:** `ai-agent-terraform` may be relevant to deployment, but its README explicitly warns that the default branch is stale. Inspect current branches before any proposal.
2. **AI231 / QUALIA:** the charter is a proposal, not proof that 2,000 agents exist. The economic document is a governance proposal, not an executed legal structure.
3. **Logical-Neural Order:** the inspected code initializes trainable complex weights and declares 120 epochs. This is an architecture tension with WANGA's logic-before-weights rule; it is not yet a proven contradiction because scope and runtime are unknown.
4. **Unrelated projects:** `globalSpeed` and minimal repositories were recorded without forcing a WANGA integration.

## Limbo Forensic Cartography

PR #122 is open/draft. Its branch is 63 commits ahead and 34 behind current main. The cumulative map has 10 recorded incidents, 2 history events, 14 nodes and 19 edges. Nine incidents lack a passing retest; one has a passing retest; one unresolved recurrence cluster has seven occurrences. One tuning candidate exists but its replay is NOT_RUN. The latest execution record is 2026-11-07 and is EXECUTION_RECORD_ONLY.

The current inbox returned no new files: **NO_INPUTS_THIS_CYCLE**. This does not mean the cumulative map is empty or complete. The package workflow is nested under `limbo-cartography-core/.github/workflows`; the main repository root workflow directory has no `daily-limbo-cartography-agent.yml`. PR #122's checks are `action_required`, and the branch is stale. No tuning change or crash point was invented.

## Logic Fractal readiness

The last verified Logic Fractal Actions run is 42629315588 (2026-11-09). Wiki build, composer tests, typed-fragment tests, synthetic first-model builder, formal reasoning and benchmark intake checks passed. The final PR-proposal step failed because `research/reports/agent-evaluation/**` did not exist when `git add` ran. That path was removed on this cycle's branch.

The last readiness artifact reports 17 source records / 11 source classes, 28 provenance-linked logic units, 2 composition rules, 0 counterexamples, 0 semantic cases, 0 benchmark suites and 0 independent reviews. Holdout and MIRROR review are false. Critical contradictions are not independently measured. The synthetic candidate hash is `a16a83eae678b668aa02fc40f311aad34120dfcb7565e3e2ad69ead384b75904`; it remains CANDIDATE_NOT_RELEASED / NOT_YET_VERIFIED.

## Library and conversation boundary

Six Library items were inspected, including partial PDF page ranges and NTM/MLN verification material. No private file identifiers or raw content were copied into this public report. No complete ChatGPT export was found; global conversation history was not scanned.

## Wix

The connected Wix Headless deployment was updated and read back for three files: `logic-wiki-research-status.html`, `logic-wiki.html`, and `logic-wiki-fractal-research.html`. The homepage contains 28 entry cards. The remaining 26 site files were not re-read, so status is PUBLISHED_READ_BACK_PARTIAL, not a full-site audit. The sync manifest update is staged on this branch.

## Roles and status

- Repository inventory / README collector: **COMPLETED** for this 10-repository batch.
- Conversation export collector: **BLOCKED / NO_EXPORTS**.
- Logic extractor / normalizer: **IN_PROGRESS**; no new source-derived units promoted.
- Fractal composer: last CI build **TESTED** on synthetic fixtures; no new semantic composition added.
- Mirror reviewer: **REVIEW_REQUIRED**; no independent review.
- Benchmark evaluator: **BLOCKED** by zero reviewed semantic cases.
- Wiki curator / Wix publisher: **COMPLETED_PARTIAL** with three-page read-back.
- Limbo cartography: cumulative map inspected; new input **NO_INPUTS_THIS_CYCLE**; tuning replay **NOT_RUN**.

## Next

1. Verify CI for the pathspec-fix/report PR; do not merge automatically.
2. Reconcile PR #122 with current main and move the Limbo workflow to repository-root `.github/workflows` through a separate PR.
3. Replay the existing tuning candidate only after CI and evidence checks; preserve all ten incidents and their retest states.
4. Scan the next ten public repositories listed in `scan_cursor.json`.
5. Keep private Library material private; wait for an actual export before claiming conversation coverage.
6. Add source-grounded counterexamples, semantic benchmarks, holdout and independent MIRROR review before any Alpha release.
