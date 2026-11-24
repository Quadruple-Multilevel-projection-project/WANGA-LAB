# Deployment Export Contract

**Status:** SPECIFIED; artifact release remains blocked until the required checks pass.

## Inputs
- Exact Git commit SHA.
- HTTPS repository origin.
- Semantic version.
- Clean source worktree.
- Approved Cosign key path provided as `COSIGN_KEY`.

## Artifact contract
The archive must contain committed source only, a JSON manifest conforming to `manifest.schema.json`, SPDX SBOM, provenance record, and SHA-256 inventory. Signature and archive digest are sidecars.

## Reject conditions
Reject invalid version, dirty source, missing origin/toolchain/signing-key path, prohibited secret/key/customer-data paths, secret scan findings, schema validation failure, or signature failure. Do not print or package secret values.

## Status contract
Exported manifest status defaults to `PROPOSED`. Status promotion requires independent, linked evidence. A signature proves that a key signed a particular artifact; it does not prove the artifact is correct or safe.

## Required tests
- Neural proposal cannot override the formal decision.
- Missing/unresolved source reference produces `REQUIRES_REVIEW`.
- Unknown formal decision fails closed.
- Export validation rejects malformed manifests and secret-bearing paths.
- Air-gap, rollback, Compose, and Kubernetes checks are separate release gates and must not be inferred from a successful packaging run.
