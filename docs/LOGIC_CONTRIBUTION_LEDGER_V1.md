# AI231 Logic Contribution Ledger — Event Contract V1

Timestamp: 2026-11-15T18:54:51+02:00
Contract_Start_Time: 2026-11-15T18:54:51+02:00
Action_ID: ACT-20261115-AI231-CYCLE1-EXEC-012
Status: SPECIFIED — schema and sample committed on an isolated branch; not a live ledger.

## Purpose
Define an auditable, append-only internal record of logic-package contributions, review decisions, proposed credits, approved credits, usage and corrections. This contract is a bookkeeping interface only.

## Explicit financial and legal boundary
- Internal credits are not cash, revenue, equity, debt, a security, a cryptocurrency, a transferable token or a claim on assets.
- No exchange rate, fiat peg, redemption, guaranteed value, public sale or investment return is implied.
- Customer cash and operating revenue must be recorded in the organization's accounting system, separately from this contribution ledger.
- No credit can be approved without a named authorization reference and accepted evidence.
- Rejected contributions cannot earn credits. Corrections are new events; historical events are never edited or deleted.

## Event lifecycle
SUBMITTED → IN_REVIEW → ACCEPTED/REJECTED → CREDIT_PROPOSED → CREDIT_APPROVED → USAGE_RECORDED or CREDIT_REVERSED.
Transitions are recorded as new events and linked by contribution_ref. The schema does not itself prove that a review occurred; evidence_refs and authorization records must resolve to external review artifacts.

## Required controls
1. Unique event_id.
2. Event time and ledger-record time are separate.
3. Actor, subject and contribution references are mandatory.
4. At least one evidence reference is mandatory.
5. Review status is explicit.
6. Unit is typed and cannot be mistaken for fiat.
7. Authorization state, approver and policy reference are explicit.
8. Hash chain fields support tamper-evidence; event_sha256 must be computed over a canonical serialization excluding event_sha256 itself. previous_event_sha256 links to the prior accepted event.
9. Reversal and correction are append-only.
10. No issuance, transfer, custody or public token functionality is implemented by this schema.

## Implementation boundary
The schema validates event shape only. It does not implement hash-chain verification, access control, double-entry accounting, legal classification, identity assurance, anti-Sybil review or external payment rails. Those require separate tested components and human/legal approval.

## Next acceptance gates
- Implement canonical JSON hashing and chain verifier.
- Add duplicate event and broken-chain negative tests.
- Define deterministic credit policy only after contribution scoring and appeal rules are independently reviewed.
- Keep cash ledger and internal contribution ledger physically/logically separate.
- Obtain legal review before any transferable or redeemable unit is considered.


## Cash measurement boundary — 2026-11-22 clarification

The aggregate cash snapshot keeps three concepts separate:
- `actual_cash_collected_minor_units`: cash receipts actually collected.
- `actual_cash_costs_paid_minor_units`: all cash costs actually paid.
- `actual_variable_cash_costs_paid_minor_units`: the direct/variable subset of paid costs used for contribution-margin calculation.

For a VERIFIED cash snapshot, `contribution_margin_minor_units = actual_cash_collected_minor_units - actual_variable_cash_costs_paid_minor_units`. Variable costs must not exceed total cash costs paid. Contribution margin is not net profit or total cash flow; fixed operating costs, taxes, partner obligations, reserves and other expenses remain separately relevant to distributable profit and cash runway. While cash evidence is NOT_YET_VERIFIED, every cash amount and currency remains null. The illustrative fixture is not a live financial record.
