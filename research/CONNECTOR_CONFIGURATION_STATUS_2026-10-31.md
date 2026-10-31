# Connector Configuration — Verified State
**Snapshot date:** 2026-10-31 09:24 Asia/Jerusalem  
**Status:** PARTIALLY VERIFIED — Google browser authentication is not saved; ProductOS personal-repository discovery requires reconnection.

This is an evidence-bound configuration snapshot. It records the live read-only checks performed on 2026-10-31 and preserves the existing configuration. It does not claim that every connector is fully configured.

## 1. Verified current state

| Component | Live observation on 2026-10-31 | Status |
|---|---|---|
| TinyFish browser profiles | One profile returned: `Default`, ID `prof_42c5b4ae277b4329`, marked default | FOUND |
| TinyFish saved Google sign-in | `signed_in_sites: []` | NOT VERIFIED for Google |
| Google Business Profile | Target URL is known; browser access was not tested because no Google sign-in is saved in the TinyFish profile | BLOCKED ON AUTHENTICATION |
| GitHub authenticated identity | `get_user_login` returned `AmbassadorOv` (GitHub user ID `63800950`) | VERIFIED |
| GitHub personal repositories | Repository listing filtered to owner `AmbassadorOv` returned 38 repositories; private repositories are included | VERIFIED |
| GitHub App installed accounts | `AmbassadorOv` (user), `Quadruple-Multilevel-projection-project` (organization), and `tribal-archery` (organization) | FOUND |
| GitHub App installations | Three installations returned; each reports `repository_selection: all` | FOUND |
| GitHub → WANGA-LAB | `Quadruple-Multilevel-projection-project/WANGA-LAB` metadata read succeeded; `admin`, `maintain`, `pull`, `push`, and `triage` are true; default branch is `main` | VERIFIED |
| ProductOS project access | Three existing projects are listed with `FULL_DEV` access | VERIFIED |
| ProductOS → Jade Mesa repository | `productos-agents/productos-jade-mesa-website-f9c723af`, branch `main`; read and push verified | VERIFIED |
| ProductOS → AI Logic Auditor repository | `productos-agents/productos-ai-logic-auditor-demo-8946d3a4`, branch `main`; read and push verified | VERIFIED |
| ProductOS → Logic Drift Orchestrator repository | `productos-agents/productos-logic-drift-orchestrator-14f43ff2`, branch `main`; read and push verified | VERIFIED |
| ProductOS personal repository discovery | Discovery returned `partial` / `reconnect_required`; one repository was returned. The warning is scoped to personal repository discovery and does not invalidate the three independently verified project bindings | PARTIALLY AVAILABLE |

## 2. Existing identifiers and links

- TinyFish profile: `prof_42c5b4ae277b4329` (`Default`)
- TinyFish setup URL: https://agent.tinyfish.ai/profiles/prof_42c5b4ae277b4329/setup?domain=business.google.com&source=mcp
- Google Business Profile target: https://business.google.com/n/2864137945088385166/profile?authuser=1&fid=17983728887610020501
- GitHub user: https://github.com/AmbassadorOv
- WANGA-LAB: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB
- ProductOS connector settings: /settings/connectors

GitHub App installation IDs returned:
- `108465723` — `AmbassadorOv`
- `90200124` — `Quadruple-Multilevel-projection-project`
- `108442948` — `tribal-archery`

## 3. ProductOS project bindings to preserve

| ProductOS project | Project ID | Bound GitHub repository | Branch | Access |
|---|---|---|---|---|
| Jade Mesa — Website | `f9c723af-6ee5-49cc-bda7-a96a0911b325` | `productos-agents/productos-jade-mesa-website-f9c723af` | `main` | `FULL_DEV`; read/push verified |
| AI Logic Auditor Demo | `8946d3a4-4c84-4a1f-b151-ac267809b82a` | `productos-agents/productos-ai-logic-auditor-demo-8946d3a4` | `main` | `FULL_DEV`; read/push verified |
| Logic Drift Orchestrator | `14f43ff2-c5b5-4e39-9de5-d68f41d5a5ba` | `productos-agents/productos-logic-drift-orchestrator-14f43ff2` | `main` | `FULL_DEV`; read/push verified |

All three ProductOS projects report deployment mode `MANUAL`. A successful GitHub push does not by itself establish that a deployment occurred.

## 4. Configuration sequence

### A. TinyFish / Google Business Profile — blocked pending user sign-in
1. Preserve the existing `Default` profile; do not create a duplicate.
2. The profile listing currently contains no saved sign-in sites. Do not run an authenticated Google browser task yet.
3. The user must open the existing TinyFish setup URL, sign in to the intended Google account in that browser session, and save the session there. Never request a password in chat or store credentials, cookies, or tokens in this repository.
4. Re-list TinyFish profiles and verify that `signed_in_sites` includes `google.com` or another documented Google sign-in domain.
5. Only after that evidence exists, perform a read-only check of the target Business Profile and confirm that the intended business/account is visible.
6. Do not edit Business Profile fields as part of this configuration pass.

### B. GitHub / AmbassadorOv — preserve existing connection
1. Keep the currently authenticated GitHub identity `AmbassadorOv`.
2. Preserve the three existing GitHub App installations and account access.
3. Continue using the verified WANGA-LAB repository access; do not create a duplicate GitHub connection.
4. Recheck repository permissions before any requested write operation.

### C. GitHub → ProductOS — preserve existing project bindings
1. Preserve all three verified project-to-repository bindings listed above.
2. The `reconnect_required` warning applies to personal repository discovery, not to the existing bound repositories.
3. If new personal repositories must be discovered or imported, reconnect the same personal GitHub account through ProductOS connector settings. Do not disturb existing project bindings to resolve a discovery-only warning.
4. Treat deployment as a separate operation; all three projects currently report `MANUAL` deployment mode.

### D. Any additional GitHub target
The current evidence verifies GitHub connector access, GitHub App installations, WANGA-LAB access, and three ProductOS project bindings. It does not identify or verify a different external target system. Do not create another integration until its exact target is identified.

## 5. Acceptance criteria

- **TinyFish:** profile listing shows a saved Google sign-in domain.
- **Google Business Profile:** a read-only browser check reaches the intended business profile and confirms the correct account/business.
- **GitHub:** authenticated login is `AmbassadorOv`; repository listing succeeds; WANGA-LAB metadata/read access succeeds.
- **GitHub App:** installed accounts and installation scope are recorded without assuming that installation alone proves a particular repository's permissions.
- **ProductOS:** each existing project continues to report its bound repository and read/push access.
- **Personal repository discovery:** reconnect only if importing/discovering additional personal repositories is required.
- **Writes:** verify resulting commit/file state after an explicitly requested repository change.
- **Business edits / deployments:** perform only as separate, explicitly intended operations and verify their resulting state.

## 6. Evidence and change log

Read-only checks performed on 2026-10-31:
- TinyFish profile listing.
- GitHub authenticated-user lookup.
- GitHub repository listing filtered to owner `AmbassadorOv`.
- GitHub installed-account and installation listings.
- WANGA-LAB repository metadata lookup.
- ProductOS project listing and metadata checks for all three existing projects.
- ProductOS personal-repository discovery check.
- Existing connector snapshot and prior conversation extraction read from WANGA-LAB.

Changes made during this pass:
- No connector settings changed.
- No browser profile created or modified.
- No Google Business Profile fields edited.
- No ProductOS repository binding changed.
- This dated configuration snapshot is the only planned repository change in this pass.

## 7. Evidence vocabulary

- `VERIFIED` — direct successful test evidence exists.
- `FOUND` — a resource or configuration was located.
- `NOT VERIFIED` — no direct proof of successful operation.
- `BLOCKED` — a prerequisite prevents the test.
- `PARTIALLY AVAILABLE` — a scoped capability is available while another scoped capability is limited.

A failed or incomplete search does not establish non-existence. Do not report a connector setup, profile edit, or deployment as complete without evidence of the saved resulting state.
