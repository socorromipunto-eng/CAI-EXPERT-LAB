# G11 / G12 Engineering Exit Criteria

All statuses apply only to the stated target and environment. Evidence IDs for real-world outcomes must be recorded by human reviewers, not invented.

## G11 — laboratory acceptance requirements

1. Integrity hash matches published ZIP. Complete internal SHA256 manifest and G10 immutable file lineage PASS.
2. Python 3.10+, OpenSSL 3.5+ with ML-DSA-87, positive and negative actual cryptographic approval tests PASS.
3. Inherited 169 tests plus 92 new tests executed; zero errors/failures/skips; unique test identifiers and coverage of MCP-001 to MCP-008.
4. No external MCP tools, network actions, process sandboxing or real CAI CORE connection claimed.
5. Audit expressly marked local nonindependent self-review; 20 historical findings not closed without current evidence.

## G12 — proposed future operational execution and evidence gate (NOT AUTHORIZED)

- Formal external MCP server architecture, session/authenticated transport and audited protocol conformance.
- OS/container sandbox with egress deny-by-default, resource limits, network namespaces/Windows containment; independent break-out tests.
- Enterprise IdP + MFA/authorization integration with immutable externally verified issuer trust.
- KMS/HSM-backed PQC key custody, rotation, revocation, algorithm agility ADR, cross-implementation test vectors.
- Distributed durable nonce ledger, TOCTOU fencing, rollback/side-effect transaction boundaries.
- Actual external execution receipts with signed, independently observed effects; INDETERMINATE where evidence is absent.
- Canonical CAI CORE binding to decision validity `D(t)`, DSA, ESA, context drift on pinned approved revision.
- Real LLM prompt-injection evaluations, data-loss prevention and provenance isolation.
- Human IV&V and human governance review independently recorded, plus explicit owner-authorized deployment gates.

Do not infer that G12 is already built or approved from this exit checklist.
