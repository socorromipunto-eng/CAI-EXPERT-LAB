# G11-ASS-001 — Evidence, Limitations and Review Roles

Evidence source classes: owner-provided Windows G10 logs; original G10 ZIP byte hashes; generated G11 source/test files; locally executed G11 runner output after build; eventual independent external evidence (not supplied). Never treat first-party test logs as human-independent IV&V.

- **Cryptographic claim:** real ML-DSA-87 via OpenSSL provider in tests. Not FIPS module validation, production PKI/HSM, or identity proof.
- **Protocol claim:** JSON-RPC 2.0 `tools/call` subset emulator, single registered fixture-read tool; NOT the full MCP specification.
- **Containment claim:** in-process in-memory access mediation, no network adapter by construction; NOT host network restriction or OS sandbox.
- **Prompt-injection claim:** hostile-looking text remains output data; no actual LLM interpretation was tested.
- **Evidence claim:** audit records in process memory, not signed, immutable, durable or independently preserved.
- **Source integrity:** SHA-256 measures bytes, not correctness, functional implementation, legal validity or security approval.
- **HOLD:** real enterprise scope, signed policies from production authority, canonical CORE, independent review, commercial/legal deployment classification and release authorization.
