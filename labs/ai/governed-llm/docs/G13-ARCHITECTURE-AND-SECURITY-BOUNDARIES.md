# G13-ARCH-001 — Signed Dual Gate Security Integration (PROTOTYPE)

**Source baseline:** G12 v0.3.4.1 Windows handle-patch ZIP; source/test lineage verified against 22 exact SHA-256 values. The GATE13 implementation is a *new, in-process lab module*, not merged CAI CORE.

## Data and trust flow

1. Test harness provisions a `Session`, `FixtureAuthority`, public-key trust registries, and an in-process trusted `LabPlan` containing `tenant_id`, `requester_id`, MCP resource, a pinned digest of source text, and the exact G12 request digest. **The plan is not an externally signed artifact** and is not attacker-resistant within the Python process.
2. `Gateway._parse` validates a strict closed-world `tools/call` JSON-RPC-looking request. The `Gateway` separately checks read authorization via a **real ML-DSA-87** signature, key pinning, purpose, time, nonce, request, tenant, policy and session authority; the only possible tool is `cai.fixture.read` from an in-memory dataset.
3. `SignedDualGatePipeline._read_response` validates the returned read-only shape and untrusted-data label. It checks the read text SHA-256 against the **preconfigured trusted plan**. It never parses the text as commands or copies it into effect parameters.
4. The completely separate G12 `ControlledBroker` verifies a second ML-DSA-87 approval for a **different purpose/domain**, exact effect intent, actor, context and policy. It writes only to an OS temporary test directory through `PUT_ONCE` and records a local SQLite intent/journal.
5. G12's read-back observer verifies the actual bytes. G13's `ReceiptInspector` verifies the signed G12 receipt, request binding, journal event chain, operation state and a fresh read-back of the local effect. Only a matching result is reported `SUCCEEDED`; otherwise `INDETERMINATE`/`DENIED`/`FAILED` as appropriate.

## Guarantees only within tested threat assumptions

- A signed MCP **read** never grants a signed G12 **write**. Distinct intent bindings and purposes are required.
- Text resembling system prompts, shell commands, URLs, tokens, workflow YAML or JSON tool requests remains **opaque data**, not executable instructions.
- Read resource, effect digest, tenant and actor are pinned by the harness, preventing basic read/write substitution and unintended source-content promotion.
- A forged receipt, altered local effect, altered journal or missing signature cannot be promoted to currently observed success in the tested cases.
- `INDETERMINATE` is preserved on uncertain local execution; `reconcile()` checks only observed effect and **does not repeat** action.
- Concurrent duplicate pipeline calls test single local effect, not cross-node exactly-once semantics.

## Known bypasses and NOT VERIFIED conditions

- A malicious plugin or actor executing **inside the same trusted Python process** could replace a gateway method, modify the `LabPlan`, swap dependency objects or alter disk and recompute the untrusted SQLite hash chain. These are outside this test threat boundary.
- No actual LLM is asked to interpret untrusted data. Successful inert-text tests are **not** evidence of prompt-injection resistance in real models.
- `patch('socket.socket')` in one test validates no Python socket was attempted on that code path. It is **not** a Windows Defender Firewall rule, OS egress restriction, or proof across all code paths.
- Local journal, receipt signer and observer are under one lab operator/control plane; no independent trust anchor, HSM, trusted timestamp, WORM or off-host confirmation.
- Read and write are not one distributed ACID transaction; state may change between the read and effect. G12 authority is rechecked at its own dispatch boundary but no global cross-system lock exists.
- No interface to real Active Directory, Entra, external MCP, OT systems, CAI CORE canonical policy engine or production environment.

## Risk disposition

The package may receive **LAB PASS** if 413/413 pass and lineage/manifest checks pass. Enterprise integration, human IV&V, deployment and release remain **HOLD** until independently verified at explicit scope. Do not assert NASA, NIST, CISA or other accreditation from the tests.
