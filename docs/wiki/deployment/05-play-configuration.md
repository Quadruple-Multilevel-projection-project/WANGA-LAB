# 05 — Play Configuration

**Status: PROPOSED / COMPILER NOT IMPLEMENTED**

Each resolved gate-pair may compile into a package that feeds the 3D visualization, Wix demo page, and other play surfaces. One package should have multiple read-only renderers; renderers must not alter source evidence.

## Proposed package shape

```json
{
  "package_id": "PC-<gate>-<pair>",
  "source": {
    "gate": 14,
    "sentence_id": "<source sentence ID>",
    "ruleset": "gate14.v1"
  },
  "rule": "<explicit, testable rule>",
  "evidence_ref": "sha256:<digest>",
  "play": {
    "board": "36-subspace plaza",
    "nodes": ["<node-a>", "<node-b>"],
    "win_condition": "rule satisfied AND evidence present",
    "fail_condition": "contradiction OR missing evidence"
  },
  "status": "PROPOSED"
}
```

This is a proposed interface example, not a valid package instance. The placeholder IDs, evidence digest, and rule are not real source data.

## Release constraints

- Every rule cites a source sentence ID.
- Every shipped package has an evidence reference that resolves to an inspectable artifact.
- A missing or invalid evidence reference blocks release.
- Ambiguous interpretation yields `REQUIRES_REVIEW`.
- Package compilation must be deterministic and tested.
- Visual output is generated from package data; no hand-edited coordinates.
