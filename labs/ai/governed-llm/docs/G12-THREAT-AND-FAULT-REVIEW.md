# G12-SEC-001 — Adversarial fault review (AI-assisted, NOT independent audit)

| Threat or fault | Local lab test response | Residual / gap |
|---|---|---|
| Approval absent, invalid, wrong purpose, revoked signer | Denied, no effect | No real identity issuer/MFA |
| Changed request, tenant, nonce, policy, context | Bound signature/recheck; deny | Policy fixture only, no canonical CAI semantics |
| Double send, concurrent send, other request same target | Local nonce + SQLite unique claim; one winner | Not distributed; no cross-host fencing |
| Untrusted executor claims success with no observed file | Must independently re-open fixture and match bytes | Same process, no separate trust boundary |
| Process stops before/after local write | INDETERMINATE; recovery reads only, no reissue | Manual operator decision needed for unknown outcome |
| Modified or partial effect | FAILED if observed mismatch | Time-of-check after observer not secured |
| Change to SQLite hash-chain row | Offline chain check stops new issuance | Not cryptographically authenticated immutable log |
| Tampered evidence receipt | ML-DSA-87 verifier rejects; failure to sign prevents committing terminal success | Ephemeral private evidence key not in KMS/HSM |
| Symlink or preexisting target | Exclusive file creation and lstat checks | Not hardened OS isolation / kernel sandbox |
| Untrusted text, secret/path leak | Exact key syntax, bounded `PUT_ONCE` fixture | No real exfiltration or prompt-injection test |

This is **not** a remote execution proof, MCP compatibility test, security certification or IV&V. In this design `PREPARED`, `DISPATCHED` and `INDETERMINATE` do not authorize retries or public assertions of success.
