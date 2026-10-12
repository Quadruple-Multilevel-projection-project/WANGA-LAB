# Repository README Sweep — 2026-10-12

**Status:** BOUNDED CONTENT COLLECTION · NOT A COMPLETE REPOSITORY AUDIT  
**Scan basis:** connector-visible repository inventory plus direct README fetch attempts  
**No code or data was written into other repositories.**

## Coverage counts

- Repository inventory returned **59 unique repository identifiers** across three access-list categories: owner (34 records), collaborator (13) and organization-member (25), before de-duplication. The lists overlap. This is an access snapshot, not a statement of ownership or visibility.
- README retrieval was attempted across multiple bounded batches. **35 distinct repository identifiers produced a usable README response after excluding known repeated/ambiguous content responses.**
- Additional repository identifiers returned 404, empty-repository responses, non-standard/unusable default refs, or repeated content that could not be trusted as specific to the requested identifier.
- The repository contents in these passes were not exhaustively cloned or scanned. The confirmed result is README-level material and a bounded set of relevant path lookups, not a full code-level audit.

## Main classes of material observed

1. **Logic/NTM/fractal architecture:** WANGA-LAB, its public research index, the TTTT/Artificial Philosopher coordination repository, and an NTM/WANGA architecture repository.
2. **Agent orchestration and deployment:** a three-agent retrieval/classification/reasoning example, plus an infrastructure-as-code repository whose README says its default branch is outdated.
3. **Knowledge / prompt / skill infrastructure:** a prompt catalog, an agent-skills CLI catalog, and a Copilot CLI README.
4. **Text and structured-data corpora:** MAM-parse and MAM-parsed describe source-linked structured text data. These are possible ingestion/normalization inputs, not evidence that logic has been extracted or semantically verified.
5. **General upstream forks or technical docs:** README fetches also found SDK, documentation, diagrams, ML-framework, browser-extension and other upstream material. They are not automatically considered relevant to the fractal logic model.

The named files above were read from repository responses during the scan; no statement is being made here that those repositories are owned by the user or that every item is a first-party project. The public report intentionally does not list unverified repository visibility or quote repository contents that might be private.

## Ambiguous connector responses and blocked refs

Several distinct repository identifiers returned identical README hashes and identical minimal contents. Examples included a repeated one-line “Nanomathematics” response across separate identifiers, and a repeated “World-Party-Federation-Branches-managers” response across separate identifiers. These are **CONNECTOR_RESPONSE_AMBIGUOUS** until a direct per-repository read can establish identity. They are not counted as independent content discoveries.

Some repository/ref requests returned 404, no commit for the declared default branch, or an explicit empty-repository response. Such results are recorded as BLOCKED_OR_MISSING; no fallback to a different branch was guessed.

## Conversation and Library source sweep

The connected Library listing contains relevant archival material, including:
- a saved NTM v0.1 executable-core ZIP;
- a logical-memory contract and loader;
- an MLN continuous-field research PDF;
- WANGA neural-graph and neurokernel package artifacts;
- primary text extracts for Rambam's Milot Higayon and Sefer HaTziruf;
- a larger architecture-review PDF containing some excerpts of past project discussions.

These are available archive leads, not a complete export of all ChatGPT conversations. No complete ChatGPT export was identified during this sweep. A private conversation cannot be claimed as scanned unless its file or surfaced conversation is actually available. The existing intake script accepts an explicitly supplied export and assigns PRIVATE_REVIEW_ONLY until review/redaction.

Credential-like or unrelated personal files are excluded from the logic research pipeline and were not opened or copied.

## Automation and CI state

- The daily WANGA Unified Work Loop was updated to use the connected repository scope in bounded batches and to continue with independent work when a source is blocked.
- An immediate run was requested through the automation connector, but this report does not claim that asynchronous execution has completed.
- PR #106 added the public-repository scout, role registry, access policy, tests and daily GitHub workflow. The PR was merged after the WANGA Ecosystem Agent Sweep, Repository Integrity and CodeQL checks passed.
- The GitHub Actions cross-repository workflow still requires an approved CROSS_REPO_READ_TOKEN secret to enumerate repositories outside its current repository. If missing, it reports a scope blocker and falls back to the current repository. It never emits private or unknown-visibility repository names, paths or content.
- Wix is updated separately through an authorized connection and deployment read-back; the GitHub workflow has no configured Wix writer.

## Decision

**Coverage improved; all-project content audit remains IN_PROGRESS.** The next cycles should prioritize new logic/NTM/fractal-relevant repositories and newly changed docs, inspect relevant code paths rather than only READMEs, and process actual conversation exports only after they are made available and reviewed.