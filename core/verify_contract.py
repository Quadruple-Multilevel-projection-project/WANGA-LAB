#!/usr/bin/env python3
"""Structural verifier. PASS means schema/count integrity only, not source truth."""
import csv, pathlib, sys
p=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "data/matrix_2450.csv")
with p.open(encoding="utf-8-sig",newline="") as f: rows=list(csv.DictReader(f))
ids=[r["unit_id"] for r in rows]
assert len(rows)==2450, f"expected 2450 rows, got {len(rows)}"
assert len(set(ids))==2450, "duplicate unit_id"
assert all(r["status"]=="null" for r in rows), "initial statuses must remain null"
assert all(r["five_matters"]=="FIVE_MATTERS_UNSPECIFIED" for r in rows), "five matters changed"
assert all(r[k]=="" for r in rows for k in ["I1_raw","I2_raw","I3_raw","I4_raw","source_uri","locator","method","version","source_sha256","replay_hash"]), "initial evidence fields must remain empty"
print("PASS: 2450 unique units; initial evidence null; FIVE_MATTERS_UNSPECIFIED preserved.")
