# Agent Foundry Wix inventory reconciliation

Date: 2026-11-22
Priority: P1
Status: VERIFIED_SOURCE_DRIFT / APP_UPDATE_BLOCKED
App: AI231 Agent Foundry (ai231-agent-foundry-35gumn), source version 1794734398523

## Comparison
- Connected Wix account inventory: 70 sites, returned in two pages (50 + 20) by ListWixSites.
- Agent Foundry backend seed array wixInventory: 65 unique site IDs in backend/index.ts.
- Live account IDs absent from the seed array: 7.
- Seed IDs no longer present in the live account inventory: 2.

## Live sites absent from the seed
| Site | Site ID |
|---|---|
| Eran — Drift & | dfa2852c-4f28-4823-a51f-999f638a4d12 |
| Map Link Provenance | f3a43d48-2263-4b32-ad69-f4fa2939ded5 |
| Deep Reasoning Logic Principle | e0d939ae-a30e-4d30-aad9-3c0439295de8 |
| AI231 Global Neural Governance | 70e8848a-5ab9-459d-905d-1d82d5706e81 |
| 500-Second Global Referendum | 195d2b6c-d07d-4215-9aee-16bf38061769 |
| My Site 18 | 6a2cfa42-4139-437a-9f92-be1642dbbed1 |
| Operational Ai Dri 4 | dbcbe570-be5f-4342-9c62-145afc0175dd |

## Seed IDs not present in the live account list
- 6a2cfa42-4139-4378-a9a3-49c3c4a8b1a8
- dbcbe570-be5f-434c-9c62-145afc0175dd

The two stale IDs resemble the current My Site 18 and Operational Ai Dri 4 records but are not exact matches. Do not infer identity solely from similar names; reconcile by exact site ID.

## Why this matters
The AppDeploy backend's POST /api/wix/sync derives its inventory from the static wixInventory array. It is not a live dynamic query of all account sites. The UI therefore cannot claim complete account-wide inventory from this seed alone. Some absent sites may be unpublished or intentionally excluded, but no explicit exclusion rule was found in the inspected source.

## Required acceptance
- Resolve all 70 current IDs exactly, with duplicate detection.
- Record published/unpublished state and unresolved URL separately.
- Use an account-level Sites API query or an explicitly versioned inventory source; do not silently infer or replace a site based on a similar name.
- Ensure per-user storage remains isolated.
- Re-run inventory comparison after sync and record counts, missing IDs and stale IDs.
- Do not modify any Wix site as part of inventory reconciliation.

## Owner, dependencies and rollback
- Owner: AI231 Agent Factory.
- Dependencies: exact current account inventory; approved source change to the deployed AppDeploy app; versioned test fixture.
- Permission: read-only analysis now; app source/deployment change requires explicit approval.
- Rollback: preserve AppDeploy version 1794734398523; revert the inventory adapter/seed patch if a future approved version fails.
- Next action: prepare a source patch and acceptance tests in a reviewable staging branch; do not deploy without approval.

## Evidence
- Wix ListWixSites: page 1 = 50, page 2 = 20, total = 70.
- AppDeploy src_read: backend/index.ts, version 1794734398523; 65 unique seed IDs.
- No AppDeploy source update or deployment was performed.
