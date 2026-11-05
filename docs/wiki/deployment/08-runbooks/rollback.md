# Rollback Runbook

**Status: DRAFT — rollback not rehearsed**

1. Identify the current release ID and last known-good signed bundle.
2. Confirm the previous bundle's signature and checksums.
3. Stop promotion and record the incident/release reason.
4. Redeploy the previous immutable artifact using the target-specific procedure.
5. Verify readiness and inspect the rendered application.
6. Confirm data/schema compatibility and ensure rollback did not overwrite evidence.
7. Record start/end timestamps, release IDs, hashes, smoke results, and operator decision.
8. Reopen promotion only after the DSA records the gate verdict.

The proposed acceptance target is rollback within one release cycle. The cycle duration must be explicitly defined and measured before the target can be evaluated.
