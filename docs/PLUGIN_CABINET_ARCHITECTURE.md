# AI231 Plug-in Cabinet — Multi-Model Coordination Architecture

**Status:** Proposed integration specification  
**Repository:** WANGA-LAB  
**Date:** 2026-11-25  
**Authority:** This document specifies a proposed coordination layer. It does not claim that external model providers are already connected or that the proposed cabinet plugin is implemented.

## 1. Purpose

Establish WANGA-LAB as the canonical project and evidence repository, and define a modular cabinet through which independent AI models and tools can receive bounded tasks, submit source-grounded reports, and coordinate through auditable records.

The cabinet is a software coordination layer. It does not merge model weights, create a shared consciousness, or imply direct model-to-model communication without explicit API or workflow connections.

## 2. Existing repository foundations observed

The following components were present in the inspected repository at the time of this document:

- `wanga_runtime/core.py`: provider-neutral deterministic local runtime; task roles, state transitions, result digests, and evidence records.
- `ark_swarm/coordinator.py`: bounded coordinator connecting ARK-Swarm roles to the WANGA logic pipeline; builds candidate packages and runs checks.
- `ark_swarm/swarm_state.py`: swarm state/event support (referenced by the coordinator).
- `logic_engine_v1/logic_kernel.py`: symbolic logic kernel.
- `logic_fractal/fragment_composer.py`: fractal composition.
- `formal_reasoning/typed_fragment.py` and `formal_reasoning/formalization_queue.py`: typed formal checks and formalization queue.
- `governance/kernel.py`: governance objects, explicit statuses, source references, links, verification references, and audit digest.
- `src/crypto/sha256_chain.py`, `src/core/audit_generator.py`, and `imperial-audit-core/src/verification/independent_verifier.py`: evidence/integrity/verification components identified in the repository architecture map.

These are repository observations, not proof that all components are deployed together or production-ready. Verify each path and its tests before integration.

## 3. Proposed cabinet modules

1. **Cabinet Control Layer** — model registry, capability declaration, task allocation, permissions, run IDs, and version tracking.
2. **Logic Core** — evaluates explicit rules, constraints, and typed relations.
3. **Analysis Core** — decomposes tasks, extracts evidence, compares reports, and identifies conflicts.
4. **Shared Relation Network** — stores explicit, typed links between tasks, findings, sources, models, and decisions. Optional 231 alphabetic-combination integration remains a separately specified research track; diagrams are not implementation evidence.
5. **Verification & Governance** — checks source traceability, status transitions, hashes, and unresolved conflicts; supports REVIEW / ABSTAIN / HALT.
6. **GitHub Cabinet Records** — versioned task assignments, model reports, evidence references, conflict records, decisions, and daily diagrams.

## 4. Coordination lifecycle

1. Model reads `START-HERE.md` and `CURRENT-STATE.md`.
2. Model declares available tools, permissions, context limits if known, and operational constraints.
3. Coordinator assigns one bounded task with repository scope and output contract.
4. Model performs work and records exact source paths and evidence.
5. Report is submitted under the model's own identifier; no report is silently overwritten.
6. Verification checks evidence and records disagreements as conflicts.
7. Accepted updates are reflected in the current state and daily diagram.
8. Next model reads the updated shared state before starting.

A repository commit is the synchronization event. Merely publishing a repository does not cause an external model to read it.

## 5. Model capability tiers

Assign work dynamically from declared and demonstrated capability, not provider brand:

- **Focused task tier:** one repository or one bounded path; README/tree/search and concise evidence rows.
- **Standard analysis tier:** a small repository group; map contracts, dependencies, gaps, and conflicts.
- **Deep analysis tier:** cross-repository comparison, provenance review, independent verification, and architecture synthesis.
- **Tool-specialist tier:** browser, GitHub, diagram, database, or automation operations within granted permissions.

A model may request a smaller task or abstain when access, context, or tools are insufficient.

## 6. Required model report

Each report must include:

- model/provider identifier and timestamp;
- assigned round and task ID;
- tools actually available and used;
- repositories and exact paths inspected;
- findings with source citations/links;
- status: VERIFIED / ASSESSMENT / HYPOTHESIS / NOT_YET_VERIFIED;
- conflicts and unresolved questions;
- files changed and commit/PR link, if any;
- next recommended task.

## 7. Safety and governance constraints

- No credentials, API keys, tokens, or secrets in repository files, issues, or reports.
- Least-privilege access; prefer pull requests for substantive changes.
- Do not overwrite another model's report.
- Preserve contradictions as explicit conflict records until reviewed.
- Never promote a hypothesis to verified without evidence and a defined check.
- Do not infer causal relationships from temporal order alone.
- Keep public research documentation separate from protected implementation details.
- External model integrations require explicit credentials, permissions, and provider-side setup.

## 8. Initial acceptance criteria

- A model can locate the entry instructions and current state.
- A task has a unique ID, scope, owner model, and expected report.
- Reports are append-only or uniquely named.
- Findings retain source paths and verification status.
- Conflicts can be recorded without silent resolution.
- A daily Mermaid diagram can be regenerated from committed coordination records.
- The workflow clearly reports when an external model has not checked in.


## 10. Constitutional fractal governance

All cabinet tasks that inspect, extract, compose, verify, or publish logic structures are governed by [Constitutional Fractal Governance V1](CONSTITUTIONAL_FRACTAL_GOVERNANCE_V1.md). The corresponding [constitutional fractal diagram](../diagrams/constitutional-fractal-governance.mmd) is a derived view, not an independent source of truth.

The cabinet must preserve source lineage, epistemic status, typed relations, scope, parent IDs, composition-rule versions, contradiction records, and verification receipts at every L0–L3 scale. Model consensus and structural checks cannot promote a claim to VERIFIED. Missing required evidence leads to REVIEW / ABSTAIN / HALT. These are required workflow policies; automatic enforcement is not claimed until implemented and tested.

## 11. Implementation status

This file is a design specification. The cabinet plugin, external provider connections, automated cross-provider messaging, daily report-generation workflow, and full automatic enforcement of constitutional invariants are **not established by this document**. Track implementation in GitHub issues or pull requests with tests and deployment evidence.
