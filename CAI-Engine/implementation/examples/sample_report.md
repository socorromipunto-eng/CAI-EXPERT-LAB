# CAI-Engine — Execution & Assurance Report

- Current state: **MODEL**
- Context facts: {}
- Pending approvals: ['gov-5b60c81073', 'gov-8088e1c275', 'gov-39f2deb680']
- Evidence integrity: OK (chain verified)

## Evidence log (hash-chained)

| seq | event | detail |
|----:|-------|--------|
| 1 | ENGINE_INIT |  |
| 2 | GOVERNED_DECISION_PENDING_APPROVAL | AI[cai-triage-llm] USA:CRITICAL_INFRASTRUCTURE/Energy OBSERVE decision=ESCALATE |
| 3 | GOVERNED_DECISION_BLOCKED | AI[cai-triage-llm] USA:CRITICAL_INFRASTRUCTURE/Energy OBSERVE decision=DENY |
| 4 | GOVERNED_DECISION_PENDING_APPROVAL | AI[cai-genai-assistant] USA:CRITICAL_INFRASTRUCTURE/Healthcare and Public Health OBSERVE decision=ESCALATE |
| 5 | GOVERNED_DECISION_EXECUTED | AI[cai-triage-llm] USA:NON_CRITICAL/corporate_it OBSERVE decision=ALLOW |
| 6 | GOVERNED_DECISION_PENDING_APPROVAL | AI[cai-triage-llm] EU:HIGH OBSERVE decision=ESCALATE |
| 7 | GOVERNED_DECISION_BLOCKED | AI[cai-triage-llm] EU:UNACCEPTABLE OBSERVE decision=DENY |