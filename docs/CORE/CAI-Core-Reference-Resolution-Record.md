# Cybersecurity Artificial Intelligence Framework – Reference Resolution Record
Version 0.1 (Draft)  
Author: Antonio José Socorro Marín  
Creator of CAI-EXPERT-LAB (Cybersecurity Artificial Intelligence Framework)  

Copyright © 2026 Antonio José Socorro Marín.  
All rights reserved.  
Use, distribution, modification, and commercial exploitation are governed by the legal documents contained in the /legal directory of this repository.  

**NOTE**  
The normative language of CAI-EXPERT-LAB documentation is English.  
This document records how references to documents that do not exist in the repository are resolved. It does not assert compliance, certification, accreditation, or regulatory approval.  

## 1. Purpose

Some CAI documents cite document names that do not exist in this repository. Several of the citing documents are frozen under CAI-USA-Master-Freeze-v0.1, which permits only formatting corrections, so their text is not edited.

This record states, for each such name, its status and the existing documents a reader should use instead. It does not change the meaning of any frozen document.

## 2. Method

Every CAI document name cited in a Markdown file was compared with the Markdown files present in the repository, at commit 7a61984 (2026-10-16). Names that are prefixes of existing documents and names that are not documents (for example, the GitHub Actions workflow name) were excluded.

## 3. Resolution

Table 1 — Cited names that do not exist, with status and the existing documents to read instead.

| Cited name | Cited from | Status | Read instead |
|---|---|---|---|
| CAI-Core-Threat-Model-Framework | The 15 USA sector Traceability Matrices (frozen) | Not written | CAI-USA-Threat-Model-Integration (named in the same matrix entry); for the engine, CAI-Engine/specifications/CAI-ENG-SEC-001-Core.md section 5. CAI-Threat-Model-Framework-Integrity covers threats to the framework itself, not to protected systems, and is not a substitute. |
| CAI-Core-Secure-by-Design-Principles | The 15 USA sector Traceability Matrices (frozen) | Not written | CAI-USA-Secure-by-Design-Controls (named in the same matrix entry); CAI-Core-Architecture section 2.4. |
| CAI-Core-Telemetry-and-Evidence-Model | The 15 USA sector Traceability Matrices (frozen) | Not written | CAI-USA-Telemetry-and-Data-Model (named in the same matrix entry); CAI-Engine-Telemetry-Ingest-and-Validation; CAI-Engine-Evidence-and-Audit-Model; CAI-ENG-SEC-001-Core section 10. |
| CAI-Core-Engine-Governance | The 15 USA sector Traceability Matrices (frozen) | Not written | CAI-USA-ICS-OT-Safety-Gating (named in the same matrix entry in 14 of the 15 matrices; the Information Technology matrix names CAI-USA-Definition); CAI-Engine-Policy-and-Governance-Enforcement; CAI-Engine-Safety-Gates-and-Human-Oversight. |
| CAI-Core-Audit-and-Assurance-Principles | The 15 USA sector Traceability Matrices (frozen) | Not written | CAI-USA-Traceability-Matrix (named in the same matrix entry); CAI-Core-Dual-Audit-Pipeline for changes to the framework; CAI-Engine-Evidence-and-Audit-Model for operational evidence. |
| CAI-USA-NIST-Map | CAI-USA-Definition, CAI-USA-Secure-by-Design-Controls and CAI-USA-Traceability-Matrix (frozen); CAI-USA-AI-RMF-Map; CAI-USA-CISA-ZT-Map | Written with this name by CHG-2026-10-16-09 (repository audit finding AUD-03, phase 1); the citations are now valid | docs/USA/CAI-USA-NIST-Map.md. |
| CAI-USA-CMMC-Map | CAI-USA-Definition (frozen) | Not yet written; planned with this name (repository audit finding AUD-03, phase 3) | None. |
| CAI-EU-Critical-Infrastructure-Governance-Overlay | CAI-EU-Governance-Traceability-Matrix, CAI-EU-Master-Freeze-v0.1, CAI-EU-Sector-Overlay-Index-and-Navigation | Declared as planned in each citing document | No action needed. |
| CAI-USA-AI-Assurance | CAI-USA-CISA-ZT-Map | Wrong name; corrected in the citing document by CHG-2026-10-16-08 | CAI-USA-AI-Governance-and-Assurance. |
| CAI-USA-Government-Lab-Telemetry-Flow-and-Evidence | Four documents in labs/usa/Government | Not published; the citing documents now say so (CHG-2026-10-16-08) | None. The other 14 sectors have this lab. |

## 4. Maintenance

When a document listed as "Not yet written" is created with the cited name, its entry in Table 1 is updated in the same change. New references to documents that do not exist are not added to frozen documents.

## Status

Status: Draft – Reference Resolution Record Established  
End of Document
