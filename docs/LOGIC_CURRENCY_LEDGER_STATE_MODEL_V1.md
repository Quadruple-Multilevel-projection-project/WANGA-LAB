# Logic Currency Ledger — State Model v1
Date: 2026-11-20
Status: DESIGN / PARTIAL — no token issuance and no monetary value assigned.

## Purpose
Separate contribution proposals, authorized internal allocations, internal credit posting, actual cash and any future external token design. The ledger is an append-only evidence and attribution system, not proof that Logic Credits are money or market value.

## Verified implementation evidence
- Event schema: `schemas/logic-contribution-ledger-event-v1.schema.json` on PR #150 head `774252990d53bc7f7a2687f942a2230db5031619`.
- Verifier: `business_brain/ledger_verifier.py`.
- Test file: `tests/test_logic_contribution_ledger_verifier.py`.
- CI run: `44478402542`, job `135404419593`.
- Exact job steps: “Logic contribution ledger verifier tests” (step 5) and “Logic contribution ledger JSON Schema validation” (step 6); both completed with conclusion `success`.
- The test file covers a valid two-event hash chain, duplicate event IDs, broken previous-hash links, modified events and empty ledgers.
- The dedicated schema command validates the example and rejects negative quantities and pending authorization for `CREDIT_APPROVED`.

## Required quantity separation
| Quantity | Meaning | Balance effect |
|---|---|---|
| `planned_quantity` | Proposed contribution credit not yet approved | No balance |
| `approved_quantity` | Authorized internal allocation not yet posted | No issued balance |
| `issued_internal_quantity` | Non-transferable internal Logic Credit posted after a separate authorization | Internal ledger only; not cash, revenue, a security or an external token |
| `external_token_quantity` | Any externally transferable or redeemable token quantity | Must remain 0; no issuance is authorized |

The quantities must never be collapsed into one “balance”. A proposal cannot become approved by being recorded. Approval cannot become internal issuance without a distinct authorization and event. External token issuance remains prohibited by this design until separate legal, technical, governance and explicit user approval gates are satisfied.

## Event mapping
- `CREDIT_PROPOSED` → contributes to planned quantity only.
- `CREDIT_APPROVED` → moves an authorized amount from planned to approved; does not post an issued balance.
- Internal issuance is a future, separately authorized transition. The current event schema does not yet define a dedicated internal-issuance event; do not infer that it exists.
- `CREDIT_REVERSED` → append a compensating event; never delete or overwrite history.
- `USAGE_RECORDED` → records internal consumption/use, not a cash payment.
- Any rejected or corrected proposal must preserve provenance and the prior event chain.

## Provenance and authorization
Every event must retain:
- unique event ID and event type;
- actor/beneficiary references and contribution reference;
- evidence references and source version;
- quantity and unit, with `LOGIC_CREDIT_INTERNAL` explicitly non-cash;
- timestamp, authorization state and approver reference where applicable;
- previous event digest and current event SHA-256.

No self-approval for a material allocation. Corrections are append-only. A broken hash chain, duplicate ID, negative quantity, missing source or invalid authorization blocks the ledger transition.

## Separate operating-finance ledger
Track independently:
- actual cash collected;
- actual cash costs paid;
- contribution margin on delivered work;
- qualified pipeline;
- forecasts/scenarios;
- internal Logic Credits.

Contribution margin is computed only from collected cash and attributable actual delivery costs. Internal Logic Credits never enter cash, revenue or margin totals. The connected evidence reviewed in this run did not expose transaction-level cash records; actual cash collected, actual cash costs and contribution margin are therefore NOT_YET_VERIFIED, not assumed to be zero.

## Next acceptance gate
1. Define and schema-validate the aggregate state object with separate planned, approved, issued-internal and external-token quantities.
2. Add a distinct internal-issuance event only after its authorization and rollback semantics are approved.
3. Add tests for every allowed and forbidden transition.
4. Keep external token quantity fixed at zero until a separate approved legal/security release gate.
5. Re-run the dedicated CI schema and verifier steps on the exact commit.

## Explicit exclusions
No token issuance, transfer, exchange, redemption, reserve backing, fiat peg, guaranteed value, share offering or payment was performed or authorized.
