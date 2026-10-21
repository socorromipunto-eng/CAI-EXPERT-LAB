# G12-ARCH-001 — Local Effect and Observable Outcome (DRAFT)

Source: inherited G11 v0.3.3 lab. Owner: Antonio José Socorro Marín. AI-assisted engineering: disclosed. Status: LOCAL TEST DESIGN; not canonical CAI CORE.

The implementation executes **one closed-world `PUT_ONCE` fixture** to a name derived from a SHA-256 digest under an OS temporary laboratory directory. There is no arbitrary path, shell, network, remote MCP endpoint, production access, plugin, process sandbox, or extension execution. Filesystem effect within an OS temporary directory is a real **local test effect**, not an external action.

Request → strict shape + NFC validation → local authority snapshot → actual ML-DSA-87 approval verification using inherited G10 → pre-dispatch authority epoch recheck → SQLite unique reservation → DISPATCHED journal event → bounded `O_EXCL` local file effect → separate observer re-opens the file and checks exact canonical bytes → SUCCEEDED/FAILED/INDETERMINATE. For SUCCEEDED, a distinct laboratory ML-DSA-87 evidence signature is produced **inside the pending SQLite transaction**, before the terminal success event is committed; signer failure rolls back terminal success and the broker reports INDETERMINATE.

### Four core principles

- **Evidence is not execution:** untrusted executor acknowledgment is discarded. The observer re-opens the file, compares exact bytes and computes a SHA-256 digest, so success requires observed effect. It is a separate code path, **not an independent process or reviewer**.
- **Unknown remains unknown:** a crash before/after effect or a lost observer result returns `INDETERMINATE`, with no success receipt. Recovery only inspects an effect; it never automatically reissues the operation.
- **Local single-reservation fencing:** SQLite UNIQUE `(tenant,request_id)` and `(tenant,effect_key)` plus an in-memory signed nonce ledger block duplicate local dispatch. Not cross-machine, not a distributed transaction; multiple nodes could diverge.
- **Signed evidence:** a separate ephemeral ML-DSA-87 laboratory key signs observed-success receipts. The evidence key is different from the approval key but **is not independently controlled**, HSM-backed, or trusted outside this fixture.

### State transitions

`PREPARED → DISPATCHED → {SUCCEEDED, FAILED, INDETERMINATE}`; `PREPARED → INDETERMINATE` and `INDETERMINATE → {SUCCEEDED, FAILED}` through observation-only recovery; `SUCCEEDED`/`FAILED` terminal. Unexpected transition throws `Denied`. PREPARED cannot upgrade to SUCCEEDED even if matching content is found; prior dispatch must be observed in journal.

### Local protections and explicit limits

- Test-only data, synthetic identities, synthetic approval policy and synthetic context. Full canonical CAI DSA/ESA/D(t), real RBAC/IdP/MFA and OT safety are **not** implemented.
- File writes confined by derived names, expected effect directory and exclusive create. This is best-effort code confinement, not an adversary-resistant OS boundary; same-process privileged code, malicious admin, hardlink/mount or attacker altering test scratch dir can bypass.
- SQLite event hash chain detects accidental or uncoordinated changes, but a privileged attacker can recompute it. No trusted timestamp, immutable off-host append-only storage, WORM, durable key escrow or anti-rollback protection.
- Successful receipt means an effect was present and correct when the observer read it; it is **not** proof of persistence, visibility in distributed clients, service success, safety, or resistance to subsequent modification.
- Interruption after effect write but before journal update can leave `DISPATCHED`; recovery handles this without reexecution. Untrusted host/process failure may prevent fsync or leave partial file; observer returns FAILED/INDETERMINATE instead of promoting success.
