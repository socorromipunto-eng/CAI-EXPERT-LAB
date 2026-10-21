# G12-GOV-001 — Assurance controls and unresolved decisions

Authority: CAI CORE and the owner's current `AI-GOVERNANCE.md` and `/legal` supersede this unmerged experiment. Baseline reference shared by owner in previous checks: `ccc5d0a6d21ec9a214cfd15b6918797a5c4f5e71`. This gate has **not** re-read/revalidated that Git commit and does not modify it.

### Human and AI roles

- Owner and decision authority: Antonio José Socorro Marín.
- Build and evidence drafting: AI-assisted, NOT separate technical reviewer and NOT independent IV&V.
- Cryptographic keys: locally generated unencrypted temporary PEM. End-user must not use in production.
- Test evidence: test discovery and actual builder stdout, distinguished from owner Windows execution still to be obtained.

### Gate 05 lineage

Previously reported 20 G05 findings remain `OPEN_NOT_REVALIDATED` until checked against current canonical revision and human review. Gate 08-11 results provide laboratory regressions only, not independent closure. Gate 12 does not claim to close any production finding.

### Release blockers

1. Approved and tested canonical CAI CORE policy/decision adapter and real DSA/ESA/D(t) evaluation at execution boundary.
2. Authenticated production principal, MFA, delegated identities and durable authorization context.
3. Actual isolation boundary (Windows AppContainer/VM/container + enforced egress controls), real MCP transports and external-service test environment under separate authorization.
4. Distributed fencing, persistent anti-replay, crash-consistent write-ahead intent/outbox/inbox, trusted time, independent observation and trusted evidence store.
5. HSM/KMS-backed ML-DSA lifecycle, issuance/revocation/rotation, software-supply-chain attestation and real key separation.
6. Independently conducted technical and governance audits with attributable evidence and owner acceptance.
7. Change-scoped permission for repository copy, followed by **separate** staged-diff, commit, and push approvals.

Never treat `test PASS` as authorization to deploy, push, certify or change CORE. No externally hosted execution occurs in G12.
