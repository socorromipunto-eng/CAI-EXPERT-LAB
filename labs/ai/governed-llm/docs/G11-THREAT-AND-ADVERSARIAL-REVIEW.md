# G11-THR-001 — Adversarial Review and Negative-Test Scope

Assessment type: developer-controlled laboratory tests, NOT independent security testing.

| Threat | Implemented lab control | Tests / limitation |
|---|---|---|
| Unregistered or effectful tool request | Only one fixed `cai.fixture.read` / READ descriptor | `test_wire_effectful_tool`, `test_34_untrusted_tool_definition_rejected`; no external tool adapter to harden |
| Malformed JSON-RPC, duplicate keys, payload smuggling | Exact wire shape, duplicate-key rejection, size/depth/type/NFC checks | `WireTests` plus wire tests; not a comprehensive MCP parser |
| Filesystem path escape and SSRF | All resources are regex-bound in-memory IDs; no URL or path resolver exists | `test_wire_parent_traversal`, `test_wire_unc_path`, `test_wire_url_resource`; no OS/network egress firewall |
| Cross-tenant data access | Tenant-indexed fixture records and server-provisioned session | `test_19_cross_tenant_lookup_denied`; not a real tenant identity authority |
| Sensitive data release | Class ceiling, per-session clearance, per-tool ceiling | `test_17_confidential_record_denied`, `test_18_restricted_record_denied` |
| Prompt injection in returned text | Data tagged untrusted and never fed to LLM | `test_21_untrusted_injection_is_data_not_command`; DOES NOT test model behavior |
| Unauthorized request, signature misuse | G10 real ML-DSA-87 approval, domain, purpose, trusted key and full request binding | `test_01_unsigned_call_denied`, `test_07_tampered_crypto_signature_denied`, others; lab signer trust only |
| Replay and concurrent double use | G10 thread-safe memory nonce ledger | `test_03_replay_of_valid_signature_denied`, `test_39_concurrent_replay_single_winner`; non-durable/non-distributed |
| Context/policy/tool/resource revocation before read | Epoch and record recheck under fixture authority lock | `test_23_changed_resource_after_sign_before_read_denied` etc.; no external fencing |
| Error leakage | Generic public errors, no raw payload in in-memory metadata audit | `test_27_audit_no_sensitive_content`, `test_41_error_redaction_on_bad_content`; not durable signed evidence |

## Technical-destruction critique

1. Malicious Python code sharing the interpreter can directly access mutable private fixture fields and bypass the gateway. Need OS process/container privilege isolation and deny-by-default egress enforcement.
2. Signature validity is NOT human authentication or a production permission decision. Need authenticated principal/key binding through enterprise IdP and HSM/KMS.
3. In-memory ledgers can lose replay and audit data on restart. Need durable, atomic, tenant-isolated persistence with distributed fencing.
4. Prompt injection is NOT mitigated by content pattern matching here. Only code/data boundary is tested. Need multi-step adversarial LLM-in-the-loop evaluations.
5. External MCP transports, server identity, `initialize`, session lifecycle, subscriptions, notifications, streaming and cancellation are NOT covered. No complete MCP interoperability claim.
6. No actual external side effects were executed or observed; no execution receipts, rollback guarantees or OT safety-case validation.

All six issues remain explicit enterprise assurance HOLDs.
