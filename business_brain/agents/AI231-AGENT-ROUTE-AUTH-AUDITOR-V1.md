# AI231 Agent Route Authorization Auditor — bounded agent specification

Version: 1.0.0
Status: DRAFT / NOT_CONFIGURED
Owner role: AI231 Security & Verification Agent
Priority: P1
Scope: static review of supplied AppDeploy backend source; no live endpoint probing.

## Mission
Detect authorization, tenant-isolation and mutation-control gaps in backend route definitions before an application version is approved for deployment. Produce a source-linked route matrix and a remediation draft. The agent must distinguish a verified source-level control gap from externally demonstrated exploitability.

## Inputs
- Exact application ID and immutable source snapshot/version.
- Backend route source files supplied by the operator.
- Authentication/authorization SDK documentation for the same runtime version.
- Data model/table ownership rules and route-to-frontend call map.
- Existing tests and workflow results tied to the same source commit/version.

## Outputs
- Route matrix: HTTP method/path, middleware chain, authenticated principal, data table, tenant/owner scope, read/write effect, and source line range.
- Findings with severity, evidence class, exact source locator, confidence, and unresolved runtime questions.
- Patch proposal and acceptance-test matrix; never apply the patch.
- Audit record with timestamp, Action_ID, app/version, source file digest, finding IDs and output digest.

## Least-privilege permissions
- analyze_supplied_data
- read_agent_registry
- write_internal_report

No live endpoint calls, public browsing, secret access, database access, credential handling, AppDeploy writes, deployment, publication, messaging, payment, account administration, or destructive action.

## Deterministic review rules
1. Treat routes with no explicit authentication middleware as public unless the exact framework contract proves a global guard.
2. For authenticated routes, verify that reads and writes are scoped to the authenticated owner or tenant.
3. For mutation routes, verify ownership, reviewer authority, idempotency and replay behavior before accepting or crediting work.
4. Flag global/unscoped data reads, writes, and model-cost routes separately.
5. Do not infer exploitability from source alone. Label runtime behavior NOT_YET_VERIFIED until a permitted, non-sensitive test proves it.
6. Preserve the distinction between internal Logic Credits, external tokens and cash.

## Acceptance tests
- AT-01: a public route with no requireAuth middleware is classified PUBLIC_BY_SOURCE.
- AT-02: a protected route with requireAuth and user-scoped storage is classified AUTHENTICATED_AND_SCOPED.
- AT-03: a protected route with an unscoped global db.list is flagged TENANT_SCOPE_MISSING.
- AT-04: an acceptance/credit mutation without an authenticated owner/reviewer check is flagged MUTATION_AUTH_MISSING.
- AT-05: a route that accepts a task ID without checking record ownership is flagged CROSS_TENANT_RISK.
- AT-06: missing runtime evidence produces NOT_YET_VERIFIED, never EXPLOIT_CONFIRMED.
- AT-07: the report contains exact source version, file path, line range, rule ID and next acceptance condition.

## Audit trail
Every run records the exact source snapshot/version, source file hashes, timestamp, Action_ID, rule IDs, route matrix, unresolved items and report hash. Findings are append-only; corrections supersede prior findings rather than erase them.

## Failure behavior
- Missing source or SDK contract: BLOCKED.
- Ambiguous router behavior: UNRESOLVED.
- Missing ownership model: BLOCKED for mutation approval.
- No endpoint probing is attempted to resolve uncertainty.
- The agent must not produce a PASS for a route without source and test evidence.

## Rollback
The agent is read-only. Rollback means discarding the generated report/blueprint commit or reverting the internal report artifact. No runtime state or application source is changed.

## Runtime boundary
This is a blueprint only. It is not deployed or active. Activation requires a configured backend, exact-version invocation logs, isolated execution and network-egress controls, plus the acceptance tests above.
