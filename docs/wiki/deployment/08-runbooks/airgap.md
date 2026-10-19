# Airgap Runbook

**Status: DRAFT — offline installation not proven**

1. Produce a release bundle from a recorded source commit.
2. Include all required runtime dependencies in the bundle or a separately hashed dependency archive.
3. Generate and verify SHA-256 checksums before transfer.
4. Transfer the bundle through the approved offline process.
5. Disconnect the target from network access.
6. Verify checksums and signature using locally available trusted verification material.
7. Install and start the service without network access.
8. Run health and browser-render checks; collect logs and screenshots.
9. Record the exact commands, target image/OS, bundle hash, signature result, and timestamp.

Pass criterion: a clean install and smoke test succeed while network access is unavailable. A checksum-only check does not prove that runtime dependencies are fully bundled.
