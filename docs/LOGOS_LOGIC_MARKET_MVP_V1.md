# LOGOS Logic Market — MVP Contract v1.0

**Status:** SPECIFIED / IMPLEMENTATION IN PROGRESS  
**Branch:** `feat/logos-logic-market-mvp`  
**Scope:** Logic-asset registry, simulated order book, positions, and evidence-backed valuation. This is not a live financial instrument or a claim that logic already has a universally accepted monetary price.

## 1. Market object

A **Logic Asset (LA)** is a versioned, source-linked logical structure that can be independently inspected and replayed. Each asset MUST include:

- `asset_id`, `version`, `canonical_representation_hash`
- source references and provenance/lineage
- extracted premises, relations, derivations, and explicit boundaries
- evidence state: `OBSERVED | DERIVED | CANDIDATE | VALIDATED | DISPUTED | UNRESOLVED`
- reproducibility protocol and test results
- known contradictions, uncertainty, domain fit, and dependencies
- license/permission state for use or transfer

No asset is market-eligible merely because an agent generated it.

## 2. Logic Unit (LU)

The initial **Logic Unit (LU)** is an internal accounting unit for simulation and comparison. It is not money, a security, a stablecoin, a token on a public chain, or a claim of legal ownership.

- `LU = NOT_MONETIZED` until a valuation method is empirically calibrated.
- Prices, exchange rates, and scoring weights remain `UNRESOLVED` until measured and approved.
- Never convert LU to fiat, execute a payment, or imply investment return in this MVP.
- Keep research value, usage/license value, and monetary price as separate fields.

## 3. Candidate valuation dimensions

Record measurements independently; do not silently combine them into a single score:

1. provenance completeness
2. derivation traceability
3. independent reproducibility
4. contradiction status
5. boundary/scope clarity
6. task-specific utility evidence
7. duplication/novelty evidence
8. runtime and compute cost
9. permission/license status
10. uncertainty and coverage

A later valuation function may be proposed only after a versioned dataset, calibration method, uncertainty report, and human approval exist. No invented weights. No universal `H=0.0` or guaranteed zero-drift claim.

## 4. Simulated market operations

MVP operations are append-only simulation records:

- `REGISTER_ASSET`
- `SUBMIT_BID`
- `SUBMIT_ASK`
- `MATCH_SIMULATED`
- `OPEN_SIMULATED_POSITION`
- `CLOSE_SIMULATED_POSITION`
- `REVALUE_SIMULATED_POSITION`
- `DISPUTE_ASSET`
- `FREEZE_ASSET`

Every event must include actor ID, event time, input hash, policy version, prior-event reference, and validation receipt. No event may overwrite the source evidence. Corrections are new events linked to the prior event.

## 5. Anti-drift transaction gate

Every asset operation and agent handoff passes the shared LOGOS Action Guard:

1. freeze request and source snapshot
2. verify source lineage and authorization
3. parse claims without silently upgrading interpretation to fact
4. validate schema, evidence status, scope, and contradictions
5. verify dependencies and cycle detection
6. calculate only explicitly specified metrics
7. append audit receipt and integrity hash
8. block on missing required source, invalid permission, unresolved critical conflict, failed test, or tampered hash

A blocked operation returns a reason code and evidence references; it does not retry indefinitely.

## 6. Agent network scale

**Target:** 10,000 logical agents is a capacity goal, not a claim that 10,000 agents have been provisioned.

Start with bounded role templates and a small test cohort. A logical agent is a registered role/configuration until an execution runtime, identity, permissions, resource budget, health probe, and audit stream are actually connected.

Initial roles:
- SOURCE_LINEAGE
- LOGIC_EXTRACTION
- RELATION_GRAPH
- DERIVATION_VALIDATOR
- DRIFT_FORENSICS
- REPLICATION_TESTER
- ASSET_REGISTRY
- MARKET_SIMULATOR
- POSITION_LEDGER
- RISK_AND_LIMITS
- EVIDENCE_AUDITOR
- NETWORK_SUPERVISOR

Scale only when measured task quality, queue latency, failure rate, and compute cost justify it. Use concurrency groups, per-job timeouts, bounded retries, deduplication, and cycle detection. No unbounded recursive spawning.

## 7. Minimum controls

- Read-only source access by default; write access scoped per job.
- No secrets in repository files or Airtable records.
- No live payments, fiat conversion, exchange listing, or real-money trading in this MVP.
- Human approval required for deployment, permission changes, publication, licensing commitments, and any future live financial operation.
- Keep simulated balances and positions segregated from payment-provider balances.
- Every metric is labelled `MEASURED`, `DERIVED`, `HYPOTHESIS`, or `UNRESOLVED`.

## 8. Acceptance criteria

The MVP is not complete until tests demonstrate:

- invalid or missing provenance blocks asset registration
- an unresolved critical contradiction blocks matching
- duplicate asset versions are detected by canonical hash and version policy
- simulated bids/asks match deterministically under a documented rule
- positions can be replayed from append-only events
- tampered event hashes fail verification
- a resource timeout stops runaway work
- audit output records the exact rule/configuration version used
- tests do not claim live trading, external settlement, or 10,000 active agents

## 9. Source alignment

This contract follows WANGA-LAB's documented sequence:

`SOURCE → EXTRACTION → RECONSTRUCTION → LOGIC IDENTIFICATION → RELATIONS / DERIVATIONS → BOUNDARIES → CONFIGURATION → DRIFT FORENSICS → VERIFICATION`

It also follows the repository's evidence discipline: observation, assumption, evidence, inference, and hypothesis are distinct. This document specifies an MVP; it does not prove the market engine has been implemented or empirically validated.
