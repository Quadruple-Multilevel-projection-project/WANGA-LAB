# WANGA-LAB Multi-Model Handoff Protocol

**Status:** Proposed operating protocol  
**Date:** 2026-11-25

## Mandatory first-read sequence

1. Read this protocol.
2. Read the current project state and active task ledger (to be maintained by the coordinator).
3. Read only the repositories and paths assigned to your task.
4. Check prior reports for overlap before repeating work.

## Capability declaration

At the beginning of each run, report:
- model/provider and model version if exposed;
- available GitHub, web, file, code execution, diagram, and automation tools;
- access limitations and permissions;
- context/output limits only when known;
- task size you can complete reliably;
- any required connector or credential setup (never disclose secrets).

Do not claim access to another provider's private tools or accounts.

## Task allocation

- Round A: repositories 1–8 in the project master assignment.
- Round B: repositories 9–16.
- Round C: repositories 17–22 plus explicitly scoped discovery.
- The coordinator must mark each task AVAILABLE / CLAIMED / IN_PROGRESS / COMPLETE / BLOCKED.
- A model must claim its round before scanning. No duplicate claim unless the coordinator requests independent review.

## Evidence row format

`ID | Model | Round | Source (repo/path) | Finding (faithful to source) | Explicit/Implicit | Evidence URL | Status | Gap | Next action`

Only report new findings or materially refined findings. A repeated finding is omitted unless it is needed to document a conflict or verification.

## Epistemic labels

- VERIFIED: directly supported by inspectable source and the stated verification procedure.
- ASSESSMENT: reasoned interpretation supported by sources, not independently proven.
- HYPOTHESIS: plausible proposal or explanation awaiting test.
- NOT_YET_VERIFIED: source or required check is unavailable/incomplete.

## Conflict handling

Never silently reconcile contradictory reports. Create a conflict record containing both claims, their sources, timestamps, and the test needed to resolve them. The coordinator or project owner decides whether to run that test.

## Handoff

Every completed task must include:
- exact paths inspected;
- concise findings and source links;
- files changed and commit/PR references;
- unresolved gaps and conflicts;
- recommended next task and suitable capability tier.

A handoff is VERIFIED only after the receiving model or automation confirms receipt. Otherwise use PENDING.

## Daily diagram

The diagram is a derived view of committed records, not an independent source of truth. Update it only when repository state changes. Preserve dated snapshots under `diagrams/daily/YYYY-MM-DD/` and keep the current diagram at `diagrams/plugin-cabinet-coordination.mmd`.

## Security

Never commit API keys, tokens, passwords, private user data, or provider credentials. Use GitHub Actions secrets or an approved secret manager. External models do not gain repository access merely because this protocol names them.
