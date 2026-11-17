"""Reference signer for Map Link Provenance action tuples."""
from __future__ import annotations
import hashlib
from datetime import datetime


def sign_action(timestamp: str, contract_start_time: str, action_id: str) -> str:
    """Return SHA-256 of the exact canonical action tuple.

    Timestamps must be ISO-8601 strings including an explicit UTC offset.
    This signature binds the tuple; it is not a digital identity signature.
    """
    if not timestamp or not contract_start_time or not action_id:
        raise ValueError("BLOCKED_SIGNATURE: timestamp, contract_start_time and action_id are required")
    for value in (timestamp, contract_start_time):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("BLOCKED_SIGNATURE: timestamp must include timezone")
    canonical = (
        f"Timestamp={timestamp}|Contract_Start_Time={contract_start_time}|Action_ID={action_id}"
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--contract-start-time", required=True)
    parser.add_argument("--action-id", required=True)
    args = parser.parse_args()
    print(sign_action(args.timestamp, args.contract_start_time, args.action_id))
