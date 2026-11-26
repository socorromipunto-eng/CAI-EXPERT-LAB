# ADR-CAI-G0-001 — Reconcile existing security architecture before E2-B

| Field | Value |
|---|---|
| Change ID | CHG-CAI-ARCH-G0-2026-10-29 |
| Status | PROPOSED / HOLD — not owner-adjudicated |
| Record date | 2026-10-29 UTC; new record, not a historical approval |
| Baseline | main, 80cd71e1620c5c580f6697742f520d329fa13709 |
| Historical reference | b52935e93237eccdcab3e58aa23d48ddf4958c43; engine0.4.2 security baseline, not re-executed here |
| Owner and human decision authority | Antonio José Socorro Marín |
| Preparation | AI-assisted architecture/technical/governance self-review; independent human review pending |
| Boundaries authorised by current user request | External reconciliation documents and evidence matrices only |
| Exclusions | Runtime/source edits, account/ACL policy, installs, keys, execution of project code, staging, commits, push and production |

## 1. Context and sources of truth

AGENTS.md, AI-GOVERNANCE.md, CORE and the licence retain their authority. The security specification CAI-ENG-SEC-001 Core v0.8 and EU/USA profiles v0.4 already define a proposed 0.5.0 architecture. Their approval tables are pending. Publication or merge does not prove architecture approval. This ADR adds an assessment of those proposals against 80cd71e; it changes none of them.

The seven defensive lifecycle states and the twelve proposed decision states are separate state spaces. SAFE_HALT and DEGRADED_ANCHORING are engine conditions; compromise review is an overlay. Neither is an eighth defensive lifecycle state. D/P is a deployment/trust axis; EU/USA is a jurisdiction axis; sector and asset safety are further independent dimensions.

## 2. Current evidence and deltas

The 501-file audit snapshot matches80cd71e. Current main was rechecked and remains unchanged. Existing GitHub CI run 40808132963 has 7/7 successful jobs, with 698 pass / 7 xfail in its engine suite. This is 0.4.2 regression evidence, not execution of the 87 proposed Core acceptance tests,34 profile tests or original T01–T10scenario scripts.

Strict type validation, unknown-jurisdiction rejection, refusal to reinitialise existing evidence and approval revalidation are repaired. They are not automatically full acceptance of SR-01/09/13/18. Missing target capabilities include signed authority/context, complete decision lifecycle/expiry, event-sourced durable state, runtime crypto/custody, external anchoring, authenticated IPC and adapters. The SR matrix records each delta independently.

The original G0 in specification §16 requires scenarios T01–T10, their scripts under implementation/tests/scenarios and a baseline report at b52935e. That path is not present in the verified current tree. Only references to some scenarios, such as T08/T09, are visible. Their exact historical scripts and raw baseline evidence were not recovered here. This dossier does not silently replace that criterion or claim a baseline run.

## 3. Proposed architecture disposition

Recommend preserving the existing architecture direction and staging through G0–G8, with immediate scope restricted to development/research. Profile P remains unavailable until its required gates and evidence pass. No current same-process engine is relabelled as an already implemented profile D from 0.5.0: D is the recommended design target, not a new capability claim.

Authority flows from owner-controlled configuration to purpose-bound signed manifest, registry, catalogue and AI registration. A request supplies an operation and targets, not their authoritative risk classification. CLI, MCP, IPC and Python API must converge on one validated decision path. The MCP front end has no keys or authority to approve. For P it is separated from the engine service by accounts, permissions and OS-authenticated IPC; logical separation alone is insufficient.

The decision coordinator evaluates core gates then each applicable jurisdiction profile, preserving the strictest outcome and the union/maxima of required approvals. Human approvals bind the exact decision digest, principal and verdict. State/policy/source changes invalidate or re-evaluate decisions as specified. Re-evaluation happens before authorisation and immediately before signed dispatch under the single writer.

The event log is the state source of truth; snapshots are validated caches. Evidence is durable before a result is returned or effect is admitted. Each permitted adapter validates dispatch identity, parameters, manifest version, deadline and single-use binding. ACK does not mean execution; an execution report does not mean independent result verification. The first adapter remains a separately authorised test adapter, not a production OT connector.

## 4. Scope of E2-B

E2-B is mapped to SR-13/14/15/22/23, trust architecture §§6.1–6.5 and profile P gate G8. The earlier SID observation is evidence of the collector's process context only. It installs no policy and grants no approval role. Runtime signing is separate from the owner's existing Git signing key and OpenSSH passphrase workflow. This ADR does not modify either.

E2-B must not become a Windows-only approval mechanism. First define authority-bearing statements, principal/role binding, replay/expiry, protected directories and denial/recovery behaviour. Then implement and qualify the selected Windows/POSIX adapters under their individual gate. A username, SID, process token or --by label alone is not the complete approval contract.

## 5. Temporal interpretation requiring explicit adjudication

SR-13.6 states that statement freshness is checked at acceptance and an accepted approval remains valid until decision expiry or digest change. Pending and authorised decision windows are different. The common signed-statement not_after in §8, key/manifest validity, dispatch deadline and revocation must not be conflated with that accepted-approval rule. Preserve these semantics unless a specific reviewed change is adopted.

A lab that checks an expires_at before an effect may need a final validity check; that does not authorise rewriting the engine's accepted-approval semantics. Revalidating by calling a replay-consuming authorize() twice is not an acceptable shortcut. Proposed targeted tests are listed separately from the preserved 87 AT criteria.

## 6. Alternatives and recommendation

Use G0-OWNER-DECISIONS for the twelve concrete recommendations, alternatives, consequences and acceptance criteria. The recommendation is platform-neutral interfaces, event-sourced segment persistence as specified, per-purpose hybrid runtime signatures, profile-specific custody, and an independent L3 anchor domain for P. SQLite, Windows-only runtime authority, immediate HSM integration, cloud services and composite-signature substitutions are not adopted here.

The selected OS, exact crypto package/wheels, token, anchor service and operational safety authority are not installed or provisioned by this ADR. Candidate technology must meet the existing contract and targeted evidence. Latest cryptography docs identified themselves as 51.0.0-dev1 during source checking: do not use that URL as a release pin. Its changelog corroborates the 48.0.0 OpenSSL 3.5 support claim; exact production artifacts still require qualification.

## 7. Experimental transfer

G08–G13 provide useful request validation, binding, replay, quorum, uncertainty and observation patterns. They use fixture identity, custom canonicalisation, SHA256 references, in-memory replay or local journals and external OpenSSL subprocesses. These are not equivalent to signed registries, RFC8785, SHA384, hybrid in-process verification or independent anchoring. Transfer decisions are PATTERN_ONLY until requalified perSR/AT. No code copy is included.

## 8. Consequences, residual risk and rollback

Retaining one design source reduces contradictory implementations and repeated repairs. It also exposes the real implementation work: the current preview cannot be called protected merely by approving a document. Host administrator/service compromise and untrusted runtime/interpreter risks remain bounded by the source threat model. Confidence/drift/provenance are still declared signals; no trueAI measurement or full D(t) computation is added.

This change is additive documentation only. Existing source and source hashes remain unchanged. Rollback of an uninstalled dossier is withdrawal of this proposal with its evidence retained. If later committed, revert only the additive change through normal signed change control; never rewrite history. Future runtime migration requires separate snapshot/log preservation, restore proof and SAFE_HALT on unverifiable state; it must not silently downgrade a P deployment to 0.4.2.

## 9. Gate decision

Preparation and structural traceability can be verified now. Original G0 baseline execution, exact historical scenarios, human technical/governance review and owner decisions remain PENDING. Therefore G0 overall remains HOLD. This record does not approve G1, E2-B code, a release, a commit or a push.

An owner may select the twelve recommendations or specify alternatives. That recorded decision is architecture adjudication; original G0 evidence conditions and dual reviews still require their own disposition. Approving the dossier's preparation is not approval of every recommendation.

## 10. Document interfaces

SR-RECONCILIATION: 27 Core requirements with verbatim source, delta, component, experiment boundary andATreferences. AT-CORE-87:every preserved Core criterion. PROFILE-RECONCILIATION-29: 14 EU + 15 USA requirements. AT-PROFILES-34: 16 EU + 18 USA criteria. INTERFACES defines nine contracts without introducing an unreviewed wire schema. VALIDATION-AND-ROLLBACK defines acceptance receipts and safe sequencing. G0-OWNER-DECISIONS contains unfilled human dispositions.
