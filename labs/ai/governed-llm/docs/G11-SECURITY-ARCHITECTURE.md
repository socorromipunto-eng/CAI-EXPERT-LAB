# G11-ARCH-001 — Signed Offline MCP Tool Gate

Status: IMPLEMENTED IN G11 LAB, NOT A PRODUCTION SECURITY BOUNDARY.

## Authority and message flow

1. Caller provides only a bounded JSON-RPC 2.0 `tools/call` message. Any session identity in message content is **not** trusted.
2. Trusted laboratory harness provides a `Session` fixture (tenant, principal, audience, context/policy digests, data clearance, tool allowlist) independently of message data. The production version needs cryptographically authenticated session claims from a vetted IdP.
3. A static `FixtureAuthority` looks up a single allowed tool (`cai.fixture.read`), a canonical resource ID and a tenant-scoped record. No user-configurable executable callback is registered as a tool.
4. `Gateway.prepare_lab_binding` derives `request_digest=SHA256(canonical(intent))`, where `intent` includes the exact JSON-RPC request, server-side session fields, selected tool metadata, resource classification and SHA-256 of the record payload. It is used only for controlled lab signing.
5. An independent laboratory ML-DSA-87 signer issues the unchanged G10 approval envelope with purpose `MCP_TOOL_CALL`. The unchanged G10 `ApprovalVerifier` validates the signature, approved tenant, audience, request ID, nonce, request/context/policy digests, issuance/expiry, signer, trusted public key and local replay reservation. No trust is conferred by a supplied public key in the incoming call.
6. The fixture authority's epoch and record are checked again under a reentrant lock before returning read-only fixture output. Any change in policy/resource/session revision fails closed.
7. Responses contain `UNTRUSTED_FIXTURE_DATA` and `IN_MEMORY_FIXTURE_READ_ONLY` labels. Text is output only; never evaluated or forwarded to an LLM. Error responses never reveal resource/tenant details.

## Critical trust distinctions

- Real ML-DSA-87 signature: YES (OpenSSL 3.5+).
- Real identity behind signer's key: NO (lab enrollment fixtures).
- Real HSM/KMS or protected private key: NO (temporary unencrypted key).
- Trusted, hardened external tool isolation: NO.
- Operational MCP transport conformance: NO (a narrow `tools/call`-shaped emulator).
- Real exfiltration prevention on host processes/networks: NO.
- Deterministic CAI CORE semantics: NOT EVALUATED.

## Atomicity and TOCTOU scope

Signature nonce reservation is synchronized within the in-memory G10 ledger; resource recheck and content release are synchronized within the G11 fixture authority. There is **no distributed transaction across those two locks** and no external side-effect transaction. If G11 fails after consuming a nonce, the nonce remains consumed (safe denial, requiring new approval). A callback to mutate fixture authority is exposed **only in tests**; it is not an execution plugin. External systems require durable locks/fencing, identity revalidation and separate approval.

## Trust hierarchy

Canonical CAI CORE / AI-GOVERNANCE.md and repository `/legal` > approved project-specific architecture/ADRs > this laboratory extension. No extension here changes DSA/ESA/`D(t)` or the separate seven defensive-tactic names from MITRE D3FEND.
