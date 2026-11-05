# Logic Trader and Logic Marketplace — Implementation Record V1

**Record date:** 2026-10-12  
**Current status:** PROTOTYPED / NOT_YET_VERIFIED  
**Scope:** first bounded software fixture and market/catalog data structure

## What is implemented

The new logic-trader/ folder provides a deterministic, rule-based paper-trading harness over fixed synthetic prices; an in-memory position ledger; a position cap; a per-tick shock halt; a drawdown gate; a draft product catalog; a draft NFT-metadata record for ECM-01; and a static catalog/demo page. Unit tests cover input validation, warm-up behavior, size limits, shock halts, policy validation, and repeatability.

## What is not implemented

There are no biological connectome runtimes, MICrONS/FlyWire/C. elegans dataset integrations, live market-data adapters, broker or exchange clients, real orders, wallet handling, NFT minting, payment processing, production storefront, CRDT replication, GossipSub mesh, or shared-reward pool. These must not be reported as installed or VERIFIED. The species-labelled roles are architectural analogies and software rule adapters only.

## Logic marketplace records

The catalog seeds ECM-01 Evidence Gatekeeper, ECM-02 Task Decomposer & Scope Binder, ECM-03 Deterministic Action Filter, and LTA-01 Logic Trader — Paper Risk Gate. Every price is null and every listing is draft/unpublished. That avoids inventing commercial terms. ECM-01 has metadata in draft form only; it is not an NFT on a chain. The license, package hash, chain, contract, token ID, and storage URL remain unset.

## Lifecycle gates

1. SPECIFIED: interfaces, constraints, source lineage and acceptance criteria are defined.
2. PROTOTYPED: local code exists and can be executed.
3. TESTED: automated tests have passed in CI for the commit under review.
4. VERIFIED: a separate evidence-backed evaluation meets approved error thresholds on representative or held-out data and is independently reviewed.

Passing synthetic unit tests alone cannot support VERIFIED, profitability, semantic truth, or production suitability.

## Next gated steps

- Review and run the paper-trading tests in CI.
- Select the canonical Wix site for a future catalog/storefront edit; no Wix site is changed by this record.
- Owner supplies price/currency, license and buyer rights, product terms, and intended publication scope.
- Only after review: integrate a market-data provider in read-only mode, run backtests on sourced data with costs/slippage, and keep paper mode as default.
- Consider NFT minting only after asset hashes, legal rights, terms, chain, storage, contract review, and explicit publication authorization are settled.
- Design CRDT/GossipSub mesh separately with threat model, conflict tests, authentication, replay protection, and partition/recovery tests.
