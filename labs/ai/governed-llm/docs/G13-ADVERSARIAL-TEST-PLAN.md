# G13-TST-001 — Adversarial verification and negative scenarios

**Method:** deterministic unittest against offline in-memory MCP fixture gateway and OS-temp G12 file-effect broker. Every G13 test has a unique ID in `verification/G13-TEST-TRACEABILITY.csv`, mapped to control ADV-001 through ADV-010. Coverage denominator is 89 test *methods*, not every adversarial variant. `test_53` runs 12 additional fixture payload subcases; they are not counted as additional test methods.

| Control | Intent | Evidence / expected outcome |
| --- | --- | --- |
| ADV-001 | Tenant, requester, trusted-plan resource and intent binding | deny mismatch without effect |
| ADV-002 | Distinct signed read and execution approvals | deny missing authorization on either boundary |
| ADV-003 | Prompt-like instructions, command strings, URLs and tool names as data | no tool execution; fixed authorized G12 bytes only |
| ADV-004 | ML-DSA-87 validation, expiry, purpose, revocation and replay | deny invalid / replayed signatures |
| ADV-005 | Signed receipt/observation/request correlation | reject tampered or incorrect receipts |
| ADV-006 | SQLite journal integrity and operation state | deny altered chain/row and missing event |
| ADV-007 | Local concurrency, duplicate intents and recovery | at most one local file effect; no automatic re-dispatch |
| ADV-008 | Fault injection and ambiguous outcomes | never promote `UNKNOWN` to success |
| ADV-009 | Strict wire and response validation; misleading metadata | deny malformed/spoofed content |
| ADV-010 | Baseline invariants, lab capability limits and test inventory | verify described mode only; do not claim external isolation |

**Security tests do not authorize offensive attacks or probing of external systems.** No real malicious payload is sent over a network; strings are contained in a test data record. The original G11–G12 tests run unchanged with G13.

**Note on IV&V:** second Python code path for receipt observation and an AI reviewing its own test implementation do **not** constitute independent verification and validation. G14 needs actual separate human technical and governance adjudicators.
