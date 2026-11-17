# Map Link Provenance

**Project type:** bilateral event-provenance protocol for links and connections exchanged between map / graph systems.  
**Project home:** AI231 / WANGA-LAB  
**Current state:** SPECIFIED + PLUGIN_PACKAGE_CREATED + FIGJAM_DIAGRAM_ADDED + WIX_SITE_PUBLISHED

## Purpose

Map Link Provenance records the complete handoff of a connection from a source map to a destination map. It distinguishes creation, source approval, dispatch, destination receipt, destination approval, durable ingestion, return acknowledgement, and source-side recording of that acknowledgement.

The central rule is simple: **sent is not received; received is not approved; approved is not durably ingested; ingested is not bilaterally verified until both sides can be read back.**

The protocol records transport and acceptance provenance. It does not merge maps, change the semantic meaning of an edge, or establish that the content of a link is true.

## Eight-event lifecycle

1. SOURCE_CREATED
2. SOURCE_APPROVED
3. DISPATCHED
4. DESTINATION_RECEIVED
5. DESTINATION_APPROVED
6. DESTINATION_INGESTED
7. ACK_RETURNED
8. SOURCE_ACK_RECORDED

Every consequential action requires its own unique Action_ID, exact ISO-8601 timestamp with timezone, Contract_Start_Time, and SHA-256 signature over the canonical string:

    Timestamp=<Timestamp>|Contract_Start_Time=<Contract_Start_Time>|Action_ID=<Action_ID>

The SHA-256 value binds that tuple. It is **not** a digital identity signature and does not independently prove that an external system performed or persisted an event.

## Bilateral record model

The source and destination each retain a record with the same immutable transfer_id, endpoint identifiers, event sequence, and relevant event hashes.

- **Source record:** source map/version/node/edge, destination map, source creation/approval/dispatch times, destination receipt hash, returned acknowledgement, source acknowledgement time, previous/current event hashes.
- **Destination record:** the same transfer ID and source identifiers, destination map/version/node/edge, received/approved/ingested times, durable record ID, source receipt hash, destination signature, acknowledgement delivery state.

The destination must return a durable record/node/edge identifier for ingestion. The source must record the returned receipt. Both records must be read back and compared.

## Acceptance gate

A transfer may be labelled BILATERAL_VERIFIED only when all of the following are evidenced:

- source approval and dispatch;
- authoritative destination receipt timestamp;
- explicit destination approval;
- durable destination ingestion identifier;
- destination receipt returned to and recorded by the source;
- read-back from both maps showing matching transfer ID, endpoints, hashes and sequence;
- valid signatures for consequential actions.

Otherwise preserve the most precise incomplete state: SOURCE_ONLY, DISPATCHED_PENDING_RECEIPT, RECEIVED_PENDING_APPROVAL, APPROVED_PENDING_INGESTION, INGESTED_PENDING_SOURCE_ACK, ACK_PENDING_READBACK, or BLOCKED.

Missing authoritative timestamps remain null and block the affected stage. Never replace a remote system timestamp with an assistant clock.

## Project components

| Component | Role | Observed state |
|---|---|---|
| ChatGPT plugin | Applies the event protocol to events available to the assistant or connected tools | Private plugin package created; source files read back |
| FigJam | Visual sequence diagram for bilateral receipts | Diagram added to the existing board |
| GitHub | Reviewable project specification, schema and reference signer | This project branch |
| Wix | Public project explanation and navigation | Static site published |
| AgentMail | Existing operational inboxes for three SY-NeuroKernel agents | Inboxes exist; no event-routing integration claimed |
| Gmail | Agent mail triage labels | Labels created; these are labels, not Google Groups |

### External automation boundary

The plugin does not create a global listener. Automatic capture of map events outside ChatGPT still requires, for each participating map system:

1. a documented event or webhook API;
2. an authenticated adapter and sender identity;
3. a receiving endpoint and durable event store;
4. idempotency and replay protection;
5. destination receipt and acknowledgement delivery;
6. read-back tests on both sides.

Until these are deployed and tested, external map automation is NOT_CONFIGURED / BLOCKED, not active.

## Connected artifacts

- **GitHub project directory:** projects/map-link-provenance/
- **FigJam board:** https://www.figma.com/board/mBeYn5jZU8mHRV7fco9eaU
- **Private ChatGPT plugin:** https://chatgpt.com/plugins/plugins_6afcb34d54c481918a1a317a6db628b2
- **Public Wix site:** https://headless-smcvcvopnwd-beywolf5-1408.wix-site-host.com
- **Related WANGA-LAB research:** [Pattern Emergence and Language Adoption Observation](../../research/PATTERN_EMERGENCE_AND_LANGUAGE_ADOPTION_OBSERVATION.md)

The plugin is private and may require authenticated access. The FigJam URL identifies the diagram; it is not itself proof that another map received or ingested a link.

## Files

- event-schema.json — event envelope schema mirrored from the plugin package.
- sign_event.py — reference SHA-256 signer for the canonical action tuple.
- integration-manifest.json — component inventory and observed integration boundaries.
- sequence.mmd — Mermaid lifecycle diagram.

**Schema note:** the original plugin schema contains the placeholder $id https://example.invalid/map-link-provenance/event.schema.json. It is retained verbatim here; a controlled public schema identifier remains unresolved.

## Evidence discipline

Keep OBSERVATION, ASSUMPTION, EVIDENCE, INFERENCE, and HYPOTHESIS separate. A successful commit, upload, timestamp or hash is evidence only for the specific operation it proves. It is not proof of external delivery, semantic correctness, legal admissibility or production readiness.
