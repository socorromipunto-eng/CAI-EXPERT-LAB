# Reconciliation overview — proposed, not implemented

Baseline: 80cd71e1620c5c580f6697742f520d329fa13709. All statuses below are source-inspection assessments; target acceptance tests NOT_RUN. Partial does not mean requirement accepted.

| SR | Component | Current target coverage | Gate | Delta |
|---|---|---|---|---|
| SR-01 | InputContract | PARTIAL | G1 | Finite numbers, strict booleans and action/context validation exist. Closed nested schemas, byte/depth limits, target grammar and rejection of authority-owned fields are not the target contract yet. |
| SR-02 | DecisionService | PARTIAL | G1 | Input rejection is audited on selected routes; not every exception/SAFE_HALT path has the normalized REJECTED contract. |
| SR-03 | QuotaController | NOT_IMPLEMENTED | G1/G2 | No per-system rate budget, active-epoch quota reserve or bounded report contract in the reference runtime. |
| SR-04 | OutputContract | NOT_IMPLEMENTED | G1 | Client descriptions and other submitted fields are returned in records/reports; bounded untrusted_text/reason templates are not the target contract. |
| SR-05 | MCPFrontEnd | PARTIAL | G1 | MCP is stdio and has no approve tool, but currently exposes four tools, not the five planned tools, and is not the protected-process interface. |
| SR-06 | SignedRegistry | NOT_IMPLEMENTED | G4 | Asset/sector/safety context is still supplied by the proposal; no signed registry/index version source. |
| SR-07 | OperationCatalogue | NOT_IMPLEMENTED | G4 | Action category/destructive/blast radius are client data; no signed operation_id catalogue or computed target-group impact. |
| SR-08 | AIRegistration | NOT_IMPLEMENTED | G4/G8 | No signed AI registration, permitted operation set or OS-account binding; explainability/model facts are declared. |
| SR-09 | ProfileDispatcher | PARTIAL | G4 | EU/USA selection and conservative gate composition exist; client chooses one jurisdiction and there is no signed per-target multi-jurisdiction evaluation. |
| SR-10 | RegistryPolicy | NOT_IMPLEMENTED | G4/G5 | Missing/unknown sector can resolve to non-critical; no signed temporary emergency entry and max(M,2) approval policy. |
| SR-11 | ContextReconciler | NOT_IMPLEMENTED | G4 | No independent registry against which to compare declared_context, conflict rate or digest-safe aggregation. |
| SR-12 | DecisionStateMachine | NOT_IMPLEMENTED | G1 | Seven defensive lifecycle states exist; they are NOT the twelve decision lifecycle states in specification §9. |
| SR-13 | AuthorizationCoordinator | PARTIAL | G5/G7 | Approval rechecks current lifecycle/policy and detects pending changes. No decision TTL, versioned signed-source invalidation or atomic dispatch re-evaluation. |
| SR-14 | ApprovalVerifier | NOT_IMPLEMENTED | G5 | approve accepts a non-empty label, not a signed verified principal; M-of-N, namespaces, replay and hardware presence are absent. |
| SR-15 | OperatorAuthority | NOT_IMPLEMENTED | G3 | CLI set/transition/deny are local commands without signed roles or authenticated assertions. |
| SR-16 | EventStore | NOT_IMPLEMENTED | G2 | state.json is authoritative at load and overwritten separately from evidence; no event-sourced single writer, fsync ordering or replay recovery. |
| SR-17 | RecoveryController | NOT_IMPLEMENTED | G2/G3/G6 | No persistent SAFE_HALT, anchored grace condition or restricted signed recovery command set. |
| SR-18 | EpochManager | PARTIAL | G2/G3 | init now refuses existing state/evidence; legacy destruction is repaired. MCP _ensure_init still initializes missing runtimes; epochs, signed archive/import and snapshot rebuild are absent. |
| SR-19 | CheckpointService | PARTIAL | G6 | Local SHA256 hash chain and clarified limits exist; signed checkpoints, segment levels and L2/L3 enforcement are absent. |
| SR-20 | ExternalAnchor | NOT_IMPLEMENTED | G6 | No external append-only anchoring host or L3 recovery verification. Signed source commits do not anchor runtime evidence. |
| SR-21 | AdapterContract | NOT_IMPLEMENTED | G7 | EXECUTED records a local decision, without dispatch/report/independent observation from an adapter. |
| SR-22 | CryptoProvider | NOT_IMPLEMENTED | G3 | No in-process SSHSIG/hybrid verifier or pinned cryptography secure extra in the main engine. |
| SR-23 | TrustManifest | NOT_IMPLEMENTED | G3/G5/G6 | No monotonic signed key lifecycle, purpose separation, compromise overlay and review closure for runtime authority. |
| SR-24 | ClaimsReview | PARTIAL | EVERY_GATE | README and evidence module now describe limits; other code/tool claims and the historic NIST map remain inconsistent. No requirement can inherit AT PASS from the 0.4.2 suite. |
| SR-25 | CryptoSuitePolicy | NOT_IMPLEMENTED | G3/G5/G6 | Main engine has SHA256 evidence and no hybrid runtime signatures; Git SSH signing is separate. |
| SR-26 | JurisdictionProfile | PARTIAL | G4 | EU/USA modules and conservative outcome composition exist; signed versioned profile parameters and the complete interface/retention contract do not. |
| SR-27 | CorePolicy | PARTIAL | G4 | Existing policy/safety gates cover selected confidence/state/OT checks; no complete signed-source core gate table and fixed-bound catalogue validation. |

SR-24 is a process/release-review requirement; no fabricated automated test is assigned. Detailed verbatim source and AT links are in SR-RECONCILIATION.csv/json.
