# CAI Computational Robustness and Calculation Assurance Model

**Status:** Design-only integration prepared as a repository record; no product-code change or assurance closure is claimed.
**Assessment date:** 2026-11-26
**Project baseline inspected:** GitHub branch `remediation/audit-reconciliation-20261126-r3` at `c8619ce300880e394e206d4e11c3e91c7753288f`, fetched read-only. The owner’s Windows checkout is not mounted in this workspace.
**Sources:** Uploaded `book.pdf` and `chap1.pdf` (see §1).

## 1. Source identification and limits

`book.pdf` is *Computational Complexity: A Modern Approach* by Sanjeev Arora and Boaz Barak, an Internet draft dated January 8, 2007. Its front matter says that chapters vary in completeness, references and attributions are preliminary, and the draft is not to be reproduced or distributed without permission. This integration paraphrases concepts and does not reproduce the book.

The most relevant parts are Chapter 1 §1.2.2 on robustness of the abstract computation model; Chapter 7 on randomized computation, error reduction, and worst-case versus expected running time; Chapter 9 §9.2.2 on approximate counting; Chapter 10 on average-case cryptographic assumptions; and Chapter 15 on distributional/average-case complexity. The draft itself marks portions as incomplete or “needs more work,” so it is a conceptual source, not an implementation standard or normative authority.

`chap1.pdf` is a separate Chapter 1, “Algorithms with numbers,” covering integer arithmetic, modular exponentiation, Euclid’s algorithm, primality testing, RSA, and universal hashing. It supplies useful algorithmic examples but no CAI risk-scoring or sector-assurance formula.

## 2. Key interpretation for CAI

The word **robustness** is used in several distinct senses and the model must keep them separate:

1. **Computational-model robustness:** Chapter 1 argues that reasonable machine models can simulate one another with limited (typically polynomial) efficiency loss. This is about complexity-class definitions, not prediction stability.
2. **Algorithmic correctness under randomization:** Chapter 7 defines probabilistic algorithms with explicit success probabilities and discusses error reduction. A probability guarantee belongs to a particular algorithm, input domain, and sampling process.
3. **Average-case complexity:** Chapters 10 and 15 require an input distribution. Average performance does not imply a worst-case guarantee, especially when an adversary can choose inputs.
4. **AI model confidence and drift:** CAI receives these as model measurements and applies policy thresholds. They are not the same as an algorithm’s probability of returning a mathematically correct answer.
5. **Statistical or operational robustness:** Stability under data shift, uncertainty intervals, perturbations, or sector conditions requires empirical definitions and validation. The book does not supply those CAI-specific measurements.

Do not merge these into one “robustness score.”

## 3. Current CAI calculation baseline

The inspected source snapshot implements rule-based comparisons rather than a derived probabilistic risk estimator:

| Source module | Current calculation | Assurance reading |
|---|---|---|
| `cai_engine/core.py` | Rejects non-finite/non-numeric normalized confidence and bounds confidence to `[0, 1]`. | Input-domain validation only; it does not establish calibration or source trust. |
| `cai_engine/governed_agent.py` | Validates caller-supplied confidence and drift as finite values in `[0, 1]`. | Values are supplied by the proposal; provenance and measurement methodology need separate evidence. |
| `cai_engine/gates.py` | Compares confidence with `0.80`; escalates when blast radius exceeds `25`; gates OT level and destructive actions. | Deterministic policy rules; not probability estimates or a mathematically optimized risk model. |
| `cai_engine/usa.py` | Uses confidence floors `0.95`, `0.90`, `0.80`, `0.70`; rejects drift above `0.15`; escalates sector/OT cases. | Configured policy values; the uploaded book does not validate these numbers. |
| `cai_engine/eu_ai_act.py` | Uses confidence floors `0.90` and `0.70`, and drift maximum `0.15`, alongside classification/oversight gates. | Project enforcement parameters; they are not thresholds prescribed by the complexity book. |

These numeric comparisons are deterministic once validated inputs and policy constants are fixed. Their **input truth, calibration, applicability, and policy justification** remain separate assurance questions.

## 4. Calculation Assurance Contract (CAC)

Add this contract to every material CAI calculation, whether it is a gate, a metric, a confidence interval, or a future solver result. The contract is an auditable model record, not a new score.

```yaml
calculation_id: stable-name
calculation_version: semantic-version-or-content-hash
purpose: decision-relevant question answered
input_schema:
  encoding: canonical input format
  domain: units, allowed values, bounds, null/missing rules
  provenance: producer, source identifier, timestamp, incident binding
algorithm:
  class: deterministic | randomized | approximate | heuristic
  procedure: versioned algorithm or library/provider identifier
  exactness: exact | bounded-error | approximate | unvalidated
  correctness_claim: formal invariant or measured acceptance criterion
  error_bound: numeric bound plus interpretation, or null for deterministic exact rules
  randomness: source, independence assumptions, seed handling, repeat policy, or null
  complexity: worst_case_time, expected_time, worst_case_memory, input-size parameter
limits:
  max_payload_bytes: owner-approved bound
  max_numeric_bits: owner-approved bound
  execution_budget_ms: owner-approved bound
output:
  value: result in explicit units/representation
  status: PASS | FAIL | HOLD
  evidence_refs: source and validation record identifiers
```

No field may be filled with a guessed bound. If the algorithm, input distribution, error guarantee, or resource limit is unknown, record it as `UNKNOWN` and hold any assurance claim that depends on it.

## 5. Integration rules from the two uploaded sources

### 5.1 Deterministic gates stay distinct from probabilistic algorithms

For current confidence, drift, blast-radius, and OT gates, record:

- validated input domain and provenance;
- exact comparison operator (`<`, `>`, or `<=`) and the policy version;
- the threshold’s owner, rationale, effective date, and change approval;
- boundary tests at threshold equality and immediately above/below;
- a statement that the gate is deterministic conditional on its input.

The model must not describe a confidence threshold as a probability of correctness unless a calibration method and applicable validation evidence support that interpretation.

### 5.2 Randomized calculation rules

If a future CAI calculation uses randomness, it must declare its error model: one-sided or two-sided error, per-input success/error guarantee, random-source assumptions, independence assumptions, repetitions, and whether the output is exact or approximate. Repetition reduces error only under the theorem’s assumptions; repeated runs over correlated data or a shared faulty source do not justify the same bound.

The book’s majority-vote error-reduction result is an algorithmic theorem under independent trials and a per-input success margin. It must not be applied to AI confidence, repeated evaluations of the same biased model, or duplicated telemetry as though they were independent trials.

### 5.3 Average-case versus adversarial inputs

Any performance claim based on average-case inputs must name and justify its distribution. CAI security interfaces accept potentially adversarial proposals, so average-case execution performance cannot replace a worst-case resource limit. Record expected runtime and worst-case runtime separately. Where the worst-case is unknown, set a hard payload/operation budget and use a safe timeout/hold path.

### 5.4 Approximate results

If a future model returns an estimate, record an explicit approximation factor/tolerance, failure probability, sample size, and validation method. Keep `approximate` outputs visibly distinct from exact outputs. An approximation theorem for one mathematical problem does not transfer to an unrelated CAI risk calculation.

### 5.5 Cryptographic calculation boundary

The two chapters explain mathematical foundations and complexity assumptions; neither specifies a current cryptographic deployment profile for CAI. Use a maintained cryptographic provider for key generation, signature operations, and validation. Record algorithm, provider/version, key purpose and lifecycle, trust source, and validation evidence. Do not implement primality tests, RSA, signatures, or cryptographic hashes from textbook pseudocode in the CAI governance engine.

Universal hashing in `chap1.pdf` concerns expected collisions for data-structure lookup. It is not a substitute for a cryptographic digest, digital signature, or external evidence anchor.

## 6. Instantiated calculation records for the inspected CAI rules

These records apply the CAC schema to current code. `UNKNOWN` means the reviewed source did not establish the value; it is not a zero or a pass.

| CAC field | Confidence floor | Drift ceiling | Blast-radius escalation |
|---|---|---|---|
| Calculation ID | `CAI-AI-CONFIDENCE-FLOOR` | `CAI-MODEL-DRIFT-CEILING` | `CAI-ACTION-BLAST-RADIUS` |
| Procedure | Compare supplied `confidence` to policy floor | Compare supplied `drift_score` to `0.15` | Compare integer `blast_radius` to `25` |
| Kind | Deterministic policy comparison | Deterministic policy comparison | Deterministic policy comparison |
| Input domain in code | finite numeric `[0,1]` | finite numeric `[0,1]` | non-negative integer |
| Threshold source in code | USA consequence floors `.95/.90/.80/.70`; EU `.90/.70`; engine `.80` | USA/EU `.15` | `25` assets |
| Measurement source | Proposal-supplied AI output | Proposal-supplied drift value | Proposal-supplied action metadata |
| Calibration / threshold rationale | `UNKNOWN` in this source snapshot | `UNKNOWN` in this source snapshot | `UNKNOWN` in this source snapshot |
| Complexity | Fixed-size scalar comparison after validation; upstream serialization/measurement cost is not bounded here | Fixed-size scalar comparison after validation; upstream serialization/measurement cost is not bounded here | Comparison cost depends on integer bit length (`b`); no explicit maximum numeric bit length is specified in the inspected code |
| Randomization/error bound | None in the gate itself; upstream metric validity is not established | None in the gate itself; upstream drift-method validity is not established | None |
| Assurance state | Deterministic behavior is inspectable; meaning/calibration of input and policy rationale remain open | Deterministic behavior is inspectable; measurement validity and threshold rationale remain open | Deterministic behavior is inspectable; maximum accepted integer/payload/resource bound remains open |

Important: deterministic execution does not imply the input is trustworthy or the policy is correct. These gate records do not calculate a combined risk score.

## 7. Robust decision extension requiring separate validation

The current engine receives point values for confidence and drift. A future uncertainty-aware interface could supply a validated interval, but the interval must come from an independently specified and tested measurement/calibration process. The decision rule below is a **CAI design proposal**, not a theorem from either uploaded book:

For a lower-bound requirement `m ≥ τ`, with valid interval `[L, U]`:

- pass the numeric gate only when `L ≥ τ`;
- fail it when `U < τ`;
- return `HOLD`/human review when `L < τ ≤ U`.

For an upper-bound requirement `m ≤ τ`:

- pass only when `U ≤ τ`;
- fail when `L > τ`;
- return `HOLD`/human review when `L ≤ τ < U`.

This is conservative interval reasoning. It does not create a confidence interval, calibrate an AI model, prove safety, or classify a sector. Before implementation, define the interval’s statistical coverage, population, incident/time scope, missing-data behavior, calibration dataset, and independent validation protocol.

## 8. Acceptance criteria for a code integration

1. Every numeric decision path has a CAC record and a stable policy/version identifier.
2. Inputs are validated before comparison; booleans, NaN, infinity, malformed encodings, missing values, and out-of-domain values have explicit rejection/hold tests.
3. All threshold boundary tests assert equality and adjacent representable values; the policy’s strictness is documented.
4. Randomized or approximate calculations expose their per-input error/approximation guarantees and their assumptions; no unsupported independence or input-distribution claim is accepted.
5. Resource safeguards are tested with maximum and over-limit payloads/numbers; worst-case and expected execution claims are not conflated.
6. Sector policy thresholds retain traceable owner rationale and empirical validation. Neither uploaded book is treated as evidence for those numeric values.
7. Full project Ruff, compile, unit, integration, and adversarial suites pass on the owner’s Windows environment and CI before a signed merge.

## 9. Disposition

**Design integration: PREPARED. Code integration: NOT IMPLEMENTED. Assurance: HOLD.** This document strengthens how CAI should specify and validate calculations, particularly algorithmic error, complexity, and input-distribution assumptions. It does not produce a new risk formula or justify current thresholds. The branch contains the sector/audit reconciliation, but this model document is not yet recorded in that branch. A proposed owner-run integration script will verify the exact branch, HEAD, and existing audit-record blob before adding this document and an append-only note to the audit reconciliation. It will not stage, commit, sign, push, or modify `main`.

## 10. Open calculation and assurance debt register

This register separates source-code observations from design proposals. “Open” means closure evidence has not been established in the reviewed branch or supplied execution record.

| ID | Debt | Status | Closure evidence |
|---|---|---|---|
| CALC-01 | Confidence and drift are proposal-supplied measurements; the reviewed code path does not establish their calibration, measurement method, dataset, or provenance. | OPEN | Versioned measurement contract; trusted provenance; calibration/validation results on representative and adversarially selected slices; independent disposition. |
| CALC-02 | Policy thresholds are deterministic comparisons, but their policy owner, rationale, effective date, and empirical basis are not established by the complexity text. | OPEN | Approved policy record for every threshold, explicit comparison semantics, change history, and boundary tests at/either side of each threshold. |
| CALC-03 | A common contract for input domain, units, algorithm class, exactness/error, resource bounds, output, and evidence references is proposed here but is not present as a machine-readable contract for every material calculation. | OPEN — DESIGN PREPARED | Approved schema and version; per-calculation records; implementation links; schema validation and negative tests. |
| CALC-04 | The reviewed model uses point values; uncertainty-aware interval handling is only a proposal. | OPEN — DESIGN ONLY | Approved uncertainty method, population/time scope, calibration, coverage evidence, missing/conflicting-data behavior, and tests before any code or claim uses intervals. |
| CALC-05 | No new combined “robustness/risk” score is justified by the uploaded texts or current code. | NO SCORE AUTHORIZED | Keep distinct measures and hard safety/security gates; any later score requires an explicit purpose, validated inputs, justified aggregation, sensitivity analysis, and owner approval. |
| EVID-02 | The current evidence log’s four strict expected failures remain open for tail truncation and full-chain rewrite; this model document does not address evidence authenticity. | OPEN | Independent anchor trust domain plus signed monotonic checkpoints, recovery/key lifecycle, offline verification, adversarial tests, and external operating evidence. |
| TEST-02 | PR #3’s merged CI is verified for source head `f63e4d5` (714 passed, 4 xfailed on six matrix jobs). Commit `c8619ce` has zero GitHub check runs in the read-only API as of this assessment. The owner reported local Ruff/compile/full-suite success for that candidate, but the shared transcript has no numeric summary. | CURRENT BRANCH CI NOT VERIFIED | Obtain a completed CI run for the exact current branch commit; retain run URL, matrix results, and pytest summary. Do not substitute the PR #3 baseline results. |
| ASSURE-01 | Approver authentication, deployed MCP/actuator boundary, alternate-route prevention, and telemetry-to-decision binding remain open in the technical audit. | OPEN | See H-01–H-04/H-06 and their acceptance evidence in `AUDIT-TECHNICAL-RECONCILIATION-2026-11-26.md`; all must be tested at the identified target boundary. |
| GOV-01 | GitHub effective branch/review/private-reporting settings, scope-specific written license authorization, independent technical/regulatory review, and deployment qualification are not established. | NOT VERIFIED / OPEN | See residual evidence gates in the technical audit reconciliation; obtain direct evidence and independent dispositions. |

### Evidence-backed disposition

- The source branch `c8619ce300880e394e206d4e11c3e91c7753288f` is signed and GitHub reports its signature as valid. This verifies that commit’s signature only; it does not establish independent review or validate the calculations.
- The merged PR #3 CI results belong to source head `f63e4d55a5175cabd47050d138e159284615b5e6`, not to the later audit/sector branch.
- GitHub’s check-runs endpoint returned zero checks for `c8619ce300880e394e206d4e11c3e91c7753288f` at review time. The local runner report is owner-reported evidence and has no visible test-count transcript here.
- The technical reconciliation’s anticipated `716 passed, 4 xfailed` gate is an expected result for its candidate, not a result for `c8619ce` unless an actual run reports that exact summary.
- **Release and deployment decision remain HOLD.** Adding this design record closes only the documentation-traceability item for the calculation model. It closes none of CALC-01 through CALC-04, EVID-02, H-01 through H-04/H-06, or GOV-01.
