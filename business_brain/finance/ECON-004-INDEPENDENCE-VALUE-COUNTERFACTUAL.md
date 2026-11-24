# ECON-004 — Independence Value & Grant Counterfactual Ledger
Classification: Internal management logic. Not legal/tax advice, not an audited saving, and not an external claim.
Timestamp: 2026-11-15T11:57:00+02:00
Contract_Start_Time: 2026-11-15T11:57:00+02:00
Action_ID: ACT-20261115-AI231-INDEPENDENCE-VALUE-005

## Decision rule
Not applying for / not receiving an Israel Innovation Authority (IIA) grant does NOT itself create cash, profit, revenue, or a booked saving. Record realized cash benefit as USD 0 until an actual avoided expense or contractual liability can be evidenced.

## Counterfactual baseline
- Historical project funding estimate supplied by project owner: USD 8M–9M. Exact application, grant amount, approval status, and funding terms not reconciled.
- Current internal expanded project envelope: USD 24M–30M (planning estimate only; midpoint USD 27M).
- No IIA grant receipt, grant agreement, royalty obligation, or grant-linked IP restriction has been evidenced in the materials reviewed for this entry.
- Therefore: no royalty savings, interest savings, or grant repayment savings may be booked as realized.

## Quantifiable scenarios (illustrative only)
If, hypothetically, USD 8M–9M of royalty-bearing grant funding had actually been received and all relevant future sales were derived from funded know-how, official IIA materials describe royalties generally at 3%–5% of annual revenues until repayment of the grant plus applicable interest. This is a contingent repayment mechanism, not an automatic 3%–5% tax on all company sales.
- At USD 1M of eligible annual sales: illustrative royalty cash outflow USD 30K–50K.
- At USD 5M eligible annual sales: USD 150K–250K.
- At USD 10M eligible annual sales: USD 300K–500K.
These are conditional examples, not savings actually earned. Total repayment depends on the grant amount, applicable rules, funded know-how, sales attribution, interest, and program agreement.

## Independence value — non-cash, not booked
Potential strategic benefits of remaining unfunded by IIA:
1. No IIA royalty repayment obligation arising from a grant that was never received.
2. Avoids grant-specific constraints on transfer/licensing of funded know-how and manufacturing relocation that could apply to approved funded R&D.
3. Greater freedom to sequence global R&D and commercial partnerships, subject to ordinary law and existing contracts.
4. Less reporting and grant-compliance overhead.
These are qualitative options/avoided conditional obligations. They are not presently assigned a dollar value because no approved grant agreement, restrictions analysis, legal review, or actual alternative-cost data is available.

## Opportunity cost — must also be recorded
By not relying on IIA, the project also forgoes potential non-dilutive financing. If an eligible grant of USD G had been approved and received, that cash could have funded R&D. Its value must not be ignored. Compare:
Net independence value = evidenced avoided royalty/interest/compliance/constraint cost
minus value of foregone grant cash and any replacement financing cost.
No positive net figure can be asserted without a comparable approved grant offer and cash-flow model.

## Economic Engine accounting rules
Maintain distinct fields:
- grant_applied_usd
- grant_approved_usd
- grant_cash_received_usd
- grant_repayment_obligation_usd
- royalty_rate_applicable
- eligible_revenue_attributable_usd
- royalty_paid_usd
- evidenced_compliance_cost_avoided_usd
- evidenced_financing_cost_avoided_usd
- foregone_grant_cash_usd
- net_independence_value_usd
- realized_cash_profit_from_independence_usd

Default current values:
- grant_cash_received_usd = 0 evidenced
- grant_repayment_obligation_usd = 0 evidenced
- realized_cash_profit_from_independence_usd = 0
- net_independence_value_usd = NOT_CALCULABLE
- status = STRATEGIC_INDEPENDENCE_OPTION; NOT_REVENUE; NOT_PROFIT

## Agent instructions
Economic Agent must never report "we earned/saved USD X by not taking a grant" unless it can point to an actual contract, approved offer, expense, royalty obligation, or comparable financing quote and show the counterfactual calculation. It must show both avoided costs and foregone funding. Independence can be strategically valuable without being booked as money.

## Source basis
Israel Innovation Authority official royalties/IP page: https://innovationisrael.org.il/en/royalties-intellectual-property/
The Authority states royalties are generally 3%–5% of annual revenues until the full grant plus applicable interest is repaid, and that transfer of funded know-how outside Israel is subject to approval and repayment rules. The precise Hebrew legal text and the actual program agreement control.
