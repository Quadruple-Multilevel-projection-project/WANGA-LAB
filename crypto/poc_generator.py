"""Deterministic structural digest generation.

CCH is an integrity digest, not a proof of truth. Verification must separately
establish provenance, reproducibility, and the validity of the underlying
claims.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


def canonical_json(payload: Mapping[str, Any]) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def generate_cch(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload)).hexdigest()
