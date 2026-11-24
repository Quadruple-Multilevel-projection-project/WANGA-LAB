"""Fail-closed draft transition helpers for AI231's internal Logic Credit buckets.

This module is not connected to a live ledger or persistence layer. It never
issues internal credits or external tokens.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class LedgerStateTransitionError(ValueError):
    """Raised when an aggregate-state transition lacks required evidence."""


def validate_cash_separation(cash: Mapping[str, Any]) -> None:
    """Validate the cash snapshot and its derived contribution-margin invariant.

    The aggregate schema validates field types and status-dependent nullability.
    This function adds the cross-field invariant that JSON Schema does not
    express here: contribution margin equals cash collected minus cash costs.
    """
    status = cash.get("status")
    currency = cash.get("currency")
    collected = cash.get("actual_cash_collected_minor_units")
    costs = cash.get("actual_cash_costs_paid_minor_units")
    variable_costs = cash.get("actual_variable_cash_costs_paid_minor_units")
    margin = cash.get("contribution_margin_minor_units")

    if status == "NOT_YET_VERIFIED":
        if any(value is not None for value in (currency, collected, costs, variable_costs, margin)):
            raise LedgerStateTransitionError(
                "unverified cash fields must remain null"
            )
        return

    if status != "VERIFIED":
        raise LedgerStateTransitionError("cash status must be VERIFIED or NOT_YET_VERIFIED")

    if not isinstance(currency, str) or len(currency) != 3 or not all("A" <= char <= "Z" for char in currency):
        raise LedgerStateTransitionError("verified cash requires a three-letter uppercase currency code")

    for label, value in (
        ("actual cash collected", collected),
        ("actual cash costs paid", costs),
        ("actual variable cash costs paid", variable_costs),
        ("contribution margin", margin),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise LedgerStateTransitionError(f"verified {label} must be an integer minor-unit amount")

    if collected < 0 or costs < 0 or variable_costs < 0:
        raise LedgerStateTransitionError("verified cash and cost amounts must be non-negative")
    if variable_costs > costs:
        raise LedgerStateTransitionError("actual variable cash costs must not exceed total cash costs paid")

    if margin != collected - variable_costs:
        raise LedgerStateTransitionError(
            "contribution margin must equal actual cash collected minus actual variable cash costs paid"
        )


def apply_event(
    balances: Mapping[str, Any],
    event: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply only proposal/approval bucket movements to a copied state.

    CREDIT_PROPOSED increases planned quantity.
    CREDIT_APPROVED moves quantity from planned to approved only with an
    accepted review and explicit APPROVED authorization.
    Internal issuance and reversal remain blocked until separately specified.
    """
    result = deepcopy(dict(balances))
    event_type = event.get("event_type")
    quantity = event.get("quantity")
    unit = event.get("unit")
    review_status = event.get("review_status")
    authorization = event.get("authorization")
    authorization_state = authorization.get("state") if isinstance(authorization, Mapping) else None

    if isinstance(quantity, bool) or not isinstance(quantity, (int, float)) or quantity <= 0:
        raise LedgerStateTransitionError("quantity must be a positive number")
    if unit != "LOGIC_CREDIT_INTERNAL":
        raise LedgerStateTransitionError("only LOGIC_CREDIT_INTERNAL is supported")
    if result.get("issued_internal_quantity") != 0:
        raise LedgerStateTransitionError("internal issuance is not enabled in state model v1")
    if result.get("external_token_quantity") != 0:
        raise LedgerStateTransitionError("external token quantity must remain zero")

    if event_type == "CREDIT_PROPOSED":
        if review_status != "UNREVIEWED" or authorization_state != "PENDING":
            raise LedgerStateTransitionError(
                "CREDIT_PROPOSED requires UNREVIEWED status and PENDING authorization"
            )
        result["planned_quantity"] = result.get("planned_quantity", 0) + quantity
        return result

    if event_type == "CREDIT_APPROVED":
        if review_status != "ACCEPTED" or authorization_state != "APPROVED":
            raise LedgerStateTransitionError(
                "CREDIT_APPROVED requires ACCEPTED review and APPROVED authorization"
            )
        planned = result.get("planned_quantity", 0)
        if quantity > planned:
            raise LedgerStateTransitionError("approval quantity exceeds planned quantity")
        result["planned_quantity"] = planned - quantity
        result["approved_quantity"] = result.get("approved_quantity", 0) + quantity
        return result

    if event_type in {"CREDIT_ISSUED_INTERNAL", "EXTERNAL_TOKEN_ISSUED"}:
        raise LedgerStateTransitionError(
            "issuance is blocked; no issuance event or authorization contract exists"
        )
    if event_type == "CREDIT_REVERSED":
        raise LedgerStateTransitionError(
            "reversal bucket semantics require a separately reviewed transition contract"
        )
    raise LedgerStateTransitionError(f"unsupported event_type: {event_type}")
