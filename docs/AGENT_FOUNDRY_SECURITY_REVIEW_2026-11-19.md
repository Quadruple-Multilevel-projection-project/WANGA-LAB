# AI231 Agent Foundry — security and runtime review
Date: 2026-11-19
Repository: Quadruple-Multilevel-projection-project/WANGA-LAB
App: `ai231-agent-foundry-35gumn`
Observed AppDeploy source version: `1794734398523`
Deployment status: `ready` (AppDeploy status read; this is deployment status, not agent-runtime acceptance)

## Executive result

**VERIFIED — code-level authorization gap.** Three general Agent Foundry API routes have no `requireAuth()` middleware and access shared global task/ledger tables. The AppDeploy SDK reference distinguishes protected routes (explicit `requireAuth()`) from unprotected public routes. No unauthenticated exploit request was sent; this finding is based on the exact deployed source and SDK semantics.

**NOT YET VERIFIED — runtime safety.** The accessible deployment status reports ready and the QA snapshot reports no surfaced frontend/backend errors, but no successful per-role invocation logs, per-user isolation test results, sandbox evidence or network-egress controls were available. The seven role profiles therefore remain role definitions; they are not promoted here to seven verified active agents.

**BLOCKED — no production change.** Authentication, data-isolation and credit-write changes are security-sensitive. This document is a draft patch plan only; no AppDeploy source, secret, environment, access setting or deployment was changed.

## 1. Exact findings

| Severity | Route / source | Verified source behavior | Risk |
|---|---|---|---|
| P0 | `backend/index.ts:119-121` — `GET /api/overview` | Route has no `requireAuth()`; reads shared `agent_tasks` and `logic_ledger` tables and returns their records | Potential unauthenticated disclosure of task outputs and internal credit records |
| P0 | `backend/index.ts:123-137` — `POST /api/agents/run` | Route has no `requireAuth()`; invokes `ai.run()` and writes to shared `agent_tasks` | Potential anonymous model-cost abuse and shared task-record creation |
| P0 | `backend/index.ts:139-153` — `POST /api/tasks/:id/accept` | Route has no `requireAuth()`; reads shared tasks and transactionally writes to shared `logic_ledger` | Potential unauthorized acceptance and internal Logic Credit issuance |
| P1 | `backend/index.ts:314+` — `POST /api/wix/tasks/:id/accept` | Route is protected with `requireAuth()`, but creates a per-user ledger entry after acceptance | The write path conflicts with the current run rule: no Logic Credit issuance without separate explicit authorization |
| P1 | `tests/tests.json` | Four UI scenario definitions cover blueprint creation, run, incomplete specifications and draft-execution guard; no API-level anonymous-auth, cross-user isolation or no-credit-issuance test is present | Current QA definitions do not prove the backend security boundary |

The source also contains a `tables(userId)` helper at `backend/index.ts:113-115` for per-user Wix tables. The three general routes above do not use it.

## 2. Required non-production patch

1. Add `requireAuth()` to `GET /api/overview`, `POST /api/agents/run` and `POST /api/tasks/:id/accept`.
2. Use per-user task and ledger tables derived from the authenticated `user.userId`; do not read or write the shared `agent_tasks` or `logic_ledger` tables for user-facing requests.
3. Verify ownership of every task ID before reading, accepting or updating it. A task ID is not an authorization credential.
4. Disable all Logic Credit writes in both general and Wix task-acceptance routes. Return an explicit `CREDIT_ISSUANCE_NOT_AUTHORIZED` result; do not create a ledger row, balance or transferable unit.
5. Update the UI so acceptance means review/acceptance of a deliverable only. Remove any action label that implies credit issuance until separately authorized.
6. Gate frontend overview refresh on a successfully restored authenticated user; do not weaken the backend to accommodate an anonymous initial fetch.

## 3. Required acceptance tests

- Anonymous `GET /api/overview` returns 401 and no task/ledger data.
- Anonymous `POST /api/agents/run` returns 401 before `ai.run()` and creates no task record.
- Anonymous `POST /api/tasks/:id/accept` returns 401 and creates no ledger entry.
- User A cannot read, run, accept or mutate a task owned by User B.
- Authenticated acceptance changes only the caller's task status and creates **zero** Logic Credit entries under the current no-issuance rule.
- Wix task acceptance also creates zero Logic Credit entries.
- A failed transaction leaves task and ledger state unchanged.
- Audit record includes actor ID, task ID, prior state, new state, timestamp, request ID and result; never store access tokens or secrets in the record.

## 4. Rollback and permission gate

- Scope: new non-production AppDeploy version only after explicit approval for this exact app and patch.
- Before any future deployment, capture the current version and source snapshot, then test in a non-production environment.
- Rollback: restore the exact last-known-good AppDeploy version from version history and verify the restored version. Capture its immutable version identifier before deployment.
- No secrets, access controls, production records or published Wix pages are changed by this report.
- Current status: **BLOCKED — production security change not authorized.**

## 5. Evidence and limits

**VERIFIED**
- AppDeploy app ID: `ai231-agent-foundry-35gumn`.
- `backend/index.ts` read from AppDeploy version `1794734398523`, 337 lines.
- Exact route and table locators listed above.
- AppDeploy SDK reference for API/auth was consulted; it states `requireAuth()` validates the Authorization header and that routes without it are public.
- `tests/tests.json` contains four UI test definitions; it does not show executed test results.

**ASSESSMENT**
- The three unprotected general routes create a high-severity exposure path because they read/write shared task and credit tables.
- The unprotected `ai.run()` route creates a cost-abuse risk.

**NOT YET VERIFIED**
- Whether any unauthenticated caller has accessed these routes.
- Whether task or credit records have been created in production.
- Per-user isolation, successful invocation logs, sandbox isolation and network-egress restrictions.
- Runtime acceptance of any individual role profile.

No unauthenticated probe was made and no production data was read.
