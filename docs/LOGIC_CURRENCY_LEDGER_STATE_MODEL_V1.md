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


## 2026-11-21 aggregate-state implementation update
A separate aggregate-state contract and fail-closed transition helper have been added on the existing Logic Currency Ledger draft PR #150:
- Schema: `schemas/logic-currency-ledger-state-v1.schema.json`
- Illustrative empty fixture: `examples/logic-currency-ledger-state.v1.example.json`
- Transition helper: `business_brain/ledger_state.py`
- Dedicated validator: `scripts/validate_logic_currency_ledger_state.py`
- Dedicated tests: `tests/test_logic_currency_ledger_state.py`
- Workflow steps: `Logic currency ledger aggregate-state schema validation` and `Logic currency ledger aggregate-state transition tests` in `.github/workflows/repository-integrity.yml`

The v1 aggregate schema keeps planned, approved, internal-issued and external-token quantities distinct. It requires internal-issued quantity and external-token quantity to remain exactly zero; no issuance event is implemented. Planned quantity requires source-event provenance, approved quantity requires authorization references, and unverified cash fields remain null. The transition helper only permits proposal and authorized approval movements; issuance and reversal fail closed.

**Status:** implementation committed to PR #150 branch; CI for the exact new head is pending. This does not create a live ledger or issue Logic Credits/Logic Coin.


## CI result — 2026-11-21
The aggregate-state implementation was verified on the exact PR #150 head commit `a471226e8763f9326613abdd5bbc1a01501ea619`.

- Workflow: `.github/workflows/repository-integrity.yml`, blob `5049b14b410569e14b9aa91023df69c9e01e4839`.
- Workflow run: `44879970500`.
- Job: `136774097187`, name `integrity`, conclusion `success`.
- Step: `Logic currency ledger aggregate-state schema validation` — success. Exact command: `python scripts/validate_logic_currency_ledger_state.py`. Output: the exact schema validated the exact example; non-zero external tokens, internal issuance and unverified cash promotion were rejected.
- Step: `Logic currency ledger aggregate-state transition tests` — success. Exact command: `python -m unittest discover -s tests -p 'test_logic_currency_ledger_state.py' -v`. Result: 11 tests ran; `OK`.
- Existing event-ledger verifier step also passed on the same run: five tests ran; `OK`.

**Acceptance:** PASS for the draft aggregate-state schema, validator and proposal/approval transition tests on this commit. **NOT_YET_VERIFIED:** a live append-only ledger, persistent storage, production authorization service, actual cash transaction records and any internal issuance. Issued-internal quantity and external-token quantity remain fixed at zero in v1.


## 2026-11-25 — independent two-pass CI revalidation

**PR #150 state:** OPEN / DRAFT / UNMERGED. Branch `agent/ai231-cycle1-ledger-foundation`, head `d77a91bc4456ec0894257fba2a9fc8ae1d164a62`, base `2e43830e8b624568ebc9195977a6fdb35fbdacff`. Compared with current main `1d9afec596a64f59290941c6ea41d3322f7b8492`, the branch is 30 commits ahead and 124 behind; rebase/reconciliation is required before merge.

**Two-pass evidence:** the run was independently re-fetched by querying the exact PR head commit, then re-fetching the job, step list, log and workflow YAML. Workflow: `.github/workflows/repository-integrity.yml`, blob `5049b14b410569e14b9aa91023df69c9e01e4839`. Run `45001947753`, job `137145211088` (`integrity`), conclusion `success`. The runner log checks out synthetic PR merge commit `747217843211f779e02008c74415d226676f04ae`; the workflow-run lookup was tied to head `d77a91bc4456ec0894257fba2a9fc8ae1d164a62`. Both identifiers are retained because the runner executed the merge ref.

Exact successful steps:
- Step 5 — `Logic contribution ledger verifier tests`: `python -m unittest discover -s tests -p 'test_logic_contribution_ledger_verifier.py' -v`; 5 tests ran; `OK`.
- Step 6 — `Logic contribution ledger JSON Schema validation`: the inline validator loaded `schemas/logic-contribution-ledger-event-v1.schema.json` and `examples/logic-contribution-ledger-event.v1.example.json`; it validated the example and rejected negative quantity and pending authorization for `CREDIT_APPROVED`.
- Step 7 — `Logic currency ledger aggregate-state schema validation`: `python scripts/validate_logic_currency_ledger_state.py`; output confirms the exact state schema validates its example, rejects non-zero external tokens/internal issuance/unverified cash promotion, and checks the contribution-margin invariant.
- Step 8 — `Logic currency ledger aggregate-state transition tests`: `python -m unittest discover -s tests -p 'test_logic_currency_ledger_state.py' -v`; 14 tests ran; `OK`.

**Acceptance:** PASS for the draft event schema, aggregate-state schema and the exact transition/verifier tests on the PR merge commit. **NOT_YET_VERIFIED:** integration on current main, a persistent/live ledger, production authorization, actual cash transactions, and any internal or external issuance. The PR remains unmerged; no token or Logic Credit was issued.
