# Kubernetes Runbook

**Status: DRAFT — no cluster deployment executed**

1. Confirm the target cluster and namespace with the operator.
2. Review manifests, image digests, resource limits, service exposure, and secret references.
3. Verify the NetworkPolicy in a test namespace; default-deny must be demonstrated, not assumed.
4. Apply manifests using the approved release procedure.
5. Inspect pod readiness, application logs, and rendered application behavior.
6. Capture manifest revision, image digest, timestamps, logs, and screenshots.
7. Test rollback to the previous immutable image/artifact.
8. Record the outcome and unresolved limitations.

**Open prerequisites:** cluster version, ingress design, service ports, image registry, and health probes are not yet source-verified. Do not apply these instructions to production without an approved target-specific change plan.
