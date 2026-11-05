# Contract Library — WANGA-LAB / PCE

**Registry status:** CREATED AS A SOURCE INDEX; not a contract signature or verification receipt.  
**Rule:** Never reconstruct or silently replace an authoritative contract from a summary. Preserve original source links and record missing artifacts as blocked.

## Dedicated contract portal

- [PCE Contract Registry website](https://pce-contract-registry-5dlcky.v2.appdeploy.ai/) — deployed source-linked portal; deployment status `ready` with no reported frontend/backend errors.

## Governing baseline

- [WANGA MASTER CONTRACT v1.0](../WANGA_MASTER_CONTRACT_v1.0.md) — existing master governance contract. It states the source-to-weights order, provenance/lineage requirements, drift handling, verification vocabulary, and that weights remain forbidden until required logic and verification gates pass.
- [PCE SYSTEM FINAL NOTICE v1.0](../PCE_SYSTEM_FINAL_NOTICE_v1.0.md) — references the required `PCE-CONTRACT-v1.3-SEALED` tag and execution prerequisites.
- [PCE SYSTEM CONTRACT BREACH NOTICE v1.0](../PCE_SYSTEM_CONTRACT_BREACH_NOTICE_v1.0.md) — explicitly requires annotated tag creation, running `python core/verify_contract.py`, and pushing the tag.

## Execution evidence

- [GitHub Actions run 39736408353](https://github.com/Quadruple-Multilevel-projection-project/AI231.meta.io/actions/runs/39736408353) — linked run; its jobs/evidence have not been confirmed by this registry write.
- Required evidence before reporting PCE v1.3 as sealed and verified:
  1. Exact repository and commit identified.
  2. Annotated tag `PCE-CONTRACT-v1.3-SEALED` exists and points to the inspected commit.
  3. `python core/verify_contract.py` was actually run and output is `PASS`.
  4. Tag push output is captured and the remote tag target is confirmed.

## Missing canonical artifact

The exact full text of the PCE v1.3 machine-readable contract (`contract_v1.3.json`) and its verifier implementation were not located in the repository search performed for this registry. They are therefore **NOT REPRODUCED HERE**. Do not treat this index or the existing notices as a substitute for that artifact. Add the canonical file only from its exact authorized source, with its original bytes/content and provenance.

## Integration policy

- All consuming projects should link to this registry and the governing baseline.
- A source link or GitHub commit is not proof of execution, contract sealing, or deployment.
- Do not create numeric weights or invent contract fields.
- Keep extraction, derivation, verification, implementation, and deployment states distinct.
- Missing required evidence blocks dependent actions.
- Writes, pushes, plugin publication, and deployment remain approval-gated.
