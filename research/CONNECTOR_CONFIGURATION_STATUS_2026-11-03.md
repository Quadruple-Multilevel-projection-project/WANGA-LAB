# Connector Configuration — Live State and Configuration Plan
**Snapshot date:** 2026-11-03  
**Status:** PARTIALLY VERIFIED — GitHub and existing ProductOS bindings are verified; Google browser authentication is not saved; ProductOS personal-repository discovery is limited.

This snapshot records read-only checks performed on 2026-11-03. It preserves the existing connector configuration and does not claim that Google Business Profile access or deployment is complete.

## 1. Live checks

| Component | Live observation on 2026-11-03 | Status |
|---|---|---|
| TinyFish browser profiles | One profile: `Default`, ID `prof_42c5b4ae277b4329`, marked default | FOUND |
| TinyFish saved Google sign-in | `signed_in_sites: []` | NOT VERIFIED for Google |
| Google Business Profile | No authenticated browser test performed because the saved TinyFish profile has no Google sign-in | BLOCKED ON USER SIGN-IN |
| GitHub authenticated identity | Login `AmbassadorOv`, numeric account ID `63800950` | VERIFIED |
| GitHub accessible repositories | 63 returned: 38 under `AmbassadorOv`, 16 under `Quadruple-Multilevel-projection-project`, 9 under `tribal-archery` | VERIFIED for returned listing |
| GitHub App installations | Three installations: `AmbassadorOv` (108465723), `Quadruple-Multilevel-projection-project` (90200124), and `tribal-archery` (108442948); all report `repository_selection: all` | FOUND |
| GitHub → WANGA-LAB | Repository metadata read succeeded; `admin`, `maintain`, `pull`, `push`, and `triage` are true; default branch `main` | VERIFIED |
| ProductOS projects | Three existing projects; each reports `FULL_DEV` access | VERIFIED |
| ProductOS personal repository discovery | `partial` / `reconnect_required`; warning scope is `personal_repository_discovery`; one bound repository was returned with read/push access | PARTIALLY AVAILABLE |

## 2. Existing identifiers and links

- TinyFish profile: `prof_42c5b4ae277b4329` (`Default`)
- Existing TinyFish setup URL: https://agent.tinyfish.ai/profiles/prof_42c5b4ae277b4329/setup?domain=business.google.com&source=mcp
- Google Business Profile target: https://business.google.com/n/2864137945088385166/profile?authuser=1&fid=17983728887610020501
- GitHub user: https://github.com/AmbassadorOv
- WANGA-LAB: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB
- ProductOS connector settings path: `/settings/connectors`

## 3. ProductOS project bindings to preserve

| ProductOS project | Project ID | Bound GitHub repository | Branch | Access |
|---|---|---|---|---|
| Jade Mesa — Website | `f9c723af-6ee5-49cc-bda7-a96a0911b325` | `productos-agents/productos-jade-mesa-website-f9c723af` | `main` | `FULL_DEV`; read/push verified |
| AI Logic Auditor Demo | `8946d3a4-4c84-4a1f-b151-ac267809b82a` | `productos-agents/productos-ai-logic-auditor-demo-8946d3a4` | `main` | `FULL_DEV`; read/push verified |
| Logic Drift Orchestrator | `14f43ff2-c5b5-4e39-9de5-d68f41d5a5ba` | `productos-agents/productos-logic-drift-orchestrator-14f43ff2` | `main` | `FULL_DEV`; read/push verified |

All three projects report deployment mode `MANUAL`. GitHub push permission does not establish deployment success. Jade Mesa and AI Logic Auditor Demo report stage `DEVELOP`; Logic Drift Orchestrator reports `IDEATE`.

## 4. Configuration plan and safeguards

### A. TinyFish / Google Business Profile
1. Preserve the existing `Default` profile; do not create a duplicate.
2. The live profile listing still reports no saved sign-in sites.
3. Do not start an authenticated Google browser task until the user explicitly authorizes the sign-in setup and saves the session in the existing profile.
4. Never request a password in chat or store credentials, cookies, or tokens in this repository.
5. After the user saves the session, re-list profiles and verify that `signed_in_sites` includes `google.com` or another documented Google sign-in domain.
6. Only then perform a read-only check of the target Business Profile and confirm the intended account/business.
7. Do not edit Business Profile fields during this configuration pass.

### B. GitHub / AmbassadorOv
1. Preserve the authenticated identity `AmbassadorOv`.
2. Preserve the three existing GitHub App installations.
3. Continue using the verified WANGA-LAB access; do not create a duplicate GitHub connection.
4. Recheck target repository permissions before any requested write operation.

### C. GitHub → ProductOS
1. Preserve all three existing project-to-repository bindings listed above.
2. The `reconnect_required` warning applies to personal repository discovery only; it does not invalidate the existing project bindings.
3. If additional personal repositories must be discovered or imported, reconnect the same personal GitHub account through ProductOS connector settings. Do not disturb existing project bindings to resolve a discovery-only warning.
4. Treat deployment as a separate operation; all three projects report `MANUAL` deployment mode.

### D. Additional GitHub target
The current evidence verifies GitHub connector access, GitHub App installations, WANGA-LAB access, and three ProductOS project bindings. No separate external target system beyond ProductOS was identified or verified. Do not create another integration until its exact target is identified.

## 5. Acceptance criteria

- **TinyFish:** profile listing shows a saved Google sign-in domain after the user completes setup.
- **Google Business Profile:** a read-only browser check reaches the intended business profile and confirms the correct account/business.
- **GitHub:** authenticated identity is `AmbassadorOv`; repository listing succeeds; WANGA-LAB metadata and permissions are readable.
- **GitHub App:** installations and repository-selection scope are recorded without treating installation alone as proof of repository access.
- **ProductOS:** each existing project continues to report its bound repository and read/push access.
- **Personal repository discovery:** reconnect only if discovering or importing additional personal repositories is required.
- **Writes, Business Profile edits, and deployments:** perform only as separate, explicitly intended operations and verify resulting state.

## 6. Evidence and change log

Read-only checks performed on 2026-11-03:
- TinyFish profile listing.
- GitHub authenticated login and profile lookup.
- GitHub repository listing (63 repositories across three owners).
- GitHub App installation listing.
- WANGA-LAB repository metadata and permission lookup.
- ProductOS project listing and metadata checks for all three existing projects.
- ProductOS personal-repository discovery check.
- Previous connector configuration snapshot read from WANGA-LAB.

Changes made during this pass:
- No connector settings changed.
- No browser profile created or modified.
- No Google Business Profile fields edited.
- No ProductOS repository binding changed.
- No deployment triggered.
- This dated configuration snapshot is the only repository change in this pass.

## 7. Evidence vocabulary

- `VERIFIED` — direct successful test evidence exists.
- `FOUND` — a resource or configuration was located.
- `NOT VERIFIED` — no direct proof of successful operation.
- `BLOCKED` — a prerequisite prevents the test.
- `PARTIALLY AVAILABLE` — a scoped capability is available while another scoped capability is limited.

A failed or incomplete search does not establish non-existence. Do not report connector setup, profile edits, or deployment as complete without evidence of the saved resulting state.
