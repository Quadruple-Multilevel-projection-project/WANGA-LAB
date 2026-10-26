# Connector Configuration — Verified State (Snapshot 2026-10-26)
**Snapshot date:** 2026-10-26  
**Status:** PARTIALLY VERIFIED — Google browser authentication remains unverified.

This is an evidence-bound configuration snapshot, not a claim that every connector is fully configured.

## 1. Current state

| Component | Observed state | Status |
|---|---|---|
| TinyFish Browser Context Profile | Existing profile `Default`, ID `prof_42c5b4ae277b4329`; marked default | FOUND |
| TinyFish saved sign-in | `signed_in_sites: []` in the latest profile listing | NOT CONNECTED / NOT VERIFIED for Google |
| Google Business Profile | Target URL is known, but saved Google authentication and profile access have not been verified | BLOCKED ON AUTHENTICATION |
| GitHub connector | Repository-list and repository-read calls succeeded for the connected GitHub integration | CONNECTOR ACCESS VERIFIED |
| GitHub → WANGA-LAB | `Quadruple-Multilevel-projection-project/WANGA-LAB` was readable; repository metadata reports `admin`, `maintain`, `pull`, `push`, and `triage` permissions | ACCESS VERIFIED |
| Existing conversation extraction | `research/CONVERSATION_EXTRACTION_2026-10-08.md` exists and contains the prior connector plan | FOUND |

**Boundary:** Successful GitHub connector calls prove access through this connected environment. They do not prove that a separate external integration, webhook, deployment, or automation is configured.

## 2. Existing configuration references

- TinyFish profile: https://agent.tinyfish.ai/profiles/prof_42c5b4ae277b4329
- Existing-profile setup for Google Business Profile: https://agent.tinyfish.ai/profiles/prof_42c5b4ae277b4329/setup?domain=business.google.com&source=mcp
- Google Business Profile target: https://business.google.com/n/2864137945088385166/profile?authuser=1&fid=17983728887610020501
- GitHub account: https://github.com/AmbassadorOv
- WANGA-LAB repository: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB
- Prior extraction: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/CONVERSATION_EXTRACTION_2026-10-08.md

## 3. Configuration sequence

### Step A — Google authentication (blocked until manual sign-in is saved)
1. Open the existing TinyFish profile setup URL above.
2. Sign in to the intended Google account in the browser session and use the page's save action.
3. Re-run the TinyFish profile listing.
4. Verify that `signed_in_sites` includes `google.com` or another documented Google sign-in domain.
5. Only then run a read-only browser check against the target Business Profile and confirm the correct business/account is visible.
6. Do not edit the business profile until access is verified and the intended changes are reviewed.

Do not create a duplicate browser profile unless the existing one is unsuitable. Never store passwords, session cookies, or access tokens in this repository.

### Step B — GitHub connector
1. Preserve the current working connector.
2. Recheck repository listing and WANGA-LAB read access when needed.
3. Before any external integration is added, identify the exact target system and its existing connection state.
4. Do not create duplicate connections or claim an external integration is active without a successful test.

### Step C — Acceptance criteria
- **TinyFish:** saved Google sign-in is visible in the profile listing.
- **Google Business Profile:** read-only browser check reaches the intended business profile without being redirected to sign-in.
- **GitHub:** repository listing and WANGA-LAB read are successful.
- **GitHub write path:** use only when an explicitly requested change is needed; confirm the resulting commit or file state.
- **External GitHub integration:** document as NOT VERIFIED until the actual target system is identified and tested.

## 4. Evidence rules

Use only these state labels:
- `VERIFIED` — direct successful test evidence exists.
- `FOUND` — a resource or configuration was located.
- `NOT VERIFIED` — no direct proof of successful operation.
- `BLOCKED` — a prerequisite prevents the test.
- `NOT FOUND IN PERFORMED SEARCH` — a scoped search did not locate an item; this does not prove non-existence.

Do not report a profile update or connector setup as complete without evidence of the saved state.

## 5. Snapshot findings

- TinyFish profile listing was successful, and `signed_in_sites` was empty.
- GitHub repository listing and WANGA-LAB metadata/file reads succeeded.
- A search for connector-configuration references surfaced the prior conversation extraction but did not surface a dedicated configuration document before this file was created. This is not proof that no other configuration exists.
- No Google Business Profile fields were changed in this configuration pass.


## 6. Recheck on 2026-10-26

Direct checks repeated on 2026-10-26:

- **TinyFish:** profile listing succeeded. The only returned profile is `Default`, ID `prof_42c5b4ae277b4329`; `signed_in_sites` remains empty. Google sign-in is therefore still NOT VERIFIED.
- **GitHub / AmbassadorOv:** the connected GitHub connector returned 37 repositories for owner `AmbassadorOv`. The user namespace does not contain `AmbassadorOv/WANGA-LAB` in that returned list; the target WANGA-LAB repository is under the organization `Quadruple-Multilevel-projection-project`.
- **WANGA-LAB:** repository metadata and the existing connector-status file were read successfully. The repository reports `admin`, `maintain`, `pull`, `push`, and `triage` permissions for the connected GitHub integration.
- **GitHub integration into any separate external system:** NOT VERIFIED. The target external system has not been identified in the available configuration, so no separate connection was created or assumed.
- **Changes:** no Google Business Profile fields were edited, and no new connector or browser profile was created.

### Next required input/action

Complete Google sign-in manually in the existing TinyFish profile setup page, save the browser state there, and then repeat the profile-list check. Proceed to a read-only Business Profile access test only after the profile listing records a Google sign-in domain.
