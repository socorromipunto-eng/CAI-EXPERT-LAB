# Interface reconciliation — proposed

These nine contracts allocate the existing specification. They are not newly approved wire schemas or an implementation.

## IF01 — Untrusted proposal → validator

Data: operation_id, typed targets, permitted client declarations, request identity/reference

Source: SR-01..05; §12

Invariant: Reject unknown/owned fields, bounds and malformed input before authority evaluation. All entrypoints share this contract.

Acceptance: AT01–10

## IF02 — Protected sources → trust loader

Data: Manifest, registry/index, catalogue and registration; versions, digests, signatures, validity

Source: SR-06..11;SR-22/23/25/26;§6

Invariant: Only protected file sources; no source replacement over MCP/IPC. Monotonic versions and cumulative revocations.

Acceptance: AT21–43,74–77,81–87

## IF03 — Front end → protected engine

Data: Length-prefixed bounded UTF8 JSON; OS peer identity bound to AI registration

Source: §6.5;§12.2;SR-08

Invariant: Separate accounts and engine-owned pipe/socket; deny remote pipe clients; no pickle/object deserialization.

Acceptance: AT70–72

## IF04 — Decision → human request → accepted statement

Data: Exact decision digest, readable summary, principal-bound signatures, explicit verdict, time and statement id

Source: SR-13/14;§8.1

Invariant: No AI approver; union/maxima of minima; no key reused across purposes. Keep acceptance freshness separate from decision lifetime.

Acceptance: AT44–54,78

## IF05 — Operator → state/trust command

Data: Signed purpose-specific command, expected epoch/state/version, one-time statement_id

Source: SR-15/18/23;§8.2

Invariant: Safety assertions require approver role; archive/import administrative role; reject stale/replayed operations.

Acceptance: AT27–31,54

## IF06 — Decision coordinator → event store/snapshot

Data: Append sequence/hash/event; durable evidence then atomic derived snapshot

Source: SR-16..19;§10

Invariant: Single writer, locks, fsync ordering, replay, SAFE_HALT and fault output; never return success on unverifiable durability.

Acceptance: AT12–20,55–58,80

## IF07 — Checkpoint service → external anchor

Data: Checkpoint envelope, deployment/epoch/head/version and purpose-bound signatures

Source: SR-19/20/25;§10

Invariant: Separate host/custody; engine cannot rewrite remote history. Grace and recovery explicitly bounded.

Acceptance: AT56–64,79

## IF08 — Engine → adapter → verifier

Data: Signed exact dispatch, operation/parameters/targets, manifest version, deadline, acknowledgements/reports

Source: SR-13/21;§11

Invariant: One-use dispatch; no blind retries after uncertainty; independent observation required for RESULT_VERIFIED.

Acceptance: AT65–69

## IF09 — Core → jurisdiction profiles

Data: Signed classified asset/use/model data; core outcome; profile gates/reasons/approval minima

Source: SR-26/27; profiles§4–8

Invariant: Equal rank EU/USA; strictest results; profiles cannot relax core. Engineering policy and legal applicability stay distinct.

Acceptance: AT38–43,81–84;34profileAT
