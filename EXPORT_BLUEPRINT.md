# Export Blueprint v1.0

**Status:** SPECIFIED — implementation and release gates require fresh CI evidence.  
**Scope:** Reproducible, secret-screened source export from a clean Git commit. This blueprint does not authorize deployment.

## Inputs and invariants

- A clean Git worktree and a committed source revision.
- A semantic version in `MAJOR.MINOR.PATCH` form, optionally followed by prerelease/build metadata.
- Required tools: `git`, `python3`, `syft`, `gitleaks`, `cosign`, `tar`, and `sha256sum`.
- An approved signing key is supplied through `COSIGN_KEY`; key contents must never be printed or included in the bundle.
- Export is fail-closed: missing prerequisites, dirty source, missing origin, invalid version, prohibited paths, or secret-scan findings stop the operation.

## Export sequence

1. **G1 — Input contract:** validate argument count and semantic version.
2. **G2 — Toolchain:** verify required executables and signing-key path are present.
3. **G3 — Source integrity:** require a clean worktree; record the exact commit and HTTPS origin.
4. **G4 — Isolation:** stage only the committed tree via `git archive`; do not package untracked workspace content.
5. **G5 — Sensitive-data exclusion:** reject prohibited secret/key/customer-data paths and scan staged contents with Gitleaks.
6. **G6 — Inventory:** generate an SPDX JSON SBOM with Syft; this is inventory, not a vulnerability verdict.
7. **G7 — Manifest and integrity:** write provenance, generate SHA-256 inventory, and validate the manifest against `manifest.schema.json`.
8. **G8 — Package and signature:** create the archive, sign the exact archive with Cosign, and emit a separate SHA-256 file. A generated bundle remains `PROPOSED` until independent release checks pass.

## Required outputs

- `wanga-deployment-<version>.tar.gz`
- `wanga-deployment-<version>.tar.gz.sig`
- `wanga-deployment-<version>.tar.gz.sha256`
- Inside the archive: `manifest.json`, `provenance.jsonl`, `SBOM.spdx.json`, and `SHA256SUMS`.

## Explicit non-claims

A successful export alone does not prove runtime correctness, vulnerability absence, air-gap operation, Compose/Kubernetes deployment, rollback, or end-to-end provenance. Those require separate evidence. No output may be labelled `VERIFIED` without an inspectable test/evidence reference. The current exporter must be checked against every gate above; documented gates are not evidence that each is already implemented.
