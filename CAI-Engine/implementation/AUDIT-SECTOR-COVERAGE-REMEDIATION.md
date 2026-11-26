# Sector coverage remediation — review record

**Candidate ID:** `CHG-CAI-SECTOR-COVERAGE-2026-11-26`
**Repository:** `socorromipunto-eng/CAI-EXPERT-LAB`
**Reviewed PR baseline:** `13770201c1be3a0c2cae530fd0b8aa1a3d19c478`
**Target branch:** `remediation/r01-r10-audited-candidate`
**Base branch:** `main` at `80cd71e1620c5c580f6697742f520d329fa13709`
**Decision:** `HOLD` for production, operational use, compliance claims, or sector control effectiveness.

## 1. Purpose and boundaries

This candidate addresses one demonstrated repository gap: only ten of the 16 NSM-22 sector application profiles had documents and worked examples, while the sector-example test accepted ten examples. It adds six draft profiles, twelve synthetic fixtures, and an exact 16-sector coverage gate.

This is a documentation and reference-test correction. It does not authenticate sector, jurisdiction, asset, action, confidence, drift, or approver metadata. It does not implement a deployed security boundary, external actuator, independent evidence anchor, legal authorization, or third-party assessment. A fixture pass is software-path evidence only.

The candidate is prepared against the PR head listed above. It has not been applied to the owner’s Windows checkout, committed, signed, pushed, or merged. `main` remains outside this change.

## 2. Evidence at the reviewed baseline

At the exact PR baseline:

- `docs/USA/sector-frameworks/README.md` listed ten application documents and put Government Facilities, Healthcare and Public Health, Information Technology, Nuclear, Transportation, and Water in “Later batches.”
- `examples/sectors/` contained twenty examples for those ten sectors.
- `tests/TEST_SECTOR_EXAMPLES.py::test_examples_exist` required only `len(EXAMPLES) >= 10`.
- `usa_sectors.py` contained 16 keys, but the registry is not an asset inventory and does not authenticate proposal context.

These are direct repository observations. They do not establish that the other ten sector documents are legally current or operationally validated.

## 3. Candidate changes

| Area | Candidate change | Acceptance evidence |
|---|---|---|
| Government Facilities, Healthcare and Public Health, Information Technology, Nuclear, Transportation, Water | Add one English draft profile per missing NSM-22 sector. Each records representative assets, service/safety invariants, trust boundaries, defensive abuse cases, isolated acceptance tests, evidence needs, source limits, and explicit `HOLD` disposition. | Profile key matches the engine registry; claims distinguish generic guidance from entity-specific legal applicability; no production-readiness claim. |
| Synthetic sector examples | Add two synthetic examples per new sector: human escalation for a containment proposal and lifecycle denial for eradication while the engine is in `ISOLATE`. | Runtime status, decision, gate list, evidence integrity, and cited profile table all match for every fixture. |
| Sector coverage test | Require exactly two fixtures for each of the 16 current sector keys and exactly one matching profile document for every key. | 16 registry keys, 32 examples, 16 profiles; omissions and duplicate profile/example mappings fail. |
| Sector README | Replace the “Later batches” gap with a draft inventory of all 16 profiles; separate aviation as a reference profile within Transportation; clarify that document presence is not control implementation or legal applicability. | README status retains the draft and `HOLD` boundaries. |

The profiles use the supplied NIST AI RMF 1.0, CISA CPG, ICS monitoring, defense-in-depth, and application-whitelisting sources only for assessment questions and control evidence. They do not claim those sources prove implementation, apply as binding law to every entity, or prescribe CAI confidence thresholds.

## 4. Validation record

| Check | Result | Limitation |
|---|---|---|
| 32 fixture execution against the reference engine | **PASS** — observed status, decision, gate results, and local evidence verification matched fixture expectations. | Local synthetic execution only; no independent reviewer, external service, or deployed system. |
| Profile-to-fixture table reconciliation | **PASS** — each fixture is cited by exactly one profile with matching lifecycle, result, and non-ALLOW gates. | Consistency does not establish the profile’s operational effectiveness. |
| Coverage accounting | **PASS** — 16/16 registered sector keys, two fixtures per key, one profile per key. | The list comes from the repository’s static registry; it does not validate the official taxonomy or SRMA assignment independently. |
| Python compilation | **PASS (owner-reported, Windows, 2026-11-26)** — `compileall -q cai_engine tests` completed without error. | Compilation is not behavioral verification. |
| `git diff --check` on candidate patch | **PASS**. | No change has been staged in the owner’s repository. |
| Full `pytest` suite | **PASS (owner-reported, Windows, 2026-11-26)** — 714 passed, 4 xfailed in 21.61 s. | Four expected failures remain for evidence truncation and rewrite; release remains HOLD. |
| Ruff | **PASS (owner-reported, Windows, 2026-11-26)** — All checks passed. | Result reported from the exact local postimage; not independently rerun here. |

## 5. Open findings after this candidate

1. **Trust in decision inputs:** sector and jurisdiction are caller-controlled fields in the reference API. Missing or incorrect inputs can select a weaker policy path. This candidate documents the gap; it does not solve it.
2. **Asset and safety authority:** the engine has no authenticated asset registry, process-hazard model, operator identity, or independent safety authority source.
3. **Execution boundary:** there is no deployed privilege boundary or external actuator integration, and the engine cannot constrain alternate client routes.
4. **Evidence completeness/authenticity:** local hash chaining cannot prove a complete history or authenticity without an independent anchor. R07/R08 remain `LIMIT`.
5. **Evidence-to-decision linkage:** sector telemetry is not established as a required, trusted input to each governed decision.
6. **Current source applicability:** the existing ten sector documents contain time-sensitive legal/status claims. This candidate does not independently revalidate those claims or determine covered-entity status for any user.
7. **Repository controls:** the effective private reporting channel, branch rules, required approvals, bypass rights, and workflow protections require direct settings evidence.
8. **License and external review:** intended operational/production/commercial use still requires the written permission specified by the repository license. No independent security, regulatory, safety, or deployment assessment is included.

**Release disposition remains `HOLD`.** Completing the document inventory does not close these findings and does not qualify CAI-EXPERT-LAB for production or operational use.

## 6. Change control

This review record corresponds to a proposed patch based on PR head `13770201c1be3a0c2cae530fd0b8aa1a3d19c478`. The owner must verify the head has not moved before applying it, run the full repository gates on the resulting postimage, inspect the diff, and sign any commit using the owner’s configured key. No commit, push, PR update, or `main` change was made by this review.
