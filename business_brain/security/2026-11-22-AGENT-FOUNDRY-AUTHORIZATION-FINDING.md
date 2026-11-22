# AI231 Agent Foundry — authorization and tenant-scope finding

Date: 2026-11-22
Priority: P1
Status: VERIFIED_SOURCE_LEVEL / PRODUCTION_REMEDIATION_BLOCKED
Application: AI231 Agent Foundry
App ID: ai231-agent-foundry-35gumn
Live URL: https://ai231-agent-foundry-35gumn.v2.appdeploy.ai/
Inspected source version: 1794734398523

## Executive finding
The deployed AppDeploy application reports deployment status READY and no frontend/backend error entries in the status response. The inspected backend source nevertheless defines three core routes without requireAuth middleware while using global, unscoped task and ledger tables. This is a verified source-level authorization gap and a P1 risk. No unauthenticated endpoint was probed, no data was retrieved through the exposed routes, and external exploitability is NOT_YET_VERIFIED.

## Exact source evidence
Source file: backend/index.ts, snapshot version 1794734398523.

| Route | Source range | Observed control gap | Risk |
|---|---:|---|---|
| GET /api/overview | lines 120–124 | Handler has no requireAuth; reads db.list('agent_tasks') and db.list('logic_ledger') without owner/tenant scope | Potential cross-user task/ledger disclosure |
| POST /api/agents/run | lines 124–139 | Handler has no requireAuth; invokes ai.run and writes to global agent_tasks table | Unauthenticated model-cost/task creation risk |
| POST /api/tasks/:id/accept | lines 140–155 | Handler has no requireAuth; loads global task by ID, marks it accepted, and writes a 1–25 internal LGC ledger entry | Unauthorized acceptance/credit mutation risk |

Contrast: GET /api/agent-builder/blueprints, POST /api/agent-builder/create, POST /api/agent-builder/blueprints/:id/activate, POST /api/agent-builder/blueprints/:id/run and the Wix portfolio routes use requireAuth. The Wix portfolio routes use per-user table names through tables(userId).

## Framework contract
The connected AppDeploy SDK auth reference states:
- Public routes use a single handler.
- requireAuth() validates the Authorization header, sets ctx.user, and returns 401 when no valid token is present.
- Auth is opt-in; protected routes must use requireAuth().
- Data access must be scoped by ctx.user!.userId to prevent cross-user data leaks.

This confirms that the three route definitions are not protected by the documented middleware contract. It does not prove that an external request has successfully exploited them.

## Runtime evidence boundary
- AppDeploy status: deployment READY; snapshot version 1794734398523; frontend_errors=[]; backend_errors=[].
- QA screenshot metadata exists for mobile and web.
- No exact live invocation log, per-route authorization test, sandbox isolation evidence or network-egress denial evidence was returned by the status/source tools.
- Therefore: deployed application = VERIFIED; active autonomous agents, safe isolated execution and external exploitability = NOT_YET_VERIFIED.

## Required remediation design
1. Add requireAuth() to GET /api/overview, POST /api/agents/run and POST /api/tasks/:id/accept.
2. Scope task and ledger reads/writes to the authenticated owner. Add createdBy/owner provenance to new task records.
3. On acceptance, verify the authenticated user owns the task and has the required reviewer authority. Do not accept legacy unowned records by ID.
4. Keep legacy global records hidden until a reviewed migration maps ownership; do not silently expose or assign them.
5. Add server-side rate limits and bounded task quotas for model-invoking routes.
6. Add tests for unauthenticated 401, owner-only reads, cross-user denial, unauthorized acceptance denial, legacy unowned records, and idempotent acceptance.
7. Verify isolation and network egress separately; middleware alone is not a sandbox.

## Permission and rollback
No AppDeploy source change or deployment was performed. Production remediation is BLOCKED pending explicit approval for this specific app/version/change. If a future approved patch fails, the prior deployment version to preserve/restore is 1794734398523; restoring it is itself a production action and requires authorization.

## Evidence class
- VERIFIED: source route definitions, middleware presence/absence, global table names, internal credit mutation, deployed status and inspected source version.
- ASSESSMENT: P1 authorization and tenant-isolation risk.
- NOT_YET_VERIFIED: external exploitability, actual data exposure, invocation volume, sandbox isolation and egress controls.
