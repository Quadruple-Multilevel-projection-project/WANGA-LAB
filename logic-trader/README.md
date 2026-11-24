# Logic Trader & Logic Market Prototype

**Status:** PROTOTYPED (rule-based paper trader and static catalog); NOT_YET_VERIFIED for any market, customer, or production use.

This repository folder establishes the first bounded implementation of the Logic Trader Agent and the reusable-logic catalog. It deliberately does **not** connect to exchanges, broker accounts, wallets, payment processors, or blockchain contracts.

## Components

- src/logic_trader.py — deterministic moving-average rule fixture, in-memory paper fills, position-size cap, price-shock halt, drawdown gate, and explicit decision records.
- run_demo.py — fixed synthetic-price demonstration.
- tests/test_logic_trader.py — stdlib unit tests for input validation, warm-up, size cap, risk halting, policy validation, and determinism.
- catalog.json — draft logic product registry with null pricing until owner configuration.
- nft/ECM-01.metadata.json — NFT-style metadata draft only; not minted, not listed, no contract/token ID, and no declared license.
- manifests/logic-trader.v1.json — runtime boundaries and lifecycle states.
- index.html — static catalog and browser-only synthetic demonstration.

## Run locally

Requirements: Python 3.11+; standard library only.

    python logic-trader/run_demo.py
    python -m unittest discover -s logic-trader/tests -v

## Architecture roles

The current implementation uses clearly labelled rule adapters, not biological brain simulations:

- Mouse-cortex role: moving-average trend estimate (PROTOTYPED as a simple rule, not MICrONS data).
- Drosophila role: translate an approved rule signal into a local paper fill (PROTOTYPED).
- Zebrafish role: stop on abrupt price moves and breached drawdown limits (PROTOTYPED rule).
- C. elegans role: noise/quality filtering (SPECIFIED_NOT_IMPLEMENTED).

The CRDT/GossipSub mesh and shared reward pool are not installed. They remain specified/planned in the manifest. No claim is made that a connectome dataset itself forms a ready-to-run autonomous trading agent.

## Product / NFT lifecycle

A catalog entry is not yet a store listing. Before publication, set price, currency, commercial license, buyer rights, canonical package hash, terms, availability, support policy, and target site. Before an NFT can be issued, additionally settle the network, metadata/media storage URI, contract, minting authority, and publication approval. Metadata drafts must not be described as minted NFTs.

## Safety and evidence policy

- PAPER_ONLY is a protected execution boundary.
- Network access, live order submission, wallet access, minting, and checkout are disabled.
- The sample feed is synthetic and deterministic; its output does not establish profitability or predictiveness.
- PROTOTYPED or TESTED is not VERIFIED. Verification requires an agreed evaluation protocol, held-out or real-source data, error thresholds, reproducible evidence, and review.
- Never insert exchange API secrets or wallet private keys into repository files, issues, or logs.
