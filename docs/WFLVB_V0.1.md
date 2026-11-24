# WANGA Formal Logic Verification Bridge (WFLVB) V0.1

Status: implementation prototype; not production-certified.

## Trust boundaries
1. WANGA supplies source-backed nodes and relations.
2. The bridge validates structure and provenance.
3. A relation becomes a proof obligation only when an explicit formal statement is supplied.
4. Human approval is required before a specification hash is treated as approved.
5. Lean checks the supplied Lean file only; it does not establish that the source interpretation is true.
6. Lean execution is gated by exact equality with the approved specification hash.

## API
- structure_to_specification(data): deterministic canonical specification and SHA-256.
- review_specification(spec): unresolved-item review; a well-formed spec remains REVIEW pending human approval.
- generate_proof_obligations(spec): only explicit formal statements become obligations.
- compare_approved_specification(current, approved_hash): exact-hash gate.
- verify_with_lean(file, current_hash, approved_hash): invokes installed Lean without rewriting proofs.
- reconstruct_and_audit(spec, original): recompiles and compares hashes.

## Deliberate non-features
- No automatic interpretation of Kabbalistic symbols, Hebrew letters, Sefirot, 231 gates, or Reshimu.
- Graph membership does not establish semantic meaning.
- No automatic specification approval.
- No network access or autonomous deployment.

## Tests
Run: python -m unittest discover -s tests -v

Lean integration requires Lean installed and a reviewed .lean file corresponding to the approved specification. Missing Lean, file, or approval hash returns BLOCKED.
