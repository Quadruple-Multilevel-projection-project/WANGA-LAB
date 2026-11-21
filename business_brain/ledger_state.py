"""Fail-closed draft transition helpers for AI231's internal Logic Credit buckets.

This module is not connected to a live ledger or persistence layer. It never
issues internal credits or external tokens.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class LedgerStateTransitionError(ValueError):
    """Raised when an aggregate-state transition lacks required evidence."""


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
