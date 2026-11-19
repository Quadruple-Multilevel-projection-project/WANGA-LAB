# Google Developer Provider Catalog

Status: RESEARCHED CANDIDATES — no live account or endpoint connection is claimed.

This catalog separates official SDKs, sample repositories, runtime tooling, and MCP servers. A repository is a code source, not an active service connection.

## Priority A — agent and MCP infrastructure

| Repository / service | Function | How WANGA should use it |
|---|---|---|
| https://github.com/google/adk-web | Web UI / development surface for agents built with Google's Agent Development Kit | Evaluate as a reference UI and agent-development surface |
| https://github.com/google/adk-recipes | ADK example patterns | Reuse patterns only after reviewing license, maintenance and fit |
| https://github.com/googleapis/mcp-toolbox | Open-source MCP server for databases | Candidate connector for supported databases; configure per-source auth and tool allowlists |
| https://github.com/googleapis/mcp-toolbox-sdk-go | Go SDK for MCP Toolbox | Candidate client library for Go-based node services |
| https://developers.google.com/android/management/use-android-management-mcp | Android Management API remote MCP | Enterprise Android fleet metadata and policy workflows; Preview, Google Cloud project/API enablement and IAM required |

## Priority B — Android device and test compute

| Repository / service | Function | How WANGA should use it |
|---|---|---|
| https://developer.android.com/cli | Android CLI for agent-accessible build, test, device, emulator, screen/layout and IDE analysis workflows | First candidate for controlled Android host automation |
| https://github.com/google/android-emulator-container-scripts | Run Android emulators in containers | Candidate for reproducible virtual-device worker pool |
| https://github.com/google/android-cuttlefish | Virtual Android device infrastructure | Candidate for scalable virtual Android node experiments |
| https://developer.android.com/studio/services | Android Studio integrations with Firebase and Google Cloud services | Map supported cloud integrations and required permissions |
| https://developer.android.com/studio/intro | Official Android Studio IDE and toolchain | Build/test authoring environment, not itself a remote server |

Android Studio BYOA/ACP and MCP support are distinct: ACP connects coding agents to IDE-native project intelligence and tools; MCP exposes external tools/services to the agent. They are complementary, not interchangeable.

## Priority C — Firebase and application services

| Repository / service | Function | How WANGA should use it |
|---|---|---|
| https://github.com/firebase/quickstart-android | Official Android Firebase API samples: Auth, Firestore, Functions, Crashlytics, Messaging, Storage, Firebase AI Logic and more | Reference implementations for Android service adapters |
| https://github.com/firebase/functions-samples | Cloud Functions for Firebase examples | Serverless task handlers and event-driven integration patterns |
| https://firebase.google.com/docs | Firebase product/API documentation | Authoritative source for service capabilities and security setup |

## Priority D — Google Cloud SDKs and APIs

| Repository | Function | How WANGA should use it |
|---|---|---|
| https://github.com/googleapis/google-cloud-python | Python client libraries for Google Cloud | Python service adapters |
| https://github.com/googleapis/google-cloud-java | Java client libraries for Google Cloud | Android-adjacent/JVM and backend adapters |
| https://github.com/googleapis/google-cloud-node | Node.js client libraries for Google Cloud | TypeScript/Node adapters |
| https://github.com/googleapis/google-api-python-client | Discovery-based Google APIs Python client | API-specific adapters |
| https://github.com/googleapis/google-api-nodejs-client | Official Node.js Google APIs client | API-specific adapters |
| https://github.com/googleapis/googleapis | Public interface definitions for Google APIs | Schema discovery and API contract references |
| https://github.com/google/XNNPACK | Optimized inference operators for mobile, server and web | Candidate runtime for bounded inference on edge/server nodes |

## Execution order

1. Use Android CLI on a controlled host for local SDK/emulator/device discovery.
2. Use Android Emulator Container Scripts or Cuttlefish for reproducible virtual workers.
3. Use Firebase samples to select Android app-service adapters.
4. Use Google Cloud client libraries for explicitly selected APIs.
5. Use MCP Toolbox only for its supported database integrations; do not treat it as a universal Google Cloud MCP gateway.
6. Use Android Management API MCP only for enterprise device-fleet workflows and only after its preview/IAM prerequisites are approved.

## Evidence and safety rules

- Verify each repository's current maintenance, license, release compatibility and API support before adopting it.
- Keep secrets outside source control.
- Use separate service identities and least-privilege scopes per node.
- Record endpoint identity, API version, tool schema, allowed operations, rate limits and payload limits.
- Do not enable write or device-policy operations during initial discovery.
- Keep model weights local to their designated inference runtime unless an independently approved transfer protocol exists.
- A successful discovery or MCP tools/list is not a functional or security verification.
