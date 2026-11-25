# Git Credential Manager and Umbrella Credential Coordination

Status: PREPARED SPECIFICATION — NOT A CONNECTED CREDENTIAL
Configuration: `config/security/credential-coordination.v1.json`
Master hierarchy: `config/umbrella/global-institute-of-neuronics.v1.json`

## 1. What the two upstream pull requests provide

- [GCM PR #2492 — Add cross-platform locking primitives](https://github.com/git-ecosystem/git-credential-manager/pull/2492) introduces injectable `ILock` / `ILockFactory` abstractions and a file-backed `CurrentUser` lock. Ownership follows the exclusive file handle, not a PID check or pathname. It supports no-wait, finite-timeout and cancellation-aware acquisition, jittered contention retries and non-destructive diagnostics. It explicitly does **not** integrate the lock into provider authentication or change provider authentication behaviour.
- [GCM PR #2500 — OAuth token exchange grant](https://github.com/git-ecosystem/git-credential-manager/pull/2500) adds OAuth 2.0 Token Exchange (RFC 8693) to the shared OAuth client. It is a token exchange capability, not a lock, and does not provide cross-machine coordination.

As checked on 2026-11-20, both PRs were open and not merged. The configuration therefore records them as upstream dependencies, not shipped GCM capabilities.

## 2. Two different credential planes

### Local Git operations: Git Credential Manager

Install GCM for the developer workstation and configure Git to invoke it:

```bash
git config --global credential.helper manager
git config --global credential.interactive auto
git ls-remote https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB.git
```

The first HTTPS operation should initiate the provider's normal sign-in flow when no usable credential is cached. GCM stores the resulting credential through the operating system's supported secure credential store. Do not use Git's plaintext `credential.helper store`, do not put a token in the remote URL, and do not run commands that print credential contents.

This local GCM credential is distinct from an AppDeploy backend secret. The browser application cannot inspect the workstation's keychain or local GCM lock files.

### Cloud application operations: AppDeploy Secret Vault

The Logic Factory Hub needs its own server-side credential if it is to call GitHub's API directly. The prepared secret reference is:

- Name: `GITHUB_FINE_GRAINED_TOKEN`
- Scope: the WANGA-LAB repository only
- Initial permissions: repository metadata read, contents read, pull requests read only. Request write permissions only with a separately approved, implemented write workflow.
- Not requested: organization administration, repository administration, or workflow write

The secret must be entered through AppDeploy's secure secret-entry flow and read only by backend code via `secrets.readSecret`. The UI may display whether the secret is configured, but never its value. This token is not copied into GCM, Git configuration, a lock file, a checked-in configuration file, a browser bundle, or logs.

For a production institutional deployment, prefer a GitHub App installation token with a short lifetime over a long-lived personal token. The current prepared field is a fine-grained-token bootstrap only; its initial scope is read-only and it is not yet connected or tested. A later write workflow must request explicit scope expansion.

## 3. Concurrency model

### Local machine

The GCM model is explicitly `LockScope.CurrentUser`. The protected critical sections are authentication prompt initiation, refresh-token rotation, OAuth token exchange and GitHub App installation-token minting.

- Use a stable lock name containing provider, host, a non-reversible account fingerprint and operation.
- Never include a token, password, private key, raw email address or Authorization header in a lock name or lock file.
- Prefer a 10-second bounded acquisition for interactive authentication, cancellation-aware waits and jittered retries.
- Always release/dispose even when the protected operation throws.
- Diagnostics inspect orphaned or malformed metadata; they do not delete it automatically.
- This lock does not coordinate different OS user accounts, other machines, or cloud workers.

### Cloud / serverless workers

Do **not** reuse a local file lock as a distributed lock. AppDeploy workers may run in different processes or instances and do not share a reliable local filesystem lock namespace.

The cloud adapter is marked `NOT_IMPLEMENTED`. It requires a shared transactional store with atomic lease acquisition, expiry/renewal and fencing tokens (or an equivalent Redis primitive). A lease without fencing is insufficient to prevent a stale worker from writing after its lease expired. The adapter must be tested with parallel workers before the system reports it as ready.

## 4. Institutional configuration inheritance

The policy is deny-by-default and narrows down the hierarchy:

1. Umbrella policy: identity boundaries and root deny rules.
2. Institute policy: approved shared providers and credential lifecycle.
3. Body policy: analytics may read and publish approved analysis artifacts; logistics may orchestrate already-approved operations; algorithmics may propose and validate configuration but cannot bypass approval.
4. Organization policy: explicit grants; no organization silently inherits another organization's credentials.
5. Application policy: app-scoped secret references and provider permissions.
6. Agent policy: no persistent personal token; one-task or short-lived token, limited to repository and operation.

The OR oversight committee is independent and read-only. It may inspect audit metadata and recommend a hold; it cannot read raw secret values, write credentials or approve its own audit target.

## 5. OAuth token exchange

RFC 8693 exchange remains disabled until the upstream capability is merged, the target provider supports the exchange, and an explicit audience, issued-token type and scope policy is configured. Subject tokens must never enter logs or lock metadata. An exchanged token is short-lived and task-scoped.

## 6. Readiness gates

The system must not claim credential integration until all required checks are complete:

- GCM is installed and tested on the actual workstation.
- The relevant upstream GCM feature is available or an equivalent implementation is selected.
- AppDeploy secret presence is confirmed without reading the value into the UI.
- The cloud distributed lock adapter is implemented and contention-tested.
- A GitHub API read/write round-trip has succeeded against WANGA-LAB using the scoped credential.
- Rotation, revocation, cancellation, timeout and parallel-agent tests pass.

Until then the status is `PREPARED_NOT_CONNECTED`. Agent dispatch remains subject to the separate introduction-diagram approval gate.
