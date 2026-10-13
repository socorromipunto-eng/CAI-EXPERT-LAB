# CAI Engine — MCP Security Specification (Core)

| Field | Value |
|---|---|
| Document ID | CAI-ENG-SEC-001 |
| Version | 0.8 |
| Status | PROPOSED — requires owner approval before any implementation |
| Classification | Public (repository document) |
| Project | CAI-EXPERT-LAB / CAI-Engine |
| Phase | Proposed specification for cai-engine 0.5.0; owner approval pending (gate G0) |
| Target release | cai-engine 0.5.0, delivered through gates G0 to G8 (§16) |
| Companion documents | CAI-ENG-SEC-001-EU (EU jurisdiction profile); CAI-ENG-SEC-001-USA (USA jurisdiction profile) |
| Baseline | Git commit b52935e (cai-engine 0.4.2) |
| Owner | Antonio José Socorro Marín |
| Prepared by | Antonio José Socorro Marín |
| Date | 2026-10-13 |

Copyright © 2026 Antonio José Socorro Marín. All rights reserved. Use is governed by the legal documents in the `/legal` directory of this repository.

## Revision history

| Version | Date | Change |
|---|---|---|
| 0.1 | 2026-10-12 | Initial proposal: 14 findings, 16 requirements (SR-01 to SR-16), 22 acceptance tests. |
| 0.2 | 2026-10-12 | Revision after design review A-01 to A-09: 17 requirements, 32 tests, seven gates. |
| 0.3 | 2026-10-12 | Redesign after review of v0.2 (R-01 to R-38): pinned root of trust, signed monotonic trust manifest, one key per purpose, deployment profiles, operation catalogue, AI-system registration, event-sourced evidence, in-process signature verification, explicit state machine. 24 requirements, 18 findings, 59 tests, gates G0 to G8. |
| 0.4 | 2026-10-12 | Revision after review of v0.3 (V-01 to V-39, Appendix A): gate dependencies corrected and tests renumbered by gate; revalidation extended to AUTHORIZED decisions and to the moment before dispatch; IPC without object deserialization and with peer identity from the operating system; `human_disclosed` and `explainable` moved to the AI-system registration; registry and catalogue digests carried by their own signed indexes; operator commands bound without a global sequence number; Git anchor commits signed in namespace `git`; missing snapshot rebuilt from evidence; review of compromised keys as an overlay flag; commands admitted in SAFE_HALT; anchoring degradation mode; durability with `fsync`; import of 0.4.2 evidence; multi-target evaluation; key binding in signature verification; approver hardware keys in profile P. 24 requirements, 18 findings, 73 tests. |
| 0.5 | 2026-10-12 | Split into a jurisdiction-neutral core and two jurisdiction profiles (EU, USA) with the same rank; jurisdiction-specific content moved to the profiles and replaced by the profile interface (SR-26). Cryptographic agility and hybrid post-quantum signatures (SR-25): Ed25519 + ML-DSA-87 for every engine-, authority- and adapter-held key, hybrid approvals (hardware Ed25519 for presence + ML-DSA-87), SHA-384 for digests in new epochs. Test identifiers kept stable; new tests AT-74 to AT-82. 26 requirements, 18 findings, 82 tests. |
| 0.6 | 2026-10-12 | Revision after review of v0.5 and the profiles (W-01 to W-30, Appendix B): hybrid trust anchor with pinned suite for `cai-admin`; normative core gate table (SR-27) with a core confidence floor that profiles can only raise; approver key wording aligned with the hybrid suite; signed sources loaded from the protected directory, not over IPC; ML-DSA self-tests limited to ACVP keyGen and sigVer plus sign-verify; defined key identifiers and pair compromise; cross-implementation ML-DSA vectors; national-security deployments not supported in 0.5.0; retention and default-jurisdiction fields in the manifest; minimum approvals as a profile output; jurisdiction text removed from the core. 27 requirements, 85 tests. |
| 0.7 | 2026-10-12 | Consistency corrections from the final review (X-01 to X-16, Appendix C): profile-P tests moved to G8; approval minimum = maximum of catalogue, emergency and profile minimums; core confidence floor fixed as a minimum; reason codes for core gates; pair-compromise, `nss`, `crypto-inventory` and default-jurisdiction tests; `classical_suite_end` defined in the profile interface; profile manifest requirements re-checked at registry reload. 27 requirements, 87 tests. |
| 0.8 | 2026-10-13 | Published in the repository (CHG-2026-10-13-01): header block completed (Phase, Owner, Prepared by); MITRE D3FEND added to the normative references as the source of the lifecycle stage names; deployment profile table no longer names a specific embedded platform. No requirement, finding or test changed. |

---

## 1. Purpose

This specification defines the security architecture, requirements, signed statement formats and acceptance tests for the CAI Engine Model Context Protocol (MCP) interface and the decision path behind it. It applies the CAI principle that a decision is valid only while its Decision State Awareness (DSA) remains aligned with Environmental State Awareness (ESA) at execution time (CAI-Core-Taxonomy §8.6) to AI clients that propose security actions.

Design principle: **the governed party supplies a request, never the facts used to judge it.** Every attribute that decides how strictly a proposal is treated comes from a signed source controlled by people: the asset registry, the operation catalogue, the AI-system registration or the trust manifest. What the AI client declares is recorded and can only deny or add scrutiny.

Claims principle: a guarantee in this document is demonstrated only when its acceptance tests have passed at an identified commit (SR-24).

Structure: this core is jurisdiction-neutral. Everything that depends on a legal or regulatory framework (classification rules, regulatory gates, thresholds tied to regulation, sector vocabularies, retention and migration timelines) is specified in the jurisdiction profiles CAI-ENG-SEC-001-EU and CAI-ENG-SEC-001-USA, which have equal rank and are bound by the profile interface (SR-26). A profile may add controls; it may never relax a control of this core.

## 2. Scope and deployment profiles

### 2.1 Scope

In scope: the MCP interface; the governed decision path (`governed_agent.py`, `eu_ai_act.py`, `usa.py`, `gates.py`, `engine.py`); approvals and denials; operator commands; asset registry, operation catalogue and AI-system registration; trust manifest; evidence, state and recovery; keys and signatures; the engine side of the adapter contract and a reference test adapter; migration of 0.4.2 evidence.

Out of scope for 0.5.0: protection against an attacker with administrative control of the host or control of the engine service account (beyond what L3 anchoring detects); hardware security module storage of engine keys; SLH-DSA and `pq-only` suites (SR-25.3, SR-25.7); deployments for U.S. national security systems (SR-25.8); production execution adapters; computation of context drift and of the telemetry and risk terms of D(t) (SR-24.3).

### 2.2 Deployment profiles

| Profile | Purpose | Process model | Evidence level | Real adapters or industrial systems |
|---|---|---|---|---|
| D — Development | Research, tests, demonstrations | Engine in the same process and account as the MCP server (stdio) | L1 or L2 | MUST NOT be connected |
| P — Protected | Any use that can cause an effect outside the engine | Engine service under a dedicated account; one MCP front end per AI-system account, without access to engine files; local IPC (§12.2) | L3 (mandatory) | MAY be connected, after G8 |

The profile is stated in the signed trust manifest. In profile D every tool result carries `profile: "D"` and `effects: "none permitted"`, and the engine refuses to load adapter keys.

## 3. Normative references

- Model Context Protocol specification, revision pinned in the G1 release notes: tools, tool annotations, stdio transport, Authorization for HTTP-based transports.
- OpenSSH PROTOCOL.sshsig (SSH signature format) and PROTOCOL.u2f (`sk-ssh-ed25519@openssh.com` signatures, flags and counter); allowed-signers file format.
- Git SSH signing (`gpg.format = ssh`), which signs in namespace `git`.
- RFC 8032 (Ed25519); RFC 8785 (JSON Canonicalization Scheme) and its test vectors; RFC 8259 (JSON); RFC 3161 (Time-Stamp Protocol).
- Python `cryptography` package (Ed25519 and ML-DSA primitives; ML-DSA requires version 48 or later with OpenSSL 3.5 or later, or an AWS-LC or BoringSSL build), pinned by version and hash.
- FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA), FIPS 180-4 (SHA-384), and the NIST ACVP test vectors for ML-DSA.
- Windows Authz API (`AuthzAccessCheck`) and named-pipe security (`CreateNamedPipeW`, security descriptors in SDDL, `PIPE_REJECT_REMOTE_CLIENTS`, `GetNamedPipeClientProcessId`); POSIX `SO_PEERCRED` / `getpeereid`.
- NIST SP 800-53 Rev. 5: AC-3, AC-5, AC-6, AU-4, AU-5, AU-9, AU-10, CM-5, IA-5, SC-12, SI-7, SI-10.
- MITRE D3FEND 1.6.0 (https://d3fend.mitre.org): the seven defensive tactics Model, Harden, Detect, Isolate, Deceive, Evict and Restore are the source of the engine's lifecycle state names (MODEL to RESTORE); CAI adds the entry conditions, per-state action categories, blocked transitions and decision gates. MITRE D3FEND is a trademark of The MITRE Corporation.
- CAI-Core-Taxonomy v0.2 §8.4 to §8.8; CAI-MX Formal Decision Rules §13 (enforcement mapping), §14 (enforcement timing), §15 (revalidation), §16 (determinism), §18 (fail-safe); CAI-Engine-Safety-Gates-and-Human-Oversight §5.2; CAI-Engine-State-Orchestration-and-Control §10.

MUST, MUST NOT, SHOULD and MAY are normative.

## 4. Baseline findings (commit b52935e)

"Executed" means reproduced by running the baseline code; "static" means found by reading it. Unless stated otherwise, governed-path reproductions use `confidence = 0.97` and `explanation = "x"`, so that the confidence and explanation gates admit the proposal and the finding under test is isolated.

| ID | Finding | Reproduction | Severity |
|---|---|---|---|
| F-01 | The AI client supplies the risk context used to govern it. | Governed path, state MODEL, category OBSERVE, description "modify grid relay". EU: `sector = energy, safety_component = true` gives PENDING_APPROVAL; context omitted gives EXECUTED. USA: `sector = energy` gives PENDING_APPROVAL; omitted gives EXECUTED. Executed. | Critical |
| F-02 | A non-finite confidence bypasses the confidence gate. | Direct path `ai_confidence = float("nan")`, and governed path `confidence = "nan"` with `explanation = "x"`: ALLOW / EXECUTED, because `NaN < 0.80` is false. Executed. | Critical |
| F-03 | Automatic initialization destroys evidence. | `state.json` removed; `_ensure_init()` calls `init()`, which truncates `evidence.jsonl` (2 records to 1). Executed. | Critical |
| F-04 | Malformed input raises an unhandled exception and leaves no evidence. | Unknown key in `context` raises `TypeError`; evidence count unchanged. Executed. | High |
| F-05 | Field types are not validated. | `ot_level = "1"` raises `TypeError` in the safety gates. Executed. | Medium |
| F-06 | Any jurisdiction string is accepted. | `jurisdiction = "XYZ"` is evaluated under EU and recorded as "XYZ". Executed. | Medium |
| F-07 | Approval authorizes a pending action without re-evaluation. | Scenario T-09: containment pending in ISOLATE; state moved to EVICT; `approve()` records execution; re-evaluation in EVICT gives DENY. Executed. | High |
| F-08 | The approver is not authenticated. | `approve()` checks only that a name is non-empty; `deny()` checks nothing. Static. | High |
| F-09 | The MCP client is neither identified nor authorized. | No identity checked or recorded; trust rests on stdio. Static. | High |
| F-10 | "EXECUTED" is recorded although nothing is executed or verified; tool documentation repeats it. | The engine has no actuator; `cai_govern` docstring and server instructions say EXECUTED. Static. | Medium |
| F-11 | The evidence chain is unsigned and unanchored. | Whole-chain rewrite verifies (scenario T-08); removing the most recent records verifies. Executed. | High |
| F-12 | No concurrency control, durable writes or crash recovery. | Concurrent appends can read the same previous hash; no `fsync`; a crash between state and evidence writes leaves them inconsistent. Static. | Medium |
| F-13 | No resource limits; `cai_report` returns the whole log. | Static. | Medium |
| F-14 | Client text is returned verbatim to the client. | Description, `ai_system`, `model_version` and `prohibited_reason` echoed. Executed. | Low |
| F-15 | The AI client declares the attributes that decide strictness. | Category, `destructive`, `blast_radius`, `affects_privileged_accounts`, `human_disclosed`, `explainable`, confidence, drift and provenance are client-declared. "modify grid relay" labelled OBSERVE is EXECUTED in MODEL; with `interacts_with_persons = true`, adding `human_disclosed = true` changes PENDING_APPROVAL to EXECUTED. Executed. | Critical |
| F-16 | The AI client chooses the regulatory profile. | `sector = energy` without `safety_component`: EXECUTED under EU, PENDING_APPROVAL under USA. Executed. | High |
| F-17 | The state file can be edited without detection. | `current_state`, `facts` and `pending` in `state.json` are trusted at load. Static. | High |
| F-18 | Safety-relevant facts are set without attribution. | `set_fact("safety_approved", True)` needs no signature. Static. | High |

## 5. Threat model

### 5.1 Actors

| Actor | Trust | Assumed capabilities |
|---|---|---|
| AI client | Untrusted; the governed party | Any call, argument, order and rate; may be prompt-injected; may run shell commands as the account it runs under. |
| MCP front end (profile P) | Untrusted for authority | One instance per AI-system account; validates and forwards; holds no keys; no access to engine files. |
| Engine service (profile P) | Trusted computing base | Owns state, evidence and engine keys under a dedicated account. |
| Operator | Trusted for operation only | Submits signed operator commands. |
| Approver | Trusted only through a valid signature | Signs approval statements and safety assertions. |
| Registry authority | Trusted only through a valid signature | Signs asset classifications and the registry index. |
| Catalogue authority | Trusted only through a valid signature | Signs the operation catalogue and AI-system registrations. |
| Owner | Root of trust | Holds the administrative key; signs the trust manifest, epoch archives and legacy imports. |
| Execution adapter | Trusted only through a valid signature | Acknowledges and reports execution. |
| Host attacker | Untrusted | Rights of a non-administrative account other than the engine service account. In profile D this includes the account the engine runs under. |
| Network attacker | Untrusted | Relevant only to the external anchor store and to a future HTTP transport. |

### 5.2 Assets

Decision integrity; the trust anchor, trust manifest and signed indexes; registry entries, catalogue and AI-system registrations; evidence, checkpoints and anchors; state snapshots; private keys; engine code and configuration.

### 5.3 Trust boundaries

1. AI client → MCP front end: untrusted data.
2. MCP front end → engine: length-prefixed JSON only; caller identity from the operating system (§6.5).
3. People → engine: authority crosses only as signed statements (§8).
4. Engine → evidence: append only, durable, event-sourced, checkpointed, anchored at L3.
5. Engine ↔ adapter: signed dispatch, signed reports, single use; adapters verify the trust manifest.

### 5.4 Security objectives

- O1. Classification, operation category and impact, jurisdiction, regulatory use-case attributes and AI-system scope never come from the AI client. The remaining client inputs (confidence, explanation text, drift score, provenance) can only deny or escalate (§15).
- O2. An action is authorized and dispatched only if every gate admits it at that moment, against signed context.
- O3. Authority is accepted only as a valid, unrevoked, non-replayed signature by the key bound to the principal, over the exact statement.
- O4. Tampering with evidence or state is detected up to the declared evidence level (§10.4), and the engine stops or degrades as specified.
- O5. Invalid input, internal errors, storage failures and trust failures fail closed.
- O6. Recorded states and published claims state only what happened and what was tested.

## 6. Trust architecture

### 6.1 Root of trust

1. The trust anchor file contains the owner's two administrative public keys (Ed25519 and ML-DSA-87, namespace `cai-admin`), the suite required for `cai-admin` (pinned to `hybrid`; it cannot be changed by any manifest), the deployment identifier and the profile. The owner installs it in a protected configuration directory (§6.4).
2. At start the engine checks that the trust anchor, the configuration directory, every parent directory and the engine code directories (§6.4.3) cannot be modified by the engine account (profile D: by any non-administrative account other than the owner's) or by any front-end or AI-client account (profile P):
   - Windows: an effective-access check with `AuthzAccessCheck` (through `ctypes`) for each account, counting as modification rights `FILE_WRITE_DATA`, `FILE_APPEND_DATA`, `WRITE_DAC`, `WRITE_OWNER`, `DELETE`, and `FILE_DELETE_CHILD` on the parent; ownership of the object by the account counts as `WRITE_DAC`.
   - POSIX: owner and mode of each object and parent; the presence of an extended ACL (`system.posix_acl_access`) on any of them fails the check unless the deployment records an explicit review of that ACL in the manifest.
3. Outcome: if the manifest declares profile P and the check fails, the engine refuses to start and writes the reason to the fault file. If the manifest declares profile D, the engine starts at L1, records `TRUST_ANCHOR_UNPROTECTED` and marks every result `trust: degraded`.
4. The administrative fingerprint, SHA-384 over the canonical JSON of both administrative public keys (key encodings as in SR-25.1), is written in the genesis record of each epoch and anchored at L3. A change of administrative key requires a new epoch.

### 6.2 Trust manifest

1. The trust manifest is canonical JSON (RFC 8785) signed with `cai-admin`. It contains:
   - `deployment_id`, `version` (integer), `issued_at`, `valid_until`;
   - `profile` and `evidence_level`;
   - principals: for each person or adapter, a key pair (classical and ML-DSA-87 public keys), role (`approver`, `registry_authority`, `catalogue_authority`, `operator`, `adapter`), the suite required for each purpose, `valid_after` and `valid_before`; in profile P the classical key of an approver MUST be `sk-ssh-ed25519@openssh.com`;
   - for each AI system, the operating-system account it runs under (profile P);
   - the engine checkpoint and dispatch public keys with validity periods;
   - the cumulative revocation list, by `key_id` only: every retired or revoked key with `reason` (`retired` or `compromised`), `effective_at` and, for compromise, `last_known_good`;
   - minimum versions of the registry index, catalogue and AI-system registration (not their digests; see SR-06.4);
   - `default_jurisdiction` (a registered profile identifier, used only for reporting under SR-09.3), `retention_min_days`, and `nss` (true for U.S. national security systems; not supported in 0.5.0, SR-25.8);
   - deployment parameters: rate limits, quotas, expiry windows, freshness window, anchoring grace period, thresholds;
   - the external anchor location and the anchor public key (L3);
   - the hash of the approved engine code manifest (§6.4.3).
2. Monotonic version: a manifest whose `version` is lower than the highest version recorded in the deployment's evidence (across epochs, §10.2) is rejected and recorded as `TRUST_MANIFEST_REJECTED`; the engine keeps running with the manifest in use. A manifest whose revocation list omits any entry of the manifest in use is rejected the same way.
3. If the manifest in use expires, the engine enters SAFE_HALT (SR-17); loading a valid newer manifest is admitted in SAFE_HALT.
4. A key in the revocation list is never accepted in any role.
5. Each load is recorded as `TRUST_MANIFEST_LOADED` with version and digest.

### 6.3 Keys by purpose

No key serves two purposes.

| Key | Holder | Namespace | Signs | Algorithms (SR-25) | Custody |
|---|---|---|---|---|---|
| Administrative | Owner | `cai-admin` | Trust manifest, `archive`, `import-legacy` | Ed25519 (hardware token or software) + ML-DSA-87 | Offline when not in use; ML-DSA key passphrase-protected |
| Approver | Each approver | `cai-approval` | Approval and denial statements, safety assertions, review closures | `hybrid`: classical part `sk-ssh-ed25519` with user presence in profile P (`ssh-ed25519` allowed in profile D) + ML-DSA-87; `classical` suite allowed only in profile D | Hardware token for the Ed25519 part; ML-DSA key passphrase-protected on the approver's machine |
| Registry authority | Classifier | `cai-registry` | Registry entries and registry index | Ed25519 + ML-DSA-87 | Hardware token or passphrase-protected keys |
| Catalogue authority | Owner or delegate | `cai-catalogue` | Operation catalogue, AI-system registrations, profile parameters | Ed25519 + ML-DSA-87 | As registry authority |
| Operator | Each operator | `cai-operator` | Operator commands and non-safety fact assertions | Ed25519 + ML-DSA-87 | As registry authority |
| Engine checkpoint | Engine service | `cai-evidence` | Checkpoints | Ed25519 + ML-DSA-87 | Unattended file keys, engine account only |
| Engine dispatch | Engine service | `cai-dispatch` | Dispatch messages | Ed25519 + ML-DSA-87 | Unattended file keys, separate files, engine account only |
| Adapter | Each adapter | `cai-adapter` | Acknowledgements and reports | Ed25519 + ML-DSA-87 | Unattended file keys on the adapter host |
| Anchor | Anchoring job outside the engine host | `cai-anchor` for anchor records; `git` for the anchor commits | Anchor records (hybrid); Git commits (Ed25519, classical) | Ed25519 + ML-DSA-87 for records | Unattended keys on the anchoring host |

Passphrase and hardware custody of human keys is checked at provisioning by the owner, not by the engine; the engine checks key type and, for `sk` keys, the user-presence flag.

### 6.4 Protected paths and code integrity

1. The trust anchor, manifest, signed indexes, registry, catalogue, AI-system registrations and engine configuration reside in a configuration directory writable only by the owner or an administrator.
2. In profile P the engine service account has read access to the configuration directory and write access only to its runtime directory (state, evidence, engine keys); front-end and AI-client accounts have no access to either.
3. The installation of the engine (Python runtime, `site-packages`, `cai_engine`) is in directories that front-end and AI-client accounts cannot modify (checked as in §6.1.2). At start the engine computes the SHA-384 of every file of `cai_engine` and of the pinned dependency files, compares the result with the code manifest whose hash is in the trust manifest, records the result in the genesis record of new epochs and in `ENGINE_STARTED`, and refuses to start in profile P on mismatch.

### 6.5 Privilege separation and IPC (profile P)

1. The engine service and each MCP front end run under different operating-system accounts; there is one front-end instance per AI-system account.
2. Transport: Windows named pipe created by the engine with `CreateNamedPipeW` through `ctypes`, with an explicit security descriptor (SDDL) granting connect access only to the registered front-end accounts and the operator accounts, and with `PIPE_REJECT_REMOTE_CLIENTS`; POSIX Unix-domain socket in a directory owned by the engine account with mode 0750 and a group containing only those accounts.
3. Messages are length-prefixed UTF-8 JSON (at most 64 KiB) validated under SR-01. No object deserialization (for example `pickle`) is used anywhere on the IPC path; if `multiprocessing.connection` is used, only `send_bytes` and `recv_bytes` are permitted, and a static test (AT-70) verifies that `recv()` and `send()` are not used.
4. Peer identity is taken from the operating system: `SO_PEERCRED` (Linux) or `getpeereid` (BSD, macOS); on Windows, `GetNamedPipeClientProcessId` and the owner of that process's token. The engine maps the account to an AI system through the manifest. A client-declared identity that differs is recorded.
5. Authority-bearing submissions (signed statements, adapter reports) are verified as signed statements regardless of the submitting account.

## 7. Security requirements

### A. Interface

**SR-01 Strict input validation** (F-02, F-04, F-05; V-01)
1. Every request is validated against a closed schema; unknown keys are rejected at every level.
2. Numbers MUST be finite JSON numbers; `NaN`, `Infinity`, numeric strings and booleans in numeric fields are rejected. `confidence` and `drift_score` MUST be in [0.0, 1.0].
3. Strings: `explanation` at most 2 000 characters, other strings at most 256; control characters other than tab and newline are rejected.
4. Request at most 32 KiB; nesting depth at most 4; at most 64 targets.
5. A proposal names an `operation_id` and one or more targets `{type, id}`. Target syntax is defined by a grammar built into the engine for `host` (RFC 1123 name), `ip` (IPv4 or IPv6), `cidr`, `account` (`domain\name`, `name@domain` or local name), `file_hash` (SHA-256, SHA-384 or SHA-512 hex), `url` (absolute `https` or `http` URL) and `dn` (RFC 4514). The catalogue states which target types each operation accepts.
6. Fields that the signed sources own are rejected if a client supplies them: the core-owned fields `category`, `destructive`, `blast_radius`, `affects_privileged_accounts` and `explainable`, and every registry or registration field defined in any profile (§4 and §5 of each profile). Declared context is accepted only inside `declared_context` (SR-11).
7. Validation is identical on every path (MCP, IPC, CLI, Python API).

**SR-02 Fail closed** (F-04)
1. Any validation failure or internal exception returns `REJECTED` with a reason code and authorizes nothing.
2. Outside SAFE_HALT, rejections are recorded as `PROPOSAL_REJECTED` with the SHA-384 of the raw input and reason codes, subject to SR-03.3 and SR-03.4.
3. In SAFE_HALT, refusals are written only to the fault file and error stream.

**SR-03 Rate limits and quotas** (F-13; V-16, V-38)
1. Every operation is rate-limited per AI system (profile P: per operating-system account; profile D: per process) — defaults: 30 proposals and 60 read calls per minute.
2. `cai_report` returns at most the last 50 records in summarized form.
3. Rate-limited and quota-rejected calls are not recorded individually. For each AI system and minute with at least one such call, one `RATE_LIMITED` or `QUOTA_REJECTED` record with the count is written at the first append after the minute ends, or at checkpoint, whichever comes first.
4. Quota applies to the active epoch's segments; archived epochs and closed segments in the archive directory do not count. At 90 % of the quota, new proposals are rejected (`QUOTA`) while a reserve remains for engine records (expiry, revalidation, condition changes), approvals, denials, operator commands and checkpoints. At 100 % the engine enters SAFE_HALT.

**SR-04 Output policy** (F-14)
1. Results contain identifiers, enumerated values, gate names, engine-generated reason codes and digests.
2. Client-supplied text appears only in `untrusted_text`: control characters removed, at most 120 characters, labelled as client-supplied.
3. Reason texts are engine templates, or reason-code templates defined by a profile, and never interpolate client text.
4. Tool descriptions and server instructions use the §9 state names and do not describe authorization as execution (F-10).

**SR-05 Exposure and transport** (F-09)
1. In 0.5.0 the MCP transport is stdio only; the server refuses to start an HTTP transport.
2. The MCP interface exposes exactly the tools of §12.1. No AI-facing interface approves, denies, initializes, resumes, transitions, sets facts, loads signed sources, reads keys or reports adapter results.
3. The client name and version declared at MCP initialization are recorded as declared. In profile P the authoritative identity is the operating-system account (§6.5.4).

### B. Context and policy

**SR-06 Signed asset registry** (F-01; V-06, V-23)
1. Classification comes only from registry entries signed with `cai-registry` by a valid registry authority. Entries that do not verify are ignored and recorded as `REGISTRY_ENTRY_REJECTED`.
2. Each entry contains the core fields `target`, `target_type`, `jurisdictions` (non-empty set of profile identifiers, `EU` and/or `USA`), `safety_component`, `ot_level` (0 to 5 or null), `asset_group_size` (integer ≥ 1), `classified_by`, `classified_at`, `valid_until`, `emergency`, `entry_version`, and, for each listed jurisdiction, the classification fields that profile requires (EU profile §4, USA profile §4).
3. Vocabularies (sectors, areas, categories) are closed and defined by each profile; a value outside the profile's vocabulary makes the entry invalid.
4. The registry index, signed with `cai-registry`, lists the digest and version of every entry and carries a monotonic `registry_version`. The engine rejects an index older than the highest version recorded in the deployment's evidence or than the manifest minimum. Registry authorities can therefore change entries, including emergency entries, without the administrative key.
5. Reload happens at start and on a signed operator `reload` command; each reload is recorded with the index version and digest and triggers SR-13.4. At every reload the engine re-checks the manifest requirements of each profile present in the registry (retention minimum, `classical_suite_end`); if they are not met, the reload is refused and recorded, and the previous registry stays in use.

**SR-07 Operation catalogue** (F-15)
1. The catalogue, signed with `cai-catalogue` and carrying a monotonic version, defines for each `operation_id`: `category`, `operational` (true or false), `destructive`, `affects_privileged_accounts`, accepted target types, parameter schema, maximum number of targets, required approvals (M of N, distinct principals), permitted adapters, and the lifecycle states in which it may be proposed.
2. `blast_radius` is computed by the engine as the sum of `asset_group_size` over the targets.
3. Category, destructiveness and privileged impact are taken from the catalogue only.
4. The dispatch carries the operation identifier and the digest of the exact parameters; adapters refuse anything else (SR-21).

**SR-08 AI-system registration** (F-15, F-16; V-05)
1. Each AI system is registered in a document signed with `cai-catalogue`: identifier, model family, permitted operations, maximum autonomy (observation only, or operational with approval), `explainable` (whether the system produces explanations), and the use-case attributes required by each profile it operates under (EU profile §5, USA profile §5).
2. An explanation text supplied by the client can only tighten: if the registration says `explainable = true`, an empty explanation fails the explainability gate; a non-empty explanation never makes a system explainable that the registration says is not.
3. Profile P: the system is identified by its operating-system account. Profile D: by declaration, marked `identity: declared`.
4. Proposals from an unregistered system, or for an operation outside its permitted set, are BLOCKED.

**SR-09 Jurisdiction and multiple targets** (F-06, F-16; V-23)
1. The jurisdictions of each target are taken from its registry entry. A target listed under several registered profile identifiers is evaluated under each of those profiles and the strictest outcome applies. A client-declared jurisdiction is recorded and compared under SR-11.
2. A proposal with several targets is evaluated per target under each target's classification and jurisdiction; the decision takes the strictest outcome (DENY over ESCALATE over ALLOW) and the union of approval requirements.
3. For `UNCLASSIFIED_OBSERVE` records, the manifest's default jurisdiction is recorded for reporting only; it does not admit any operational action.

**SR-10 Unclassified targets and emergency classification** (V-28, V-32)
1. An observation-only operation (catalogue `operational = false`) on a target without a valid registry entry is not blocked by CORE_UNCLASSIFIED; it is recorded with `UNCLASSIFIED_OBSERVE` and the manifest's `default_jurisdiction`, so that discovery can proceed. Other core gates still apply.
2. An operational action on such a target is BLOCKED with reason `UNCLASSIFIED_TARGET`; no approval request is created.
3. Emergency classification: a registry authority signs an entry with `emergency = true` and `valid_until` at most 4 hours after `classified_at`, published through a new registry index. Operational actions on that target require max(M, 2) approvals from distinct principals, where M is the catalogue requirement, and are recorded with `EMERGENCY_CLASSIFICATION_USED`. After expiry the target is unclassified again, and `EMERGENCY_CLASSIFICATION_EXPIRED` lists the decisions taken under it for post-incident review.

**SR-11 Declared-context conflicts** (V-27)
1. Context and jurisdiction declared by the client in `declared_context` are recorded; only the fields actually declared are compared with the registry.
2. A difference escalates the decision with reason `DECLARED_CONTEXT_CONFLICT`, showing both values in the approval request. This never relaxes a gate.
3. Conflicting proposals beyond the limit (default 5 per AI system per hour) are REJECTED with reason `CONFLICT_RATE`, aggregated under SR-03.3. The counter is a rate limit and not an input of the decision.

**SR-27 Core gates**
The core gates below are evaluated for every proposal before the profile gates. Thresholds are signed catalogue parameters; profiles may raise them and may add gates, but may not lower or remove them (SR-26.2).

| Gate | Trigger | Outcome | Reason code | Fixed minimum |
|---|---|---|---|---|
| CORE_SYSTEM_SCOPE | AI system unregistered, or operation outside its permitted set (SR-08.4) | DENY | `SYSTEM_NOT_PERMITTED` | — |
| CORE_UNCLASSIFIED | Operational operation on a target without a valid registry entry (SR-10.2) | DENY | `UNCLASSIFIED_TARGET` | — |
| CORE_STATE_POLICY | Operation not permitted in the current lifecycle state (catalogue) | DENY | `STATE_POLICY` | — |
| CORE_AI_CONFIDENCE | Declared confidence below the core floor | DENY | `AI_CONFIDENCE` | 0.80 |
| CORE_AI_EXPLAINABILITY | Registration `explainable = false`, or empty explanation | DENY | `AI_EXPLAINABILITY` | — |
| CORE_OT_SAFETY | Target `ot_level` ≤ 2 and operation of category CONTAINMENT or ERADICATION, or destructive | ESCALATE | `OT_SAFETY` | Purdue level 2 |
| CORE_OPERATIONAL_IMPACT | Destructive operation (catalogue) | ESCALATE | `OPERATIONAL_IMPACT` | — |
| CORE_BLAST_RADIUS | Computed blast radius above threshold (SR-07.2) | ESCALATE | `BLAST_RADIUS` | 25 assets (maximum) |
| CORE_MANDATORY_HUMAN | Lifecycle state EVICT; operation affects privileged accounts; category CONTAINMENT or RECOVERY | ESCALATE | `MANDATORY_HUMAN` | — |
| CORE_DECLARED_CONFLICT | Declared context differs from the registry (SR-11) | ESCALATE | `DECLARED_CONTEXT_CONFLICT` | — |

The values in the last column are fixed bounds: the catalogue may make them stricter (a higher confidence floor, a higher Purdue level for OT safety, a lower blast-radius threshold) but never less strict; a catalogue that does so is refused at load. The core confidence floor (0.80) equals the baseline `AI_MIN_CONFIDENCE`; a profile threshold at or below it has no effect and is not defined.

### C. Decision lifecycle

**SR-12 State machine** (F-10)
The decision states and transitions of §9 are normative from G1. The recorder rejects any other state name. CAI-MX enforcement outcomes (§13 of that document) map as follows: AUTHORIZED ↔ ALLOW, PENDING_APPROVAL ↔ ESCALATE, REVALIDATION_REQUIRED ↔ REQUIRE_REVALIDATION, REVALIDATION_DENIED ↔ REVOKE, BLOCKED and DENIED_BY_HUMAN ↔ DENY.

**SR-13 Revalidation, expiry and authorization timing** (F-07; V-03, V-25, V-33)
1. Authorization and dispatch are atomic with re-evaluation: under the engine's single writer, the engine re-evaluates the action against the current lifecycle state, registry, catalogue, AI-system registration and manifest (a) when the approvals are complete and (b) immediately before signing the dispatch. If either re-evaluation denies, the decision becomes REVALIDATION_DENIED and nothing is dispatched.
2. The decision digest (§8.1) covers every input of the evaluation, including the SHA-384 of the canonical proposal. Approvals bind to one digest.
3. Pending decisions expire (default 15 minutes); authorized decisions that are not dispatched expire (default 5 minutes).
4. When the lifecycle state changes, or the registry, catalogue, AI-system registration or manifest is reloaded, every PENDING_APPROVAL and AUTHORIZED decision moves to REVALIDATION_REQUIRED and is re-evaluated immediately (§9.2).
5. A decision that required approval at any point keeps requiring at least the approvals it required before; revalidation never removes an approval requirement.
6. Freshness of an approval statement is checked when the statement is accepted; an accepted statement remains valid until the decision expires or its digest changes.

**SR-14 Signed approvals and denials** (F-08; V-18, V-19)
1. An approval or denial is accepted only as a signed approval statement (§8.1) that verifies under SR-22, whose principal holds the approver role and is valid, whose verdict is explicit, whose digest equals the current decision digest, and whose `signed_at` is within the freshness window (default 10 minutes) at acceptance.
2. Each statement is accepted once; reuse is recorded as `APPROVAL_REJECTED` with reason `REPLAY`.
3. The number of required approvals is the maximum of: the catalogue requirement M (SR-07.1), the emergency minimum (SR-10.3) and every minimum of the applicable profiles (SR-26.1). Approvals count only from distinct principals.
4. The identity recorded in evidence is the verified principal.
5. Profile P: the classical component of an approval MUST be an `sk-ssh-ed25519@openssh.com` signature with the user-presence flag set, and the post-quantum component an `ml-dsa-87` signature by the same principal (SR-25.5); a classical component of any other key type is rejected. Profile D accepts `ssh-ed25519` for the classical component and declares the residual risk in §15.

**SR-15 Operator commands, assertions and separation of duties** (F-17, F-18; V-07, V-35)
1. Operator commands that change state or trust (`reload`, `resume`, `rotate-segment`, `checkpoint`, `transition`, `evidence-gap`) are accepted only as statements signed with `cai-operator` (§8.2). `archive` and `import-legacy` require the administrative key.
2. Safety assertions (`safety_approved`, `deception_scope_approved`, `clean_baseline_validated`) are accepted only when signed by an approver. Other fact assertions (for example `assets_discovered`) are accepted when signed by an operator or reported by an adapter.
3. Entry conditions evaluate only signed assertions and adapter-signed observations; each is recorded with its signer.

### D. Evidence and state

**SR-16 Event-sourced state, durability and evidence before effect** (F-12, F-17; V-09, V-10, V-21)
1. Evidence is the source of truth; state is derived by replay. The snapshot file is a cache containing the epoch, the sequence number and record hash of the last record it reflects, and the SHA-384 of the snapshot content.
2. Every operation: append the evidence record, `fsync` the file (and, on POSIX, the directory when a segment file is created); then write the snapshot to a temporary file, `fsync` it, replace the snapshot atomically (`os.replace`) and, on POSIX, `fsync` the directory. The snapshot is updated after every append, including records that do not change decision state.
3. Snapshot write failure: retried up to three times; if it still fails, the snapshot is marked stale in the fault file and rebuilt at the next start; three consecutive operations with a failed snapshot write enter SAFE_HALT. The snapshot is opened only by the engine's single writer.
4. Start: verify the evidence (§10.5). If the snapshot is current and its digest matches the replay, continue. If it is behind or missing, rebuild it by replay and record `SNAPSHOT_REBUILT`. If its digest or reference does not match the replay, enter SAFE_HALT.
5. A result is returned to a caller only after its evidence record is durable.
6. Profile P: a single writer inside the engine service serializes all appends. Profile D: a file lock with a 2-second timeout; a timeout returns `REJECTED` with reason `BUSY` (retryable) and is not recorded.
7. Each decision record contains: SHA-384 of the canonical proposal; engine version; deployment identifier; AI-system identity and how it was established; MCP client name and version as declared; digests and versions of the registry index and entries, catalogue, AI-system registration and manifest used; the decision digest; the gate results.

**SR-17 SAFE_HALT and degraded anchoring** (V-16, V-17)
1. SAFE_HALT triggers: evidence write failure; verification failure; snapshot mismatch or repeated snapshot write failure (SR-16.3); expiry of the manifest in use; quota exhausted.
2. In SAFE_HALT every governance call is refused, no decision is authorized or dispatched, and refusals are written only to the fault file and error stream.
3. Admitted in SAFE_HALT: loading a valid newer manifest; signed `rotate-segment`; signed `evidence-gap`; signed `archive`; signed `resume`. Each is recorded when evidence can be written.
4. SAFE_HALT persists across restarts. `resume` is executed only after a full verification passes at the deployment's evidence level; `RESUMED` is recorded with the result.
5. Degraded anchoring (L3): if the external store is unreachable, the engine enters the condition `DEGRADED_ANCHORING`, records it, keeps queuing anchors and continues. After the grace period (default 60 minutes) no new operational decision is AUTHORIZED; observation-only operations continue. When the store is reachable and the queue is anchored, the condition clears and is recorded.

**SR-18 Initialization, epochs and legacy import** (F-03; V-10, V-22)
1. No AI-facing interface initializes, resets, archives or truncates anything.
2. If the evidence of the active epoch is missing or unreadable, AI-facing calls return `NOT_INITIALIZED` and nothing is written. A missing snapshot with valid evidence is rebuilt (SR-16.4).
3. `init` with existing evidence is refused. `archive` (administrative key) closes the epoch: it records `EPOCH_CLOSED` with the final head hash, anchors it at L3, moves the epoch's segments and checkpoints to the archive directory, and opens a new epoch whose genesis record carries the previous epoch identifier and head hash, the highest manifest, registry index, catalogue and registration versions recorded so far, and the cumulative revocation list.
4. `import-legacy` (administrative key) verifies a 0.4.2 `evidence.jsonl` at L1, stores it unchanged as epoch 0 (read-only), and opens epoch 1 whose genesis record carries the epoch-0 head hash and the file's SHA-384.

**SR-19 Checkpoints and evidence levels** (F-11; V-11)
1. The engine signs a `CHECKPOINT` record every 20 records, at segment rotation, at clean shutdown and on a signed `checkpoint` command.
2. The evidence level is stated in the manifest and recorded in every checkpoint; a change of level is a manifest change and therefore visible in evidence.
3. Documentation and outputs MUST NOT describe evidence as immutable or tamper-proof; they MAY say tamper-evident at the declared level against the attackers that level covers (§10.4).

**SR-20 Anchoring and recovery** (V-08)
1. At L3 every checkpoint is anchored in an external append-only store: a Git repository on a remote that the engine host cannot rewrite (protected branch, no force-push). Each anchor record contains the checkpoint and is signed with the anchor key in namespace `cai-anchor`; the anchoring job commits it with a Git commit signed with the same anchoring host's commit key (Git namespace `git`). RFC 3161 tokens MAY be added to anchor records for proof of time.
2. Verification at L3 retrieves the anchor records from the remote, verifies their `cai-anchor` signatures against the anchor key in the manifest, and compares them with the local checkpoints; local copies of anchors are not trusted.
3. Recovery follows §10.6.

### E. Execution

**SR-21 Adapter contract** (F-10; V-26)
See §11. `EXECUTED` is recorded only on a signed adapter report.

### F. Cryptographic implementation

**SR-22 In-process signature verification** (V-18, V-31)
1. The engine verifies SSH signatures in process with the `cryptography` package: it parses the SSHSIG structure; checks magic, version, namespace and hash algorithm (`sha512` required; `sha256` accepted only in profile D, for interoperability); checks that the signature algorithm matches the public-key type; for `sk-ssh-ed25519@openssh.com` checks the application string, the flags (user presence required where SR-14.5 applies) and the signed structure of PROTOCOL.u2f.
2. Key binding: the public key embedded in the SSHSIG MUST equal the key listed in the manifest (or signed index) for the principal and role being exercised; the principal is determined by that key, never by a name in the statement.
3. Interoperability: test vectors produced with `ssh-keygen -Y sign` (Git for Windows and Linux for `ssh-ed25519`; Windows built-in OpenSSH with a FIDO2 token, or Linux with a FIDO2 token, for `sk-ssh-ed25519`) are committed to the repository.
4. The engine executes no external program to verify or sign.
5. The Ed25519 component of engine signatures (checkpoint, dispatch) is produced in SSHSIG format and verifies with `ssh-keygen -Y verify`; the ML-DSA-87 component is carried in the signature envelope of SR-25.
6. `cryptography` is required by the `secure` extra, pinned by version and hash. Without it the engine runs only in profile D at L1 and rejects every signature-dependent operation with `SIGNATURES_UNAVAILABLE`.
7. Canonicalization uses one RFC 8785 implementation inside `cai_engine`, tested against the RFC 8785 test vectors; the approver helper uses the same code.
8. Malformed structures, unsupported key types and any exception during verification are verification failures.

**SR-23 Key lifecycle and review** (V-12)
1. Every key in the manifest has `valid_after` and `valid_before`, at most 12 months apart.
2. Rotation: the new key is added before the old one expires; the old key is then listed with reason `retired`, which ends its validity without review.
3. Compromise: the key is listed with reason `compromised` and `last_known_good`. The engine records `REVIEW_OPENED` for every decision, classification, command, assertion or report signed with that key after `last_known_good`. Review is an overlay flag on the affected item, not a decision state; the decision's lifecycle continues (including adapter reports). A review is closed by an approver-signed statement (`CONFIRMED` or `INVALIDATED`) recorded as `REVIEW_CLOSED`.
4. Engine checkpoint and dispatch keys rotate at least every 12 months; each rotation is a manifest version and is anchored at L3.

**SR-25 Cryptographic agility and hybrid post-quantum signatures**
1. Every signed statement is carried in a signature envelope: `{statement, signatures: [{alg, key_id, value}]}` where `statement` is the canonical bytes, `alg` is one of `ssh-ed25519` (SSHSIG), `sk-ssh-ed25519` (SSHSIG) or `ml-dsa-87` (FIPS 204, pure mode, context string equal to the namespace of §6.3), and `key_id` is SHA-384 over the public key encoding (the SSH wire-format public key blob for `ssh-ed25519` and `sk-ssh-ed25519`, the raw FIPS 204 public key for `ml-dsa-87`). `key_id` is a lookup hint only; verification always uses the key bound to the principal in the signed source, and a mismatch makes the signature invalid.
2. The trust manifest defines, for each key purpose, the required algorithm suite. Default suite for every purpose in 0.5.0: `hybrid` = one classical signature (`ssh-ed25519` or, for approvers in profile P, `sk-ssh-ed25519`) AND one `ml-dsa-87` signature, both by keys bound to the same principal in the manifest. A statement is valid only if every algorithm required by the suite verifies; an extra signature never compensates a missing or invalid one.
3. Suites `classical` (profile D only) and `pq-only` (reserved; not enabled in 0.5.0) exist for agility. A change of suite is a manifest change and is recorded; a downgrade from `hybrid` to `classical` is refused in profile P.
4. ML-DSA-87 signing and verification use `cryptography` (SR-22.6), whose ML-DSA support requires version 48 or later with OpenSSL 3.5 or later (version 47 supported only AWS-LC and BoringSSL builds). Because the library exposes hedged signing only, the start-up self-test uses the NIST ACVP ML-DSA keyGen vectors (seed to public key) and sigVer vectors (external interface, pure mode, with context), plus a sign-verify test with each engine key; cross-implementation vectors produced with OpenSSL 3.5 or later (`pkeyutl` with a context string) are committed and verified; on failure, signature-dependent operations return `SIGNATURES_UNAVAILABLE` and profile P refuses to start.
5. Approvers in profile P sign the approval statement twice with the helper of §8.1: once with the hardware `sk-ssh-ed25519` key (proof of presence) and once with their passphrase-protected ML-DSA-87 key. When OpenSSH composite post-quantum signatures and hardware tokens supporting them are stable, the manifest MAY define a suite that replaces this pair; until then the pair is required.
6. Hash function: new epochs use SHA-384 for record hashes, decision digests, proposal digests and key identifiers. Epoch 0 (legacy import) keeps SHA-256.
7. SLH-DSA (FIPS 205) is reserved for the administrative key and anchor records in a later release, when a vetted, pinned Python binding is available; it is not used in 0.5.0.
8. Migration timelines are defined by the profiles (EU profile §9, USA profile §9). Deployments with `nss = true` are not supported in 0.5.0: CNSA 2.0 requires exclusive use of post-quantum algorithms in its final phase and does not list Ed25519, so the `hybrid` suite is not a CNSA 2.0 suite; the engine refuses to start with `nss = true`.
9. Compromise of either key of a pair (classical or ML-DSA) is treated as compromise of the pair (SR-23.3).

### G. Jurisdiction profiles

**SR-26 Profile interface**
1. A jurisdiction profile defines: its identifier; closed vocabularies for registry and registration fields; the classification function from signed registry and registration data to a profile classification; the profile gates and their outcomes (ALLOW, ESCALATE, DENY) with reason codes; profile thresholds, which may only raise the core thresholds of SR-27; the minimum number of distinct approvals the profile requires for a classification; the minimum `retention_min_days`; `classical_suite_end` (the date from which the `classical` suite is refused for deployments that include the profile); reason-code templates; evidence-retention requirements; the post-quantum migration timeline; its findings, requirements and acceptance tests.
2. Profile gates are evaluated after the core gates; the combined outcome is the strictest (DENY over ESCALATE over ALLOW). A profile cannot change a core outcome to a less strict one, cannot remove a core gate, and cannot accept client-declared input that the core rejects.
3. Profile parameters (thresholds, vocabularies, sector tables) are signed with `cai-catalogue` as part of the catalogue and carry its version.
4. A profile gate result labels its relationship to the instrument as `alignment` or `supports`; it never states `compliant`, `satisfied` or `conformant`.
5. Cross-profile consistency: for a target under both profiles, both evaluations are recorded. For a target under one profile, the engine also records, for audit only, what the other profile would have decided when the registry entry carries the fields that profile needs; a less strict outcome under the applied profile is flagged `PROFILE_DIVERGENCE` in the record but does not change the decision.
6. Each profile is approved, versioned and released with the gates that implement it (mainly G4; tests that need approvals or adapters run in G5 or G7); a profile change after release is a catalogue change and triggers SR-13.4.

### H. Claims

**SR-24 Claims policy**

This is a process requirement, verified by the release review of each gate rather than by an automated test.

1. A requirement is claimed as implemented only when all its acceptance tests pass at an identified commit, on the platforms listed.
2. Results are PASS, FAIL, LIMIT (the test confirms a documented limitation exactly as documented) or NOT TESTED. A missing test is never reported as PASS.
3. Release 0.5.0 implements the temporal-validity term τ (expiry) and revalidation against lifecycle state, registry, catalogue, AI-system registration and manifest, at approval and before dispatch. It does not compute context drift or the T(t) and R(t) terms of D(t) (CAI-Core-Taxonomy §8.7, §8.8); CAI-MX §15 is therefore partly implemented. No document, article or output may state or imply otherwise.

## 8. Signed statement formats

All signed content is canonical JSON (SR-22.7), carried in the signature envelope of SR-25 with the algorithms required for its purpose and the namespace of §6.3. Every statement carries `deployment_id`, `epoch`, `statement_type`, `statement_id` (random 128-bit, accepted once), `signed_at` and `not_after` (at most 15 minutes after `signed_at` for commands and approvals).

### 8.1 Approval statement

1. Decision digest: SHA-384 over the canonical form of the decision identifier; SHA-384 of the canonical proposal; AI-system identifier; operation identifier; parameter digest; targets; registry entry digests and index version; catalogue version; registration version; manifest version; lifecycle state; gate results; declared-context conflicts; required approvals; decision expiry.
2. For each pending decision the engine produces an approval request with the canonical content, its digest and a human-readable summary.
3. The approver runs `cai_engine approval-statement --request <file> --verdict APPROVE|DENY --reason <text>` on their own machine; it writes `{decision_digest, verdict, reason, ...common fields}` signs it with `ssh-keygen -Y sign -n cai-approval` (hardware key) and, where the suite requires it, adds the ML-DSA-87 signature with the approver's post-quantum key; the helper assembles the envelope. Any tool producing the same canonical bytes and valid signatures is acceptable.
4. Review closures and safety assertions use the same format with `statement_type` `review_closure` or `assertion`.

### 8.2 Operator command

`{command, arguments, expected_epoch, ...common fields}`, namespace `cai-operator` (or `cai-admin` for `archive` and `import-legacy`), with command-specific preconditions instead of a global sequence number: `transition` carries `expected_lifecycle_state`; `reload` carries `expected_manifest_version` or the expected index version; `resume` and `evidence-gap` carry `expected_last_seq`, because the log does not advance in SAFE_HALT. `statement_id` single use and `not_after` prevent replay.

### 8.3 Signed sources

The trust manifest (`cai-admin`), registry entries and registry index (`cai-registry`), operation catalogue and AI-system registrations (`cai-catalogue`) are signed whole, each with a monotonic version.

### 8.4 Checkpoint and anchor record

Checkpoint: `{epoch, segment, seq, head_hash, record_count, evidence_level, manifest_version}`, namespace `cai-evidence`. Anchor record: `{deployment_id, epoch, checkpoint, checkpoint_signature, anchored_at, rfc3161_token?}`, namespace `cai-anchor`.

### 8.5 Dispatch, acknowledgement and report

Dispatch: `{decision_id, decision_digest, operation_id, parameter_digest, targets, adapter_id, manifest_version, not_after}`, namespace `cai-dispatch`. Acknowledgement and report: `{decision_id, decision_digest, adapter_id, outcome, result_digest, observed_at}`, namespace `cai-adapter`.

## 9. Decision state machine

### 9.1 States

| State | Terminal | Meaning |
|---|---|---|
| REJECTED | Yes | Invalid request or fail-closed processing |
| BLOCKED | Yes | A gate denied; unclassified target for an operational action; AI system or operation not permitted |
| PENDING_APPROVAL | No | Admissible only with the required signed approvals |
| REVALIDATION_REQUIRED | No | An input changed; re-evaluation is immediate |
| REVALIDATION_DENIED | Yes | Re-evaluation denied |
| EXPIRED | Yes | Pending or authorization window elapsed |
| DENIED_BY_HUMAN | Yes | Valid signed denial |
| AUTHORIZED | No | All gates admit the action now and approvals are valid |
| DISPATCHED | No | The adapter acknowledged the signed dispatch |
| EXECUTED | No | The adapter reported success with a result digest |
| EXECUTION_FAILED | Yes | The adapter reported failure |
| RESULT_VERIFIED | Yes | An independent observation confirmed the result |

SAFE_HALT and DEGRADED_ANCHORING are engine conditions. Review (SR-23.3) is an overlay flag.

### 9.2 Transitions

| From | Event | To |
|---|---|---|
| (new) | Validation fails | REJECTED |
| (new) | Gate DENY; unclassified operational target; system or operation not permitted | BLOCKED |
| (new) | All gates ALLOW and no approval required | AUTHORIZED |
| (new) | Admissible with approval | PENDING_APPROVAL |
| PENDING_APPROVAL, AUTHORIZED | Input change (SR-13.4) | REVALIDATION_REQUIRED |
| REVALIDATION_REQUIRED | Re-evaluation denies | REVALIDATION_DENIED |
| REVALIDATION_REQUIRED | Re-evaluation admits; approval required now or before (SR-13.5) | PENDING_APPROVAL with a new digest; earlier approvals void |
| REVALIDATION_REQUIRED | Re-evaluation admits; no approval ever required | AUTHORIZED with a new digest |
| PENDING_APPROVAL | Approvals complete and re-evaluation admits | AUTHORIZED |
| PENDING_APPROVAL | Approvals complete and re-evaluation denies | REVALIDATION_DENIED |
| PENDING_APPROVAL | Valid signed denial | DENIED_BY_HUMAN |
| PENDING_APPROVAL | Statement for another digest, invalid, revoked or replayed | unchanged; `APPROVAL_REJECTED` recorded |
| PENDING_APPROVAL, AUTHORIZED | Window elapsed | EXPIRED |
| AUTHORIZED | Pre-dispatch re-evaluation denies | REVALIDATION_DENIED |
| AUTHORIZED | Dispatch signed and acknowledged | DISPATCHED |
| DISPATCHED | Signed success report | EXECUTED |
| DISPATCHED | Signed failure report | EXECUTION_FAILED |
| DISPATCHED | Report deadline elapsed | unchanged; `DISPATCH_TIMEOUT` recorded |
| EXECUTED | Independent confirmation | RESULT_VERIFIED |

Records written by 0.4.x as `ACTION_EXECUTED` or `GOVERNED_DECISION_EXECUTED` mean "authorized"; they remain unchanged in epoch 0 (SR-18.4).

## 10. Evidence model

### 10.1 Records

Each record contains `epoch`, `segment`, `seq`, `timestamp`, `event_type`, `prev_hash`, `payload` and `record_hash` (SHA-384 over the canonical record without `record_hash`). State-changing records also contain the digest of the resulting state.

### 10.2 Epochs

An epoch starts with a genesis record (SR-18.3, SR-18.4) containing the administrative key fingerprint and, after the first epoch, the links and highest versions carried forward. Monotonic-version and revocation checks use the values carried forward, so they hold across epochs. Anchors are scoped to an epoch.

### 10.3 Segments

The log is split into segments of configurable size, each ending with a checkpoint and linked by `prev_hash` to the previous segment. Rotation is a signed operator command; closed segments move to the archive directory and remain part of verification.

### 10.4 Evidence levels

| Level | Mechanism | Covers attackers | Detects | Does not detect |
|---|---|---|---|---|
| L1 | Hash chain across segments | Accidental damage | Edit or removal of any record or segment except at the end of the log | Whole-chain rewrite; removal of the most recent records or segments |
| L2 | L1 + signed local checkpoints | Accounts that cannot read the engine checkpoint key (profile P: AI clients, front ends, operators without administrative rights) | L1, plus rewrite of checkpointed records | Removal of the most recent records after the last checkpoint, or of the most recent segment(s) together with their checkpoints; any change by an account that can read the checkpoint key |
| L3 | L2 + every checkpoint anchored externally | L2, plus the engine service account and host administrators, up to the last anchor | L2, plus removal or rewrite of any anchored portion | Records after the last anchored checkpoint |

Profile D runs at L1 or L2 and gives no protection against the account it runs under.

### 10.5 Verification

`verify` checks: genesis records, epoch links and administrative key fingerprints; the hash chain across segments; every checkpoint signature against the checkpoint key valid at that time; that each closed segment ends with a valid checkpoint; that the record count is not below the latest checkpoint; at L3, the remote anchor records and their signatures against the local checkpoints. It reports PASS or the first failure with its location. The engine's own verification (at start and every 5 minutes) enters SAFE_HALT on failure, except that an unreachable anchor store leads to DEGRADED_ANCHORING (SR-17.5). The `cai_verify` tool only reports.

### 10.6 Recovery

1. L3: restore segments from backup up to the latest anchored checkpoint; declare unrecoverable records after it with a signed `evidence-gap` command (sequence range, reason), which also lists the local checkpoints after the gap as retired; rebuild the snapshot by replay; then `resume`.
2. L2: the same procedure from the latest valid local checkpoint; the gap record states `completeness: unproven`.
3. Decisions inside a gap are flagged for review (SR-23.3 mechanism) and treated as unverified.

## 11. Adapter contract

1. Dispatches are signed with the engine dispatch key only. Adapters hold the trust anchor and verify the current trust manifest themselves, so they learn dispatch-key rotation and revocation; they accept only dispatches whose `manifest_version` is not older than the highest they have verified.
2. Adapters are principals in the manifest with permitted operations. The engine accepts acknowledgements and reports only from the adapter named in the dispatch.
3. At most once: `decision_id` is the idempotency key on both sides; second dispatches, acknowledgements or reports are refused and recorded.
4. The adapter refuses a dispatch past `not_after`, for an operation it is not permitted, or with parameters that do not match `parameter_digest`.
5. Unsigned reports are rejected and recorded. Without a report before the deadline, `DISPATCH_TIMEOUT` is recorded; the decision is never assumed executed.
6. RESULT_VERIFIED requires an observation from a source other than the reporting adapter, linked to the decision.
7. Adapter operations are CLI, API and IPC operator-side operations, never exposed to AI clients.

## 12. Interfaces

### 12.1 MCP tools (0.5.0)

| Tool | Purpose | Annotations |
|---|---|---|
| `cai_status` | Engine condition (normal, SAFE_HALT, DEGRADED_ANCHORING), profile, evidence level, lifecycle state, number of pending decisions | readOnlyHint = true, openWorldHint = false |
| `cai_govern` | Submit one proposal (SR-01, SR-07); returns decision identifier, state, gate names, reason codes, decision digest | readOnlyHint = false, destructiveHint = false, idempotentHint = false, openWorldHint = false |
| `cai_decision` | State of one decision by identifier | readOnlyHint = true, openWorldHint = false |
| `cai_verify` | Run verification and report; does not change engine condition | readOnlyHint = true, openWorldHint = true at L3, false otherwise |
| `cai_report` | Last 50 records in summarized form and the latest verification result | readOnlyHint = true, openWorldHint = false |

Annotations are hints to clients and do not replace any control.

### 12.2 IPC operations (profile P)

Front-end accounts: the five operations above. Operator accounts: submission of signed operator commands, approval statements, adapter acknowledgements and reports (at most 64 KiB each). Signed sources (manifest, registry, catalogue, registrations) are never transferred over IPC: they are placed in the protected configuration directory by an administrator and loaded by a signed `reload` command.

### 12.3 Operator CLI

`init`, `archive`, `import-legacy`, `reload`, `resume`, `rotate-segment`, `checkpoint`, `transition`, `evidence-gap`, `approval-statement` (helper, runs on the approver's machine), `verify`, `report` and `crypto-inventory` (lists every key, algorithm, suite and purpose from the manifest; read-only). Every authority-bearing submission is verified as a signed statement regardless of the submitting account.

## 13. Acceptance tests

Path codes: A = Python API, C = CLI, M = MCP, I = IPC (profile P). Every test runs on Linux; tests marked W also run on Windows. Test identifiers are stable across versions; AT-01 to AT-73 are in gate order and AT-74 to AT-82 were added in v0.5, AT-83 to AT-85 in v0.6 and AT-86, AT-87 in v0.7. The Gate column is authoritative.

| Test | Gate | Requirement | Path | Expected result |
|---|---|---|---|---|
| AT-01 | G1 | SR-01 | A, M | Unknown key at any level, wrong type, oversize, excessive depth, more than 64 targets: REJECTED; process continues. |
| AT-02 | G1 | SR-01 | A, C | `confidence` NaN, Infinity, -0.1, 1.1, "0.9", true: REJECTED (CLI parses raw JSON). |
| AT-03 | G1 | SR-01 | M | NaN or Infinity in an MCP request: rejected at the protocol layer or REJECTED by the tool; never evaluated. |
| AT-04 | G1 | SR-01 | A | Invalid syntax for each built-in target type: REJECTED; valid syntax accepted by validation. |
| AT-05 | G1 | SR-01 | A, M | Client-supplied `category`, `destructive`, `blast_radius`, `explainable`, or a profile field such as `eu_transparency_measures`, `genai` or `usa_sector` outside `declared_context`: REJECTED (closes the client-declaration part of F-15). |
| AT-06 | G1 | SR-02 | A | Injected internal exception during evaluation: REJECTED, PROPOSAL_REJECTED recorded, nothing authorized. |
| AT-07 | G1 | SR-03 | M | 31st proposal within a minute: REJECTED; exactly one RATE_LIMITED record for that minute with the correct count. |
| AT-08 | G1 | SR-03 | M | `cai_report` returns at most 50 records. |
| AT-09 | G1 | SR-04 | M | Instruction-like text in description and `ai_system`: only in `untrusted_text`, sanitized, at most 120 characters; reason texts contain no client text; tool descriptions contain no "EXECUTED" for authorization. |
| AT-10 | G1 | SR-05 | M | Tool list equals exactly the five tools of §12.1; HTTP transport start refused. |
| AT-11 | G1 | SR-12 | A | New-decision transitions of §9.2 (REJECTED, BLOCKED, AUTHORIZED, PENDING_APPROVAL) using an unsigned test catalogue and test registration loaded only in profile D test mode; recorder rejects an unknown state name. Later transitions are covered by AT-44 to AT-47 (G5) and AT-65 to AT-69 (G7). |
| AT-12 | G2 | SR-03 | A | At 90 % of quota: proposals REJECTED (QUOTA) and aggregated; engine records (EXPIRED, condition changes) still written from the reserve; at 100 %: SAFE_HALT. Archived segments do not count. |
| AT-13 | G2 | SR-16 | A, W | Process killed after the evidence append and before the snapshot update: next start records SNAPSHOT_REBUILT; state equals replay. |
| AT-14 | G2 | SR-16 | A, W | Snapshot edited (`current_state` or `pending`): start enters SAFE_HALT (closes F-17). |
| AT-15 | G2 | SR-16 | A | Non-state records appended, clean restart: snapshot current; no SNAPSHOT_REBUILT. |
| AT-16 | G2 | SR-16, SR-18 | M | Snapshot deleted with valid evidence: rebuilt, SNAPSHOT_REBUILT recorded, existing evidence prefix unchanged byte for byte. Evidence deleted: NOT_INITIALIZED and nothing written (closes F-03). |
| AT-17 | G2 | SR-16 | A, W | Profile D: two processes contend for the lock: one gets REJECTED (BUSY); no SAFE_HALT; chain verifies. |
| AT-18 | G2 | SR-16 | A, W | Snapshot write fails once: retried, stale mark, rebuilt at next start; fails on three consecutive operations: SAFE_HALT. |
| AT-19 | G2 | SR-17 | A, W | Evidence write failure (read-only file, simulated full disk): REJECTED; SAFE_HALT persisted across restart; refusals only in the fault file. |
| AT-20 | G2 | SR-18 | C | `init` with existing evidence: refused. |
| AT-21 | G3 | SR-22 | A, W | Committed test vectors (`ssh-ed25519` from Git for Windows and Linux; `sk-ssh-ed25519` from a FIDO2 token) verify in process; malformed SSHSIG, wrong namespace, wrong hash algorithm, algorithm–key mismatch, unsupported key type: rejected. |
| AT-22 | G3 | SR-22 | A | Signature whose embedded key differs from the manifest key of the claimed principal: rejected; principal taken from the key, not from any name. |
| AT-23 | G3 | SR-22 | A | Engine signing primitive in namespaces `cai-evidence` and `cai-dispatch` produces signatures whose Ed25519 component `ssh-keygen -Y verify` accepts and whose ML-DSA-87 component OpenSSL 3.5 or later verifies with the same context string; RFC 8785 test vectors pass. |
| AT-24 | G3 | SR-22 | A | Without `cryptography`: profile D, L1; signature-dependent operations return SIGNATURES_UNAVAILABLE. |
| AT-25 | G3 | §6.2, SR-23 | A | Older manifest submitted: TRUST_MANIFEST_REJECTED, engine keeps running; manifest omitting a revocation: rejected; revoked key re-listed: still rejected; manifest in use expires: SAFE_HALT, newer manifest admitted in SAFE_HALT; key past `valid_before` or with validity over 12 months: rejected. |
| AT-26 | G3 | §6.1, §6.4 | A, W | Trust anchor, parent directory or engine code directory modifiable by a non-permitted account (Windows: write, WRITE_DAC through ownership, DELETE_CHILD on parent; POSIX: mode, unreviewed ACL): manifest P → engine refuses to start; manifest D → L1 and TRUST_ANCHOR_UNPROTECTED. Code file changed: profile P refuses to start. |
| AT-27 | G3 | SR-15 | C | Unsigned `transition` or `resume`: refused; replayed `statement_id`, expired `not_after`, wrong `expected_lifecycle_state`, stale `expected_last_seq` on `resume`: refused; valid commands under concurrent proposal load: accepted. |
| AT-28 | G3 | SR-15 | A | `safety_approved` signed by an operator key: refused; signed by an approver: accepted; entry condition satisfied only by signed assertions. |
| AT-29 | G3 | SR-17 | C | In SAFE_HALT: the commands of SR-17.3 admitted, all others refused; `resume` after a failing verification refused, after a passing one RESUMED. |
| AT-30 | G3 | SR-18 | C | `archive` signed by an operator key: refused; by the administrative key: EPOCH_CLOSED; new genesis links to the previous head and carries versions and revocations; older manifest or registry index after archive: rejected. |
| AT-31 | G3 | SR-18 | C | `import-legacy` of a 0.4.2 `evidence.jsonl`: epoch 0 stored unchanged; epoch 1 genesis carries its head hash and file hash; a modified legacy file fails L1 verification and is refused; imported records verify with SHA-256. |
| AT-32 | G4 | SR-06 | A | Registry entry with missing or invalid signature: ignored; REGISTRY_ENTRY_REJECTED. |
| AT-33 | G4 | SR-06 | A | Registry index older than the recorded version or the manifest minimum: rejected; emergency entry published by a registry authority without a new manifest: accepted. |
| AT-34 | G4 | SR-06 | A | Free-text sector or missing jurisdiction in an entry: entry invalid. |
| AT-35 | G4 | SR-07 | A | Operation `ot.relay.modify` (catalogued operational, permitted in HARDEN) on a registered energy safety component (run under each profile), lifecycle HARDEN, confidence 0.97, non-empty explanation: PENDING_APPROVAL; with any combination of client inputs it is never AUTHORIZED without approval (closes F-01 and F-15). |
| AT-36 | G4 | SR-07 | A | `blast_radius` equals the sum of `asset_group_size`; above threshold: PENDING_APPROVAL. |
| AT-37 | G4 | SR-08 | A | Unregistered AI system, or operation outside its permitted set: BLOCKED. |
| AT-38 | G4 | SR-08, SR-26 | A | Registration `explainable = true` with empty explanation: denied. Every baseline regulatory gate remains reachable from signed sources; the gate-by-gate tests are the acceptance tests of the EU and USA profiles (§11 of each). |
| AT-39 | G4 | SR-09, SR-11 | A | Client declares USA for a target registered as EU: EU applied; DECLARED_CONTEXT_CONFLICT escalation (closes F-16). |
| AT-40 | G4 | SR-09 | A | Two targets, one EU and one USA, one requiring approval: strictest outcome and union of approvals. |
| AT-41 | G4 | SR-10 | A | Observation-only operation on an unclassified target, other gates passing: AUTHORIZED with UNCLASSIFIED_OBSERVE and the manifest's `default_jurisdiction` recorded. |
| AT-42 | G4 | SR-10 | A | Operational action on an unclassified target: BLOCKED (UNCLASSIFIED_TARGET); no approval request. |
| AT-43 | G4 | SR-11 | A | Conflicts compared only on declared fields; sixth conflict within an hour: REJECTED (CONFLICT_RATE), aggregated; decision digests unaffected by the counter. |
| AT-44 | G5 | SR-13 | A | Scenario T-09: pending containment, transition to EVICT: REVALIDATION_REQUIRED then REVALIDATION_DENIED; approval for the old digest: APPROVAL_REJECTED (closes F-07). |
| AT-45 | G5 | SR-13 | A | Registry, catalogue, registration or manifest reload while pending: REVALIDATION_REQUIRED; admissible re-evaluation: PENDING_APPROVAL with new digest, earlier approvals void, approval requirement never removed. |
| AT-46 | G5 | SR-13 | A | AUTHORIZED decision, then lifecycle transition before dispatch: REVALIDATION_REQUIRED then REVALIDATION_DENIED or new digest per §9.2. |
| AT-47 | G5 | SR-13 | A | Pending window elapsed: EXPIRED; authorized but not dispatched within 5 minutes: EXPIRED. |
| AT-48 | G5 | SR-14 | A, C, W | Statement unsigned, from an unlisted, expired or revoked key, with a `git` namespace signature, for another digest, without verdict, older than the freshness window at acceptance, or (profile P) whose classical component is not an `sk-ssh-ed25519` signature with user presence: APPROVAL_REJECTED. |
| AT-49 | G5 | SR-14 | A | Replay of a valid statement: APPROVAL_REJECTED (REPLAY). |
| AT-50 | G5 | SR-14 | A, C, W | Valid statement from an approver: AUTHORIZED after re-evaluation; evidence records the verified principal. |
| AT-51 | G5 | SR-13, SR-14 | A | M of N = 2: two statements from one principal do not satisfy it; two distinct principals accepted 12 minutes apart, both within the decision expiry: satisfied. |
| AT-52 | G5 | SR-14 | A | Valid signed denial: DENIED_BY_HUMAN with reason. |
| AT-53 | G5 | SR-10 | A | Emergency classification: max(M, 2) distinct approvals required; after `valid_until` the target is unclassified and EMERGENCY_CLASSIFICATION_EXPIRED lists the decisions. |
| AT-54 | G5 | SR-23 | A | Key declared compromised: REVIEW_OPENED for each decision, classification, command, assertion and report signed after `last_known_good`; adapter reports for affected decisions still recorded; review closed by approver statement; retired key: no review. Only the ML-DSA key of a pair declared compromised: the classical key of the same pair is refused as well, and review opens for statements signed with either key (SR-25.9). |
| AT-55 | G5 | SR-16 | A | A governed decision record contains every field of SR-16.7, with digests matching the signed sources in use. |
| AT-56 | G6 | SR-19 | A | Checkpoints written every 20 records, at segment rotation, at clean shutdown and on signed command. |
| AT-57 | G6 | SR-19 | A | L2: rewrite of checkpointed records detected; removal of a middle segment detected; removal of the most recent segment together with its checkpoints NOT detected (LIMIT). |
| AT-58 | G6 | SR-19 | A | Manifest lowering the evidence level: change recorded and reported by `verify`. |
| AT-59 | G6 | SR-20 | A | L3: removal of recent anchored segments detected against the remote; local anchor copies altered: detected; anchor record with an invalid `cai-anchor` signature: verification failure; anchor commits signed in Git namespace `git`. |
| AT-60 | G6 | SR-17 | A | L3 store unreachable: DEGRADED_ANCHORING recorded, operations continue; after the grace period operational decisions are not AUTHORIZED, observation continues; store reachable again: condition cleared. |
| AT-61 | G6 | SR-20 | C | Recovery at L2 and L3 per §10.6: EVIDENCE_GAP recorded, later checkpoints retired, `resume` succeeds after verification; gap decisions flagged for review. |
| AT-62 | G6 | SR-18, SR-20 | A | Epoch archive at L3: earlier anchors validated against the closed epoch, not reported as removal. |
| AT-63 | G6 | SR-23 | A | Checkpoint key rotation: new manifest, anchored; checkpoints before and after rotation verify with the key valid at their time. |
| AT-64 | G6 | SR-19 | A | Documentation and tool outputs contain no "immutable" or "tamper-proof" for evidence (text scan of the package and docs). |
| AT-65 | G7 | SR-21 | A | No EXECUTED without a signed adapter report; unsigned, wrong-adapter or duplicate reports rejected and recorded. |
| AT-66 | G7 | SR-21 | A | Reference adapter refuses: replayed dispatch, expired dispatch, parameters not matching `parameter_digest`, dispatch signed with the checkpoint key, dispatch with a `manifest_version` older than verified; manifest signed only with the Ed25519 administrative key; adapter learns a dispatch-key rotation from the manifest. |
| AT-67 | G7 | SR-13 | A | AUTHORIZED containment; lifecycle moves to EVICT before dispatch: pre-dispatch re-evaluation denies; nothing dispatched; REVALIDATION_DENIED. |
| AT-68 | G7 | SR-21 | A | No report before the deadline: DISPATCH_TIMEOUT recorded; decision stays DISPATCHED. |
| AT-69 | G7 | SR-21 | A | RESULT_VERIFIED requires an observation from another source; a second report from the same adapter does not produce it. |
| AT-70 | G8 | §6.5 | I, W | Peer identity from the operating system; declared identity mismatch recorded; remote pipe client rejected; pipe and socket permissions as specified; static check: no `recv()`, `send()` or `pickle` on the IPC path; 64 KiB message limit; an attempt to submit a manifest, registry or catalogue over IPC is refused. |
| AT-71 | G8 | SR-08 | I | AT-37 repeated over IPC with identity from the account. |
| AT-72 | G8 | SR-16 | I | 200 concurrent proposals from 8 accounts (test manifest raises rate limits): chain verifies; record count equals 200 decision records plus the CHECKPOINT records (one per 20 records) plus the start, condition and expiry records the test enumerates. |
| AT-73 | G8 | Regression | A, W | The 25 baseline unit tests rewritten per the mapping committed in G1; the evaluation scenarios committed in G0 re-run: T-09 PASS; T-08 LIMIT at L1, PASS at L3. |
| AT-74 | G3 | SR-25 | A, W | Hybrid suite: statement with valid Ed25519 and valid ML-DSA-87: valid; missing ML-DSA, invalid ML-DSA, missing Ed25519, or the two signatures by keys of different principals: invalid; an extra valid signature does not compensate a missing one; a wrong `key_id` with otherwise valid signatures: invalid; key identifiers are SHA-384 over the defined encodings. |
| AT-75 | G3 | SR-25 | A, W | ML-DSA-87 ACVP keyGen and sigVer vectors and OpenSSL cross-implementation vectors pass on the pinned Linux and Windows wheels (key generation does not raise UnsupportedAlgorithm); a corrupted vector makes the self-test fail: SIGNATURES_UNAVAILABLE, profile P refuses to start. |
| AT-76 | G3 | SR-25 | A | ML-DSA signature with a context string different from the namespace: invalid. |
| AT-77 | G3 | SR-25 | A | Manifest downgrading a purpose from `hybrid` to `classical` in profile P: refused and recorded; in profile D: accepted and recorded. |
| AT-78 | G5 | SR-25, SR-14 | A, C, W | Profile P approval with only the hardware Ed25519 signature, or only the ML-DSA signature: APPROVAL_REJECTED; with both: accepted. |
| AT-79 | G6 | SR-25 | A | Checkpoint and anchor records carry hybrid signatures; removing the ML-DSA component makes verification fail. |
| AT-80 | G2 | SR-25 | A | Record hashes and proposal digests of a new epoch use SHA-384 (decision digests are checked in AT-55; key identifiers in AT-74; the epoch-0 SHA-256 case in AT-31). |
| AT-81 | G4 | SR-26 | A | A profile parameter set that would relax a core gate (for example an ALLOW overriding a core ESCALATE): refused at catalogue load. A profile gate result never uses the words compliant, satisfied or conformant (text scan). |
| AT-82 | G4 | SR-26 | A | Target registered under both EU and USA: both evaluations recorded, strictest applied; target under one profile with fields for the other: PROFILE_DIVERGENCE flagged when the applied profile is less strict, decision unchanged. |
| AT-83 | G3 | §6.1, SR-25 | A | A manifest signed only with the Ed25519 administrative key, or declaring `classical` for `cai-admin`: rejected at first load, on a fresh installation and after restart (the adapter side is tested in AT-66). |
| AT-84 | G4 | SR-27 | A | Each core gate of the SR-27 table triggers with its outcome and reason code; a catalogue or profile parameter set making a fixed minimum less strict is refused; confidence 0.79 is denied under every profile. |
| AT-85 | G3 | §12.2 | A | A manifest with 40 principals, a revocation list of 500 entries and hybrid keys loads from the protected directory (the refusal of signed sources over IPC is tested in AT-70). |
| AT-86 | G3 | §12.3 | C | `crypto-inventory` lists every key, algorithm, suite and purpose of the manifest and writes nothing to evidence. |
| AT-87 | G3 | SR-25.8 | A | Manifest with `nss = true`: the engine refuses to start and writes the reason to the fault file. |

## 14. Traceability

| Requirement | Findings | CAI principle |
|---|---|---|
| SR-01 to SR-05 | F-02, F-04, F-05, F-09, F-10, F-13, F-14 | Fail-safe and deterministic evaluation (CAI-MX §16, §18); anti-contamination: untrusted content never gains authority |
| SR-06 to SR-11 | F-01, F-06, F-15, F-16 | ESA is supplied by signed environmental sources, not by the governed party (CAI-Core-Taxonomy §8.5, §8.6) |
| SR-12, SR-13 | F-07, F-10 | Decision integrity condition (Taxonomy §8.6); enforcement mapping and timing (CAI-MX §13, §14); revalidation, partly (CAI-MX §15) |
| SR-14, SR-15, SR-23 | F-08, F-17, F-18 | Human authority is final, attributable and separated by role |
| SR-16 to SR-20 | F-03, F-11, F-12, F-17 | Integrity and self-protection of evidence |
| SR-21 | F-10 | Evidence states only what happened |
| SR-22 | — | The verifier is part of the trusted base |
| SR-24 | — | Claims follow evidence |
| SR-25 | F-11 | Long-term integrity of evidence and authority against future cryptanalysis |
| SR-27 | F-02, F-15 | Fail-safe gates of the core apply under every profile (CAI-MX §18) |
| SR-26 | F-01, F-16 | Regional overlays extend the core and never redefine it (CAI-Core-Taxonomy §3) |

## 15. Residual risks

- Compromise of the administrative key compromises the deployment.
- Compromise of the engine service account (profile P), or of the account running profile D, allows forging checkpoints and dispatches until rotation; L3 limits rewriting of anchored history. Engine, adapter and anchor keys are unattended keys without passphrase.
- Confidence, explanation text, drift score and provenance remain declared by the AI client; they can only deny or escalate.
- Profile D: the AI-system identity is declared; an AI client with shell access under the same account can use the operator's SSH agent or unprotected keys to sign statements. Profile D MUST NOT be connected to real effects (§2.2); hardware approver keys are recommended even in D.
- A signed adapter report proves what the adapter states; RESULT_VERIFIED requires independent observation.
- Context drift and the T(t) and R(t) terms of D(t) are not computed (SR-24.3).
- Thresholds are engineering defaults.
- ML-DSA implementations are recent; the hybrid suite keeps classical security if an ML-DSA flaw is found, and post-quantum security if Ed25519 is broken, for statements signed with the `hybrid` suite. Profile D deployments using the `classical` suite, epoch 0 (legacy evidence) and Git anchor commits remain classical; post-quantum protection of anchors comes from the hybrid anchor records.
- Hardware tokens provide presence only for the Ed25519 part of an approval; the ML-DSA part relies on passphrase protection on the approver's machine until post-quantum hardware tokens are available.
- An AI client can consume its rate budget and conflict allowance; this degrades availability, not integrity.
- The Python runtime, `cryptography` and the operating system are part of the trusted base; §6.4.3 detects modification of installed files but not compromise of the running interpreter.

## 16. Implementation plan

Each gate is a separate change: owner approval of the gate's scope, one signed commit, its tests passing on the listed platforms, an independent review, and release notes listing requirements demonstrated, PASS/LIMIT/NOT TESTED results and the commit. A gate may not weaken a control of an earlier gate. Versions follow PEP 440 and are defined once in `cai_engine/__init__.py`.

| Gate | Version | Scope | Tests |
|---|---|---|---|
| G0 | (no engine change) | This specification; the evaluation scenarios (T-01 to T-10) and their script under `CAI-Engine/implementation/tests/scenarios/`; baseline report at b52935e | Baseline run recorded |
| G1 | 0.5.0a1 | State machine and recorder; strict validation with built-in target grammar; rejection of client-supplied owned fields; fail closed; rate limits; output policy; tool contract and stdio-only transport; single version source; profile D test mode with unsigned test catalogue and registration; rewrite of the 25 baseline tests with an old-to-new mapping | AT-01 to AT-11 |
| G2 | 0.5.0a2 | Event-sourced evidence and snapshots; durability; evidence before effect; quotas; SAFE_HALT; no initialization from AI-facing interfaces; genesis record; profile D locking | AT-12 to AT-20, AT-80 |
| G3 | 0.5.0a3 | Signature envelope and hybrid suites (Ed25519 + ML-DSA-87); `crypto-inventory`; `nss` refusal; signature verification and engine signing; RFC 8785; trust anchor, protected paths and code integrity; trust manifest, revocation, key validity; signed operator commands and assertions; SAFE_HALT command set; epoch archive; legacy import | AT-21 to AT-31, AT-74 to AT-77, AT-83, AT-85 to AT-87 |
| G4 | 0.5.0a4 | Signed registry and index; operation catalogue; AI-system registration; jurisdiction and multiple targets; unclassified targets; declared-context conflicts; profile interface; EU and USA profiles | AT-32 to AT-43, AT-81, AT-82, AT-84; EU-AT-01 to EU-AT-12, EU-AT-15; USA-AT-01 to USA-AT-03, USA-AT-05 to USA-AT-09, USA-AT-12 to USA-AT-14, USA-AT-17, USA-AT-18 |
| G5 | 0.5.0a5 | Signed approvals and denials; M of N; revalidation of pending and authorized decisions; expiry; emergency classification; compromise review; decision record content | AT-44 to AT-55, AT-78; EU-AT-14; USA-AT-10, USA-AT-15, USA-AT-16 |
| G6 | 0.5.0a6 | Segments and checkpoints; evidence levels; external anchoring; degraded anchoring; recovery; epoch anchoring; checkpoint key rotation | AT-56 to AT-64, AT-79 |
| G7 | 0.5.0b1 | Adapter contract with dispatch key; pre-dispatch re-evaluation; reference test adapter; result verification | AT-65 to AT-69; EU-AT-16; USA-AT-11 |
| G8 | 0.5.0 | Profile P: engine service account, one front end per AI-system account, IPC with operating-system identity; full adversarial and regression run on Linux and Windows | AT-70 to AT-73; EU-AT-13; USA-AT-04; then a full re-run of AT-01 to AT-69, AT-74 to AT-87 and both profiles' tests |

Each test's gate is the gate in which every capability it needs exists; the profile D test mode of G1 (unsigned test catalogue and registration) is removed from builds for profile P.

## 17. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Owner | Antonio José Socorro Marín | Pending | |

## Appendix A — Disposition of the v0.3 review (V-01 to V-39)

| Item | Disposition |
|---|---|
| V-01 | §13 and §16 renumbered by gate; AT-11 limited to G1 transitions; built-in target grammar and test-mode catalogue in G1; AT-12 uses engine records for the reserve; segments moved to G6; AT-23 tests the signing primitive; compromise review moved to G5 (AT-54); emergency approvals moved to G5 (AT-53). |
| V-02 | §6.1.3: profile P refuses to start; profile D degrades to L1. SR-17 no longer lists the trust-anchor check. |
| V-03 | SR-13.1, SR-13.4, §9.2: AUTHORIZED revalidated on input change and immediately before dispatch; AT-46, AT-67. |
| V-04 | §6.5: no object deserialization; explicit pipe security descriptor with remote clients rejected; socket directory 0750; identity from the operating system; one front end per AI-system account; AT-70. |
| V-05 | SR-01.6, SR-08.1, SR-08.2: `human_disclosed` and `explainable` in the registration; client values rejected; AT-05, AT-38. |
| V-06 | §6.2.1, SR-06.4: manifest carries minimum versions; signed registry index carries digests; AT-33. |
| V-07 | §8.2: command-specific preconditions; global sequence only for `resume` and `evidence-gap`; AT-27. |
| V-08 | §6.3, SR-20.1: Git commits in namespace `git`; anchor records signed in `cai-anchor` and verified; AT-59. |
| V-09 | AT-15 reworded to match SR-16. |
| V-10 | SR-16.4, SR-18.2: missing snapshot rebuilt; NOT_INITIALIZED only without evidence; AT-16. |
| V-11 | §10.4: L1 detects middle-segment removal; L2 limitation limited to the most recent segments; AT-57. |
| V-12 | SR-23.3: review as overlay flag with closure; removed from §9. |
| V-13 | AT-35 states lifecycle, confidence, explanation and "never AUTHORIZED without approval". |
| V-14 | §4: reproduction conditions stated (confidence 0.97, explanation "x"). |
| V-15 | §10.2, SR-18.3: versions and revocations carried across epochs; AT-30. |
| V-16 | SR-17.3: commands admitted in SAFE_HALT; SR-03.3, SR-03.4: QUOTA aggregated, archive excluded; SR-17.5: degraded anchoring instead of halt; AT-29, AT-60. |
| V-17 | §6.2.2: older manifest rejected without halting; AT-25. |
| V-18 | SR-22.1, SR-22.2: algorithm–key match and key binding; AT-22. |
| V-19 | SR-14.5: hardware approver keys with user presence in profile P; §15 residual for D. |
| V-20 | §6.1.2, §6.4.3: Authz effective access with ownership, DELETE_CHILD, POSIX ACL detection, code directories and code manifest; AT-26. |
| V-21 | SR-16.2, SR-16.3: `fsync` of files and directories; snapshot write failure handling; AT-18. |
| V-22 | SR-18.4: signed legacy import as epoch 0; AT-31. |
| V-23 | SR-06.2 jurisdiction mandatory; SR-09.2 per-target evaluation; AT-40. |
| V-24 | §8.1.1: canonical proposal hash in the decision digest. |
| V-25 | SR-13.6: freshness checked at acceptance; AT-51. |
| V-26 | §11.1: adapters verify the manifest; AT-66. |
| V-27 | SR-11.3: conflict limit as REJECTED rate limit, not a decision input; AT-43. |
| V-28 | SR-10.1, AT-41: state named (AUTHORIZED). |
| V-29 | AT-72: counting rule stated. |
| V-30 | SR-22.3: `sk` vectors from a FIDO2 token via Windows built-in OpenSSH or Linux, not from Git for Windows. |
| V-31 | SR-22.7: one internal RFC 8785 implementation with the RFC test vectors, shared with the approver helper. |
| V-32 | SR-10.3: max(M, 2). |
| V-33 | SR-13.5 and §9.2: approval requirement never removed; explicit transition for systems that never required approval. |
| V-34 | §3: MCP revision pinned in G1 release notes. |
| V-35 | SR-15.1, SR-15.2: safety assertions by approvers; `archive` and `import-legacy` by the administrative key. |
| V-36 | SR-12: mapping to CAI-MX §13 outcomes (REVALIDATION_DENIED ↔ REVOKE); tests renumbered in order. |
| V-37 | SR-02.2 cites SR-03.3 and SR-03.4. |
| V-38 | SR-03.3: when aggregated records are written. |
| V-39 | §6.3: custody of human keys is a provisioning check by the owner; the engine checks key type and user presence. |

Earlier dispositions (A-01 to A-09 and R-01 to R-38) are recorded in v0.3 Appendix A and remain in force except where this table supersedes them.

## Appendix B — Disposition of the v0.5 review (W-01 to W-30)

| Item | Disposition |
|---|---|
| W-01 | §2.1: post-quantum signatures removed from out of scope; SLH-DSA, `pq-only` and national security systems listed instead. |
| W-02 | §6.1.1, §6.1.4, §6.2.1: hybrid administrative keys and pinned `hybrid` suite in the trust anchor; fingerprint over both keys; key pairs and per-purpose suites per principal; AT-83, AT-66. |
| W-03 | SR-14.5, §6.2.1, §6.3, AT-48: classical component `sk-ssh-ed25519`, post-quantum component ML-DSA-87. |
| W-04 | SR-27: normative core gate table; core floor 0.80; profile floors at or below it removed; AT-84; EU-AT-09 and USA-AT-05 reworded. |
| W-05 | §12.2: signed sources not transferred over IPC; revocations by `key_id`; AT-85. |
| W-06 | SR-25.4, AT-75: ACVP keyGen and sigVer, sign-verify self-test; library version facts; Windows wheels. |
| W-07 | SR-25.1, SR-25.9, AT-74: key encodings, `key_id` as lookup hint, pair compromise. |
| W-08 | SR-25.4, AT-23: OpenSSL 3.5 cross-implementation vectors for ML-DSA. |
| W-09 | SR-25.8, §6.2.1: no claim that the hybrid suite meets CNSA 2.0; `nss` field; `nss = true` refused. |
| W-10 | USA profile USA-SR-15, §9: IR 8547 summary corrected; Ed25519 relevant date 2035. |
| W-11 | USA profile §4 and USA-F-10: Transportation SRMA DHS and DOT. |
| W-12 | USA profile §3, USA-F-09: NSM-22 review under Executive Order 14239. |
| W-13 | USA profile USA-SR-14, USA-SR-15, USA-AT-17, USA-AT-18. |
| W-14 | USA profile §7: CAI interpretation of the four gates; USA-SR-04, USA-SR-11, USA-SR-12; USA-AT-04, USA-AT-16. |
| W-15 | USA profile USA-SR-06: presence check labelled `supports`; core explainability gate applies to generative systems. |
| W-16 | USA-AT-14 split (USA-AT-15 in G5); AT-80 restricted to record hashes and proposal digests. |
| W-17 | EU profile §6.3: target-based rule labelled CAI policy; legal classification through `eu_annex_iii_areas`. |
| W-18 | EU profile EU-F-03 restated (Art. 12 ALLOW and Art. 50 "transparency satisfied"). |
| W-19 | EU profile EU-SR-11 to EU-SR-14; SR-26.1 minimum approvals as a profile output. |
| W-20 | SR-01.6, SR-04.3: core-owned field names only; profile fields by reference; reason-code templates. |
| W-21 | EU profile EU-SR-09, §9: CAI policy label; 1 January 2031; full 2026 milestone. |
| W-22 | §6.2.1 `retention_min_days`; profiles enforce minimums; retention otherwise a process control. |
| W-23 | EU profile §3: Art. 111(2) wording; Omnibus effect to verify. |
| W-24 | EU profile §5 and §6: `eu_art6_3_assessment_ref`. |
| W-25 | EU profile §5: `eu_transparency_measures` with provider and deployer duties separated. |
| W-26 | §6.3: approver row aligned with SR-25.2. |
| W-27 | SR-22.1: epoch-0 clause removed. |
| W-28 | §3, SR-06.2, SR-09: jurisdiction text removed; `default_jurisdiction` in the manifest; section order A to H; `crypto-inventory` in §12.3. |
| W-29 | Profiles: post-action evidence record at window expiry; SRMA naming tested in G5 (USA-AT-10). |
| W-30 | §15: residual qualified for profile D classical, epoch 0 and Git commits. |

Repository findings raised by this review (outside the specification): `REGULATORY-BASIS.md` (NSM-22 status, Art. 111(2) wording) and `usa_sectors.py` (Transportation SRMA) need correction; they are tracked as USA-F-09, USA-F-10 and EU profile §3.

## Appendix C — Disposition of the final consistency review of v0.6 (X-01 to X-16)

| Item | Disposition |
|---|---|
| X-01 | EU-AT-13 and USA-AT-04 (profile P) moved to G8. |
| X-02 | AT-85 limited to the protected-directory load; IPC refusal added to AT-70. |
| X-03 | SR-14.3: required approvals are the maximum of catalogue, emergency and profile minimums. |
| X-04 | AT-54 tests compromise of one key of a pair. |
| X-05 | SR-27: fixed minimums that a catalogue can only tighten; AT-84. |
| X-06 | EU profile: two-person rule relabelled CAI policy aligned to Art. 14(5). |
| X-07 | AT-38 cites the profile test tables. |
| X-08 | AT-05 uses current profile field names. |
| X-09 | `crypto-inventory` in G3 scope; AT-86. |
| X-10 | AT-87 (`nss`); AT-41 checks `default_jurisdiction`. |
| X-11 | Reason-code column in SR-27. |
| X-12 | SR-26.1 defines `classical_suite_end`; both profiles use it. |
| X-13 | SR-06.5: profile manifest requirements re-checked at registry reload. |
| X-14 | USA-AT-09 asserts `USA_OT_SAFETY`; USA-SR-08 wording. |
| X-15 | EU-F-10 added for the Art. 111(2) wording in `REGULATORY-BASIS.md`, closed in G4. |
| X-16 | "AUTHORIZED" statements reworded to "not escalated (or not blocked) by this gate". |
