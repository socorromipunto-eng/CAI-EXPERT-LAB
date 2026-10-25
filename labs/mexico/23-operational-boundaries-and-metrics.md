# CAI-MX – Operational Boundaries, Metrics, and Validation Model

> Proposed design reconciliation CHG-CAI-RECON-2026-10-22-001. Not an approved revision
> or executed validation. Canonical MX references: 15 (entities), 16 (rules),
> 17 (risk). Preserve original authorship and source baseline.

---

## 1. Purpose

This document formalizes the operational limits, measurable properties, and validation conditions of the CAI (Cybersecurity Artificial Intelligence) model.

Its objective is to:

- Define where CAI applies and where it does not  
- Introduce measurable indicators of decision integrity  
- Establish validation conditions for decision execution  
- Address dependency risks related to telemetry (ESA)  

---

## 2. Decision Validation Model and Canonical Authority

The earlier expression `V(d) = f(DSA, ESA, T) >= theta` is a conceptual summary,
not a competing executable rule. DSA and ESA are structured views, not scalars.
The canonical behavioral function in document 16 sections 3-4 consumes baseline,
telemetry, risk, policy and temporal inputs, returning DecisionState and
EnforcementOutcome. Document 16 sections 7.2-7.4 define the typed field projection,
normalized absolute differences and weighted drift. Document 17 defines risk.

## 3. Enforcement Condition

The earlier notation `|DSA - ESA| <= T` denotes only a drift constraint.
Use document 16's drift_total and thresholds; do not subtract complete objects
without a typed projection. Acceptable drift is necessary for normal
VALIDATED/ALLOW, not sufficient. Temporal validity, telemetry trust/freshness,
risk, confidence, policy and authority must also satisfy the canonical rules
before an effect is permitted.

---

## 4. Operational Boundaries

CAI is designed for:

- Federated environments  
- Systems with decision propagation  
- Context-sensitive execution environments  
- Real-time or near real-time telemetry  

### CAI is NOT applicable in:

- Fully isolated systems without telemetry  
- Static decision environments (no context change)  
- Offline or batch-only execution systems  
- Systems without decision propagation across boundaries  

---

## 5. Telemetry Dependency Model

CAI depends on ESA integrity.

### Risks:

- Incomplete telemetry  
- Delayed telemetry  
- Corrupted telemetry  

### Mitigation strategies:

- Multi-source telemetry validation  
- Confidence scoring for ESA inputs  
- Fallback to safe enforcement states  
- Conservative threshold adjustment  

---

## 6. Decision Integrity Metrics

These proposed definitions are not measured results. Every report identifies
system/ref, window, units, sampling, oracle, denominators, exclusions and limits.
A zero denominator is NO_DATA/NOT_APPLICABLE, never 100% success. Numerical
acceptance targets require owner approval; none are invented here.

### 6.1 Decision Drift Rate

Report magnitude using document 16's drift_total. Separately report frequency
as transitions across the chosen threshold / total monitored decision-time
(e.g. decision-hours) in the observation window. Repeated above-threshold samples
are not new crossings. Declare initial above-threshold and missing-data handling.

### 6.2 Validation Latency

Report observation-to-ingest, ingest-to-completed-validation and pre-dispatch
recheck duration separately. Declare time source and clock uncertainty. Report
missing, timed-out and unfinished cases rather than converting them to zero.

### 6.3 Enforcement Accuracy

For a declared population of final binary permitting/blocking decisions and
an independent test oracle: TP = invalid correctly blocked; FN = invalid
incorrectly permitted; FP = valid incorrectly blocked; TN = valid correctly
permitted. Accuracy = (TP + TN) / (TP + TN + FP + FN).
The earlier correctly blocked invalid / total enforcement actions ratio is not
general accuracy. Report conditional, pending and revalidation outcomes
separately unless the evaluation protocol defines their labels explicitly.

### 6.4 False Block Rate

False block rate = FP / (FP + TN) over oracle-valid cases.
Also report invalid allow rate = FN / (TP + FN) over oracle-invalid cases.
Publish raw counts and oracle limitations for both metrics.

### 6.5 Decision Consistency

Replay equivalent complete input tuples including versions, policy, source
snapshot, evaluation time and time-derived inputs. Report identical outputs /
comparable replay pairs. Similar ESA alone is not equivalence. Zero pairs is NO_DATA.

---

## 7. Failure Modes

CAI may degrade under:

- ESA loss  
- synchronization delay  
- incomplete context  

### Safe behavior:

- default to conservative enforcement  
- restrict execution when uncertainty increases  

---

## 8. Defensive Strength

These additions ensure that CAI:

- Is not purely conceptual  
- Is measurable and auditable  
- Defines operational limits  
- Addresses telemetry risks  

---

## 9. Conclusion

By introducing formal validation conditions, operational boundaries, and measurable metrics, CAI transitions from:

- Conceptual integrity model  

to:

> **Operational, measurable, and enforceable decision assurance system**