# CAI-EXPERT-LAB — Regulatory and Standards Basis

This document declares the legal instruments and standards that CAI-EXPERT-LAB
aligns to, their versions, and the review status. It is the single place where
the framework's regulatory basis is stated and dated.

> Alignment, not compliance. CAI-EXPERT-LAB maps to and enforces proportionate
> governance. It does not assert legal compliance, conformity assessment,
> certification or accreditation. Always verify the official text before relying
> on any date or provision below.

- **Last reviewed:** 2026-10-11
- **Next review due:** 2027-01-11 (quarterly cadence)
- **Owner:** Antonio José Socorro Marín — Creator of CAI-EXPERT-LAB®

---

## European Union

**Instrument:** Regulation (EU) 2024/1689 (the "AI Act"), **as amended by the
Digital Omnibus — Regulation (EU) 2026/1744** (in force 27 July 2026).

Key application dates after the Digital Omnibus:

| Obligation | Applies from |
|---|---|
| Prohibited practices (Art. 5) | 2 Feb 2025 (already applicable) |
| New Art. 5 prohibitions added by the Digital Omnibus (NCII, CSAM) | 2 Dec 2026 |
| Transparency (Art. 50) | 2 Aug 2026 |
| Art. 50(2) marking — legacy generative AI (on market before 2 Aug 2026) | 2 Dec 2026 (grace) |
| High-risk — Annex III standalone systems | **2 Dec 2027** (deferred from 2 Aug 2026) |
| High-risk — Annex I product-embedded systems | 2 Aug 2028 |
| High-risk — public-authority systems | 2 Aug 2030 |

Other Digital Omnibus changes to track: narrowed "safety component" definition;
AI-literacy duty softened to "support development" (Art. 4); special-category
data processing for bias detection extended under a strict-necessity standard;
regulatory-sandbox establishment deadline 2 Aug 2027 (Art. 57); AI Office
enforcement powers (Arts. 75–75d).

Engine mapping: `cai_engine/eu_ai_act.py` implements risk tiers and the Art. 5 /
9–15 / 50 gates. The Digital Omnibus changes **dates and scope**, not the
article obligations the engine enforces. The engine does not detect prohibited
practices itself: it blocks a proposal when the caller declares
`prohibited_practice: true`, which covers the two new Art. 5 prohibitions only
if the caller declares them.

---

## United States

| Instrument | Version / status (2026-10-11) |
|---|---|
| NSM-22 — National Security Memorandum on Critical Infrastructure Security and Resilience | 2024; current |
| 16 critical-infrastructure sectors + SRMAs | per NSM-22; current |
| NIST AI Risk Management Framework | AI RMF **1.0**; current |
| NIST AI 600-1 — Generative AI Profile | current |

Engine mapping: `cai_engine/usa.py` and `cai_engine/usa_sectors.py` implement
the 16 NSM-22 sectors (SRMA, consequence level, OT intensity), NIST AI RMF
function traceability, and the NIST AI 600-1 generative-AI gate.

---

## Review procedure

1. On the review date, check the official sources below for changes.
2. For each verified source change, assess jurisdiction, actor, use case,
   applicability and impact before proposing a repository change. A changed
   date or document title does not automatically justify changing a threshold.
3. Trace affected requirements to documents, implementation and tests. Change
   only the affected components after the required authorization and review;
   version those components and record the change in
   `docs/CORE/CAI-Core-Evolution-Traceability-Register.md` before or concurrently
   with publication. Preserve historical evidence and source editions.
4. Update **Last reviewed** only after the actual normative review is complete.
   An editorial correction is not a fresh verification of every legal date.

## Official sources to watch

- EU AI Act and amendments — official text and consolidation on
  https://eur-lex.europa.eu/
- NIST AI RMF and profiles — https://www.nist.gov/itl/ai-risk-management-framework
- U.S. critical infrastructure / NSM-22 — CISA (https://www.cisa.gov) and the
  relevant Sector Risk Management Agencies


## Applicability and source status

For adoption, identify each source by issuer, identifier, edition, status,
exact provision, applicability and verification date. Distinguish legislation,
contract requirements, voluntary guidance and internal proposed requirements.
Keep public drafts separate from final publications. Secondary explainers may
help discovery but do not replace official normative text.

NIST AI 600-1 is the generative-AI profile; do not automatically apply every
generative-AI provision to a predictive graph model. Applicability of CMMC and
CUI requirements must be established for the actual contract, data and system.
No repository mapping alone constitutes certification or comprehensive United
States compliance. Identify an ambiguous source name before claiming alignment.

This section is an editorial reconciliation candidate dated 2026-10-23. It does
not change the historical review date or claim that all legal dates above have
been reverified. Adoption and normative review remain separate decisions.
