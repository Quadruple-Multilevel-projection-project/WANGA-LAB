# ARK Executive Order 005 — Implementation Boundary and Evidence Record

**Status:** implementation scaffold committed to a review branch; production deployment is not asserted.  
**Branch:** `ark/executive-order-005-safe-implementation`

## Verified starting state

- The connected Wix account lists **Logic Engine Research Lab** as published.
- Its currently returned URL is https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/
- The site is editorless and reports the Free plan.
- The current conversation does not contain the three XLSX source workbooks named in the earlier registry mandate. The agent registry therefore cannot be truthfully populated from those missing files.

## Earth Ring — Layer 4 protection

No canonical Layer 4 source, change history, or known-good commit was identified by the reads completed for this task. Consequently, no claim of sabotage, reversion, or restoration is made, and no Layer 4 files are changed by this branch.

Before any restoration, preserve the current state and collect:
1. canonical source path and known-good commit;
2. current branch/commit and diff;
3. the 231 Gates and 230 Crystal Space Points source representation;
4. reproducible tests proving which invariants fail and which pass.

Only a source-backed diff and a passing regression suite can support a restoration claim.

## Fire Ring — agent genesis

`scripts/ark_agent_genesis.py` produces a deterministic **proposal registry** from a source-backed JSON seed. It does not create email accounts, credentials, external agents, or access keys. All proposed entries remain inactive until a human authorizes activation and the runtime's identity, budget, and permission boundaries are configured.

Example:

```bash
python scripts/ark_agent_genesis.py --seed seed_agents.json --out agents_registry_proposal.json
```

Optional child proposals are bounded and opt-in:

```bash
python scripts/ark_agent_genesis.py --seed seed_agents.json --out agents_registry_proposal.json --children-per-agent 2
```

Input contract:

```json
{
  "agents": [
    {
      "agent_id": "L1-001",
      "level": "L1",
      "parent_id": null,
      "source_reference": "path/to/canonical-source.md#section"
    }
  ]
}
```

No source reference, no registry entry. No automatic authority inheritance. No secret material in the registry.

## Water Ring — Wix publication

The site is already reported as published at the URL above. That alone does **not** prove that the nine requested pages have been created or published. This branch does not claim they are live. A page/content inventory and the exact CMS or page-management surface must be identified before making writes, so existing content is not overwritten accidentally.

The requested content topics are:
1. Role Charter
2. Agent Orchestration
3. Export Blueprint
4. First Order of Logic
5. Evidence and Provenance
6. Drift Forensics
7. Verification Gates
8. Registry and Agent Lifecycle
9. Deployment Status and Limitations

The phrase “Sultan's face” does not identify an available approved image asset in the current source set. No face or identity image should be invented or substituted.

## Wind and Void — destructive actions and credentials

This implementation does not revoke keys, delete nodes, purge memory, or create a root email account. Those actions are irreversible or security-sensitive and require an explicit target inventory, authorization, backup/recovery plan, and an appropriate account/provider workflow. Credentials must not be placed in GitHub commits or chat transcripts.

## Required evidence before calling deployment complete

- Source workbooks or an explicitly approved replacement seed.
- Registry generation output and validation tests.
- A before/after Layer 4 diff and invariant test results, if restoration is requested.
- A Wix content inventory, successful publish result, and public URL checks for each page.
- Actual commit SHA(s) and CI result, reported only after the corresponding operations succeed.
