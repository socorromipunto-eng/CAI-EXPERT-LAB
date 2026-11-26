# CAI-USA Government Facilities Sector Profile and Assurance Plan

**Status:** Draft, research and simulation profile; not an implementation or compliance claim.
**Sector key:** `government_facilities`
**NSM-22 profile/SRMA recorded in the current engine:** General Services Administration
**Review date:** 2026-11-26 (source snapshot date; sector-specific legal applicability not independently determined)

## 1. Scope and decision boundary

This profile defines a defensive review scope for the **Government Facilities** sector. It does not determine whether a particular organization, asset, service, contract, facility, or operator is regulated. Confirm those facts with the system owner and competent counsel using current primary sources before making an applicability decision.

A sector name supplied in a proposal is a label, not an authenticated asset classification, operational authority, or jurisdiction source. The current reference engine evaluates proposal-supplied context. Its sector gate is not a deployed security boundary, does not validate a target against a trusted registry, and cannot prevent a client from using another route.

## 2. Sector assets and service invariants

Representative systems include: facility access-control and visitor-management systems; building automation; fire/life-safety interfaces; elevators; emergency power; public-facing facility services.

**Safety and service invariants:** Life safety, physical access accountability, emergency egress, continuity of public services, and independent manual control must remain available.

**Asset-scoping caution:** Building automation, life-safety interfaces, physical access, emergency power, and public services can coexist in one facility; a sector-level tag does not identify which device is safety-critical.

## 3. Trust boundaries and failure analysis

Review these boundaries before a target is admitted to a governed action:

- Enterprise identity / facility-management network / building-control zones / life-safety systems; contractor/vendor remote access; public-facing services / internal facility services.
- Identity and authorization source; asset owner and operational authority; evidence collection and retention; control-system/operator interface.
- Normal, maintenance, emergency, degraded, failover, and recovery modes. An emergency or maintenance route must be modeled explicitly; it is not an undocumented exception.

### Defensive abuse cases for isolated analysis

1. A containment proposal labeled “observe” severs a building-control path needed for fire, elevator, or emergency-power operations.
2. A vendor maintenance path is treated as trusted after an identity or ownership change.
3. An access-control policy update locks out responders or removes the audit trail for privileged entry.


These are synthetic threat hypotheses, not incident claims. Do not run them against live infrastructure. Any physical or operational test requires the asset owner’s written authorization, a site safety plan, and an approved non-production test environment.

## 4. Reference-engine behavior observed in synthetic examples

The examples below exercise only the local CAI reference decision path. `PENDING_APPROVAL` means the engine recorded a local decision requiring a human; it does not authenticate the human or prove an external action occurred. `BLOCKED` reflects a lifecycle denial in the example; it is not proof that alternate paths are blocked.

| Fixture | Scenario | Lifecycle | Action | Observed result | Non-ALLOW gates |
|---|---|---|---|---|---|
| `government_facilities-1.json` | Synthetic defensive example for Government Facilities; no real asset or action is represented. Case 1. | ISOLATE | CONTAINMENT, Purdue level 2 | PENDING_APPROVAL (ESCALATE) | usa.srma_oversight = ESCALATE; safety.ot_ics = ESCALATE |
| `government_facilities-2.json` | Synthetic defensive example for Government Facilities; no real asset or action is represented. Case 2. | ISOLATE | ERADICATION | BLOCKED (DENY) | usa.srma_oversight = ESCALATE; policy.state_constraint = DENY |

The fixtures are synthetic and assert consistency between JSON, the engine result, and this table. They do not establish sector coverage, operational safety, effectiveness, legal compliance, or deployment qualification.

## 5. Required sector-specific acceptance tests

Before claiming that controls are effective for a deployment, add owner-approved, non-production tests for:

- Require a facility-specific asset identity, owner, zone, and life-safety dependency before policy evaluation.
- Reject caller-supplied “non-OT” or “observe” labels when the target registry identifies a building-control or life-safety function.
- Exercise manual override, emergency egress, alternate power, and recovery paths in a non-production simulator.
- Missing, misspelled, conflicting, stale, replayed, or caller-forged sector, jurisdiction, asset, authority, telemetry, confidence, drift, and action metadata; each must fail closed or escalate according to an approved risk policy.
- Unauthorized alternate routes, stale/replayed approvals, identity-provider loss, evidence-store failure, clock skew, partial writes, process crash, and recovery; preserve the safe state and capture auditable evidence.
- Independent control-effectiveness assessment by reviewers who did not implement the candidate.

For each test, retain the baseline commit, exact fixture/input hashes, expected and actual outcomes, logs, environment, operator, safety approval, limitations, and disposition. Synthetic unit tests remain software evidence only.

## 6. Existing engine mapping and limits

The repository currently represents this sector through a static sector key, one SRMA string, a consequence label, and a Boolean OT-intensive flag. These values are directory metadata, not an asset inventory or safety case. The caller supplies context and action labels. Human escalation in the library is not authenticated approval; local evidence chaining is not external completeness or authenticity; the engine has no enforced operating-system or actuator boundary.

Do not infer a numeric confidence threshold, calibrated model quality, regulation applicability, OT classification, or safe operational effect from this profile. Any such parameter needs a documented owner-approved risk rationale, measurement method, independent validation, and a versioned change record.

## 7. Source basis and applicability limits

The following uploaded sources support the **assessment method and evidence questions**, not a claim that a specific sector entity is compliant:

| Source | Use in this profile | Limit |
|---|---|---|
| NIST AI RMF 1.0, NIST AI 100-1, pp. 25–38 | Govern/Map/Measure/Manage; human oversight; measurement; safety, security, resilience, and monitoring. | Voluntary risk-management framework; does not prescribe this engine’s numeric thresholds. |
| CISA Cross-Sector Cybersecurity Performance Goals v1.0.1, checklist pp. 1–5 and report pp. 9–11 | Asset inventory, vulnerability mitigation, OT compensating controls, segmentation, and third-party assessment evidence. | Applicability and binding status are entity- and contract-specific; CPGs do not prove implementation. |
| ICS Monitoring Technology Considerations, pp. 2–3 | Asset/traffic baselines, unauthorized-link detection, safe response, and monitoring-tool isolation. | Guidance only; no live process change is authorized by this document. |
| NCCIC ICS-CERT Defense in Depth, pp. 15, 27, 39 | Zones/conduits, remote access, logging, layered controls, and detection limitations. | Guidance; site architecture and current source status must be verified. |
| ICS Application Whitelisting Guide, pp. 3–5 | Vendor compatibility, emergency/degraded modes, administrator bypass, and lifecycle/safety review. | Does not authorize deployment or configuration change. |
| NSM-22 (sector directory in repository) | Identifies the 16-sector taxonomy and the SRMA value currently represented by the project. | Verify the controlling primary text and current agency assignment before publication; a project mapping is not legal authority. |

Sector-specific statutes, regulations, directives, contracts, and agency guidance are **not asserted here**. Add them only after verifying the current primary text, effective date, scope, covered entity/asset, and competent reviewer disposition.

## 7.1 Sector-specific authoritative sources (checked 2026-11-26)

| Source and status | Use in this profile | Applicability limit |
|---|---|---|
| CISA, Infrastructure Resilience Planning Framework v1.2 (February 2024), sector/SRMA table, p. 54 — [PDF](https://www.cisa.gov/sites/default/files/2024-02/Infrastructure%20Resilience%20Planning%20Framework%20v1.2_JAN2024_508c.pdf) | Records the General Services Administration (GSA) as the Government Facilities SRMA in that framework. | This establishes the agency mapping in the cited 2024 framework, not authority over every federal, state, local, tribal, territorial, or privately operated facility. Confirm current agency assignment and asset ownership for the target. |
| GSA Acquisition Letter MV-2022-06, Cyber-Supply Chain Risk Management Requirements for Leasing — [GSA source](https://www.gsa.gov/policy-regulations/policy/acquisition-policy/acquisition-policy-library-and-resources/mv202206) | Gives a concrete federal-leasing context for building automation and facility-related control systems. | Limited to the stated GSA acquisition/leasing context and applicable lease instruments; it is not a general cybersecurity regulation for all government facilities. Verify current directive, contract and facility scope before use. |
| GSA Smart Buildings directive — [GSA source](https://www.gsa.gov/directives-library/gsa-smart-buildings) | Provides agency-specific context for GSA smart-building systems and cybersecurity practices. | Applies within GSA's stated program scope. It does not establish a government-wide control baseline or prove a target has implemented those controls. |

The registry SRMA value is directory metadata only. The GSA source set above is sector-specific scoping evidence, not a control-effectiveness assessment.

## 8. Evidence required before a deployment claim

- Owner-approved inventory tying asset identity, site, function, consequence, OT zone, safety owner, and authority to a versioned trusted source.
- Threat model and architecture showing trust boundaries, alternate routes, service dependencies, emergency/degraded modes, and external enforcement points.
- Test results for all acceptance cases above, with independent witness/review, test environment provenance, and an auditable evidence chain with external anchoring where completeness/authenticity is claimed.
- Verified license authorization for the intended use, effective repository controls, incident-reporting route, and an independent technical and regulatory review.

**Disposition:** `HOLD` for operational use, compliance claims, or sector assurance. This profile closes only the documentation/example-count gap for this sector. It does not close R07/R08, the deployed security boundary, license authorization, repository settings, independent validation, or deployment qualification.
