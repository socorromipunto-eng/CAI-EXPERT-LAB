# GATE 10 — Cryptographic Assurance Architecture (DRAFT)

## Trust and data flow

1. **Approved upstream request:** G09 lab request (JSON fixture) with tenant, audience, request_id, nonce, action, context and policy. Identity is explicitly LAB_ASSERTED_HIGH, not authenticated by a real IdP.
2. **Approval payload:** strict finite schema with `domain`, `version`, `tenant_id`, `audience`, `purpose`, `request_id`, `nonce`, `request_digest`, `context_digest`, `policy_digest`, `issued_at`, `expires_at`, `approver_id`, `decision`.
3. **Message:** `b"CAI-G10-MLDSA87-V1\x00" + UTF8(sort_keys compact JSON)`; Unicode must already be NFC, floating-point values not admitted, unknown keys rejected. OpenSSL `-pkeyopt context-string:CAI-G10-v1` supplies ML-DSA signature context.
4. **Signature:** genuine OpenSSL ML-DSA-87 over the complete message; signature 4627 bytes, base64 in an exact four-field envelope (`payload`, `algorithm`, `key_id`, `signature_b64`).
5. **Pinned trust:** verifier receives an out-of-band registered key, recomputes `spki-sha256:<64hex>` from DER SubjectPublicKeyInfo, rejects key substitution, verifies the algorithm family as ML-DSA-87 and binds signer identity, tenant, and permitted purpose from the trust registry.
6. **Validity:** reject future approvals (15-second permitted clock skew), expired approvals, lifetimes above five minutes, invalid purpose, unknown tenant/audience, altered request/context/policy digest, revoked key, bad signature and repetition.
7. **Quorum:** high/critical-impact operations require primary plus second-person signature; any OT safety classification above NONE requires primary plus OT safety signature; signer identities must differ from requester and each other. Risk **derives required quorum**, caller cannot downgrade it.
8. **Post-approval action:** only once the quorum verifies does G09's **mock** executor run. G09 independently performs its pre-dispatch checks. This is not an atomic cross-system transaction or proof of real-world execution.

## Domain and purpose registry

- Domain: `CAI-GOVERNED-LLM/G10/APPROVAL/V1`.
- Algorithm: `ML-DSA-87`, cryptographic profile **provisional**.
- Primary signature purpose: `EXECUTE_ACTION`.
- Additional: `SECOND_PERSON_REVIEW` for HIGH/CRITICAL, or `OT_SAFETY_AUTHORIZATION` for any non-NONE OT class.
- `APPROVE` is the only signing outcome accepted by this authorization gate.
- Test-only public signer mapping and key trust are provided to the verifier externally through the constructor. No public key supplied inside an incoming envelope is automatically accepted.

## Boundary distinctions

Real PQ signature != confirmed end-user identity. A valid signature does not demonstrate that a physical operator held MFA or that key generation/storage was HSM-protected. DER-SPKI SHA-256 is a *key identifier*, not a signature. Memory-only replay protection is not restart safe. Approval verification is not independent evidence that a downstream command happened. Deterministic bytes are not an interoperable cross-language canonicalization standard until one is formally approved and tested.

## Architectural risks (must block production)

- Rollback/replay after process restart or across instances.
- Atomic race between crypto-quorum validation, policy/context recheck and execution on an external target.
- Key theft from test-only unencrypted PEM files.
- Trust-anchor enrollment/rotation/revocation not authoritative, signed or audited across systems.
- Non-independent consent: fixture signer bound by manual trust registry, no real OIDC/SAML/Entra/AD authentication.
- Semantic reconciliation with v0.2.1 schemas and canonical CORE still required.
- Certificate chain, authority separation, record retention, HSM/KMS policy and algorithm agility not implemented.
