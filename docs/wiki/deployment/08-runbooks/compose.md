# Compose Runbook

**Status: DRAFT — no deployment executed**

1. Verify the intended source commit and lockfile state.
2. Build the production artifact using the repository's documented build command.
3. Validate environment configuration without printing secret values.
4. Start the Compose stack using the checked-in configuration.
5. Confirm health checks and inspect the rendered application in a browser; HTTP 200 alone is insufficient.
6. Capture timestamped logs and screenshots; record artifact and commit hashes.
7. Exercise the documented stop/restart procedure.
8. Do not mark TESTED until the commands, environment, outputs, and inspection evidence are attached to the release record.

**Open prerequisites:** actual Compose file path, service names, health endpoints, and supported runtime are not yet verified in this runbook.
