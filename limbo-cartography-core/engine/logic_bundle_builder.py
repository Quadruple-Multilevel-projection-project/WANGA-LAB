"""Preserve proposed bundles from inbox as draft artifacts; never self-validate as VERIFIED."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "cartography" / "inbox" / "logic_bundles"
OUT = ROOT / "cartography" / "logic_bundles"
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")


def build_bundles() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    existing = {p.stem for p in OUT.glob("*.json")}
    created, rejected = [], []
    for path in sorted(INBOX.glob("*.json")):
        try:
            source = json.loads(path.read_text(encoding="utf-8"))
            bundle_id = source.get("bundle_id")
            if not isinstance(bundle_id, str) or not ID_RE.fullmatch(bundle_id):
                raise ValueError("INVALID_BUNDLE_ID")
            if bundle_id in existing:
                raise ValueError(f"DUPLICATE_BUNDLE_ID:{bundle_id}")
            if not isinstance(source.get("source_refs"), list) or not source["source_refs"]:
                raise ValueError("SOURCE_REFS_REQUIRED")
            if not isinstance(source.get("structure"), dict):
                raise ValueError("STRUCTURE_MUST_BE_OBJECT")
            if source.get("status") == "VERIFIED":
                raise ValueError("INPUT_CANNOT_SELF_DECLARE_VERIFIED")
            canonical = json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
            record = {
                "bundle_id": bundle_id,
                "version": str(source.get("version", "0.1.0")),
                "status": "DRAFT_UNVERIFIED",
                "source_refs": source["source_refs"],
                "structure": source["structure"],
                "source_candidate_sha256": hashlib.sha256(canonical).hexdigest(),
                "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "verification": {"verified": False, "evidence_refs": []},
                "ingested_from": str(path.relative_to(ROOT))
            }
            destination = OUT / f"{bundle_id}.json"
            destination.write_text(json.dumps(record, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
            existing.add(bundle_id)
            created.append({"bundle_id": bundle_id, "path": str(destination.relative_to(ROOT)), "status": record["status"]})
        except Exception as exc:
            rejected.append({"file": path.name, "reason": f"{type(exc).__name__}:{exc}"})
    result = {"status": "FAILED" if rejected else ("BUILT" if created else "NO_INPUTS"),
              "created": created, "rejected": rejected,
              "verified_count": 0}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == "__main__":
    raise SystemExit(1 if build_bundles()["status"] == "FAILED" else 0)
