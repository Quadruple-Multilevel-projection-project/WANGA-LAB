# Cross-Project Agent Sweep V1

**Status:** agent roles are defined; a daily bounded GitHub Actions workflow is proposed in this branch; cross-repository runtime coverage depends on a configured, approved read token. The connected daily WANGA work loop has separately been updated to scan all repositories visible through its connectors and an immediate run was requested.

## Inventory observed in the connected GitHub session

- 34 repositories appeared in the AmbassadorOv owner listing.
- 13 repositories appeared in the collaborator listing.
- 25 appeared in the organization-member listing.
- After de-duplicating repository full names, the connector returned **59 unique accessible repository records**. This count is a snapshot of connection scope, not a count of projects owned by the user and not proof that every repository was content-scanned.
- A bounded content check confirmed README retrieval from key project repositories: `AmbassadorOv/AmbassadorOv`, `AmbassadorOv/Nanomathematics`, `AmbassadorOv/TTTT-0.0.0.0.1`, `AmbassadorOv/multi-agent-orchestator`, `Quadruple-Multilevel-projection-project/WANGA-LAB`, `Quadruple-Multilevel-projection-project/ai-agent-terraform`, `Quadruple-Multilevel-projection-project/AI231.meta.io`, `Quadruple-Multilevel-projection-project/ARK-KERNEL-OVERSIGHT`, `Quadruple-Multilevel-projection-project/MNM`, `Quadruple-Multilevel-projection-project/think-thank-you-of-cyber-Department`, and `tribal-archery/-logicl-neural-order`. These repositories have different levels of relevance; README access is not full-repository analysis.

## Relevant project relationships found

- The TTTT / Artificial Philosopher repo already documents the flow `LOGOS → CONNECTIONS → FRACTALS → ABSTRACTION → MODELS → VERIFICATION → SYNCHRONIZATION`, including a team map for Nanomathematics, Logical-Neural Order, Cyber Department, branch management and multi-agent orchestration.
- `tribal-archery/-logicl-neural-order` describes an NTM/WANGA orchestration layer with 28 reasoning/orchestration modes, provenance, verification, audit, and a provider-neutral model adapter interface. Its README explicitly says the branch contains an orchestration skeleton and that learned routing, parallel execution, persistent audit storage and broader verification remain roadmap work.
- `AmbassadorOv/multi-agent-orchestator` contains a three-agent pattern: text classification, data retrieval and reasoning. Its README describes a dependency on model/API configuration; this does not prove those agents are currently deployed across the WANGA ecosystem.
- `Quadruple-Multilevel-projection-project/ai-agent-terraform` describes infrastructure deployment for AI chat/agent APIs across environments, and warns that its main branch is out of date; a future scan should inspect the latest branches before implementation proposals.
- WANGA-LAB remains the aggregation and evidence/provenance layer. The scanner does not edit other projects. Cross-project improvements are proposed through their own review branches and PRs.

## Agent roles and execution

The registry `agent_registry.json` defines bounded roles: repository inventory, README/material collector, conversation export collector, logic extractor/normalizer, fractal composer, mirror/contradiction reviewer, benchmark evaluator, wiki curator, Wix sync auditor, and report publisher.

These roles execute deterministic scans and tests in GitHub Actions; they are not eleven separately trained LLM instances. The existing `scripts/run_logic_agents.py` executes the Logic Wiki research roles, while the new repository scanner enumerates a bounded batch of public repositories.

## Access boundaries

- A GitHub Actions `GITHUB_TOKEN` is normally scoped to the workflow repository. For a cross-repository inventory, configure an approved secret named `CROSS_REPO_READ_TOKEN` with read access to the repositories intended to be scanned. No token is included in code.
- The workflow excludes private and unknown-visibility repository names, paths, and content from public artifacts. It reports only a redacted count for such repositories. Authorized private-project extraction remains in the connected WANGA work loop until a suitable private report destination is configured.
- ChatGPT does not expose a universal API for all of the user's private conversation history. The conversation collector only processes actual files/Library results or supplied ChatGPT export ZIP/JSON records. It must report missing history as `ACCESS_GAP`.
- The Files Library contains relevant documents and model archives, including the NTM V0.1 executable archive, the logical-memory contract, MLN field documentation, and a conversation-style PDF of prior project research. These need item-level provenance and semantic review; unrelated sensitive files must be excluded from the research corpus.
- The scanner does not publish to Wix, modify remote repositories, merge PRs, or create compute resources.

## Current compute path

The GitHub Actions runner provides bounded CPU time for metadata collection, parsing, tests and report generation. It is not a dedicated AI training cluster and the workflow does not train a neural model. Model/API backends and paid compute remain unconfigured.

## Continuation

1. On each scheduled workflow run, scan the next batch of public accessible repositories and upload a report artifact.
2. In the connected daily WANGA work loop, scan the full connector-visible repository scope in bounded batches, including approved collaborator repositories.
3. Register new source material and cross-repository links only with exact source references and status.
4. Ingest user-provided conversation exports to the private-review inbox; publish only reviewed derivatives.
5. Run Logic Fractal and NTM/MLN tests, update readiness metrics, and open review PRs for repository changes.
6. Publish approved source-backed additions to Wix through the authorized Wix connection and verify with deployment read-back.

The first logic-fractal model remains `NOT_READY_INTERNAL_CANDIDATE_ONLY` until source coverage, counterexamples, semantic benchmarks, holdout, MIRROR review and independent reviews meet the configured gate.
