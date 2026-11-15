"""Verify an AI231 Logic Contribution Ledger hash chain (stdlib only)."""
from __future__ import annotations
import hashlib
import hmac
import json
from typing import Iterable, Mapping, Any


class LedgerVerificationError(ValueError):
    pass


def canonical_event_digest(event: Mapping[str, Any]) -> str:
    payload = {key: value for key, value in event.items() if key != "event_sha256"}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def verify_chain(events: Iterable[Mapping[str, Any]]) -> str | None:
    seen: set[str] = set()
    previous_digest: str | None = None
    count = 0
    for index, event in enumerate(events):
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            raise LedgerVerificationError(f"event {index}: missing event_id")
        if event_id in seen:
            raise LedgerVerificationError(f"event {index}: duplicate event_id {event_id}")
        seen.add(event_id)
        if event.get("previous_event_sha256") != previous_digest:
            raise LedgerVerificationError(f"event {index}: broken previous_event_sha256 link")
        supplied = event.get("event_sha256")
        if not isinstance(supplied, str) or len(supplied) != 64:
            raise LedgerVerificationError(f"event {index}: invalid event_sha256")
        actual = canonical_event_digest(event)
        if not hmac.compare_digest(supplied, actual):
            raise LedgerVerificationError(f"event {index}: event_sha256 mismatch")
        previous_digest = actual
        count += 1
    if count == 0:
        raise LedgerVerificationError("ledger is empty")
    return previous_digest
