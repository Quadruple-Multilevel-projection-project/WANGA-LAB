# 02 — Export Contract

**Status: SPECIFICATION DRAFT — implementation not yet verified**

## Intended bundle contents

A release bundle is expected to contain:

- `manifest.json`
- `README.md`
- `SHA256SUMS`
- `provenance.jsonl`
- software bill of materials (SBOM)
- signature and verification instructions
- configs and schemas
- source/runtime assets needed for the declared deployment mode
- `deploy/` definitions
- `artifacts/visuals/`
- tests and smoke-test evidence

Never export secrets, private keys, `.env` files, uploads, or customer data.

## Required manifest fields

The final JSON Schema must define at minimum: bundle identity and version, source repository and commit SHA, build timestamp, declared maturity/status, file inventory with SHA-256 hashes, schema versions, SBOM reference, provenance reference, signature metadata, deployment targets, and test-evidence references.

Exact field names and constraints must be frozen in `manifest.schema.json` before implementation. This page is not itself the machine-readable contract.

## Export process

1. Confirm source commit and clean-tree/lockfile state.
2. Assemble only allowlisted files.
3. Reject secrets and disallowed paths.
4. Generate file hashes and SBOM.
5. Generate provenance records with source commit, operation, timestamp, and artifact hashes.
6. Validate the manifest and bundle contents.
7. Sign the bundle and verify the signature.
8. Run offline integrity verification.
9. Publish with immutable retention only after gates pass.

## Required files still to implement

- `scripts/export.sh`
- `manifest.schema.json`

Their absence on the inspected `main` branch was previously confirmed. This page does not claim they exist on the documentation branch.
