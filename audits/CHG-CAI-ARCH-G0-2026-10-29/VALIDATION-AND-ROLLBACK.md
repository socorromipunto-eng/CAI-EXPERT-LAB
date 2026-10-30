# Validation and recovery plan — proposed

## What was actually verified in this preparation

Current main unchanged at 80cd71e; source file hashes checked against the prior 501-file inventory;27 unique Core SR, 87 unique Core AT, 29 profile SR and 34 profile AT enumerated from pinned source. Requirement/AT links and referenced paths were checked structurally. No repository modules, tests, PowerShell, crypto key generation, installs or operational systems were executed. Existing CI is regression evidence, not an original G0 baseline run or target AT acceptance.

## Original G0 prerequisites retained

1. Locate and preserve exact T01–T10 scripts and their original b52935e run report, or submit an explicit owner-adjudicated evidence replacement/change. Do not reconstruct unknown historical scripts and label them originals.
2. Define current regression scenarios separately, with exact command, interpreter, dependency artifacts, disposable runtime, expected output and negative controls. Recover history only in an authorised isolated workspace.
3. Separately authorise test execution. Record environment, timestamps, baseline, raw output, exit code, expected/actual, skipped/xfail disposition and hashes. No effects outside the fixture.
4. Complete technical and governance review. Record reviewer identity, independence/conflicts and exact reviewed artifact hashes. AI self-review is not human-independent evidence.
5. Record the owner's D01–D12 dispositions and final G0 decision. None is filled automatically.

## Proposed current baseline probes, not historical T identifiers

G0R-01 strict numeric/boolean/schema rejection; G0R-02 init preservation and partial-runtime refusal; G0R-03 approval state/policy revalidation; G0R-04 expired pending decision known limitation; G0R-05 omitted sector known limitation; G0R-06 stale facts/telemetry known limitation; G0R-07 tail/whole-chain known limits; G0R-08 CLI verify exit/JSON contract; G0R-09 concurrent/crash persistence analysis followed by separately approved fixture probes; G0R-10 MCP tool/permission exposure and claims boundary. Specify executable cases and expected current results before execution. A test demonstrating a known limit is LIMIT, not PASS for the proposed control.

## Target qualification

Preserve all 121 existing acceptance criteria and the SR-24 process review; do not report any as passed here. Follow gate dependencies from G1 to G8. Platform path codes and W markers are copied exactly from the source. Tests needed by profiles run at their declared gate, not prematurely. G8 requires the listed reruns and protected-profile proof, not only a platform matrix of 0.4.2.

Beyond the preserved criteria, adjudicate explicit concurrency/revocation/time-boundary tests and §8 not_after versus SR-13.6 semantics. Qualify a released in-process crypto provider and exact artifacts on both supported platforms before G3. Fail closed on unavailable signatures; no mock PASS or subprocess fallback inside engine verification.

## Recovery and rollback

This dossier has no runtime rollback because it changes no runtime. Proposed repository additions are under a new audits subdirectory; do not overwrite an existing path. If the baseline changes, compare affected source hashes and re-assess before applying the additive patch.

Later gate rollbacks require their own receipt: closed epoch/snapshot and source hashes; backup verified; no evidence deletion; compatibility/migration identified; restore tested in a fixture. Downgrading protected mode to an unprotected 0.4.2 engine is not a recovery strategy. If authenticity or state is unknown, retain evidence and HOLD/SAFE_HALT rather than reset or blindly retry.

## Evidence receipt contract

Every run/review must record ID, baseline SHA, scoped paths/hashes, command or review method, environment, authorised effect boundary, start/end timestamps, expected/actual, exit/status, raw-output hashes, anomalies, reviewer and final human disposition. Store references to external evidence without publishing private credentials or unnecessary identity details. Never request a private key/passphrase in chat.
