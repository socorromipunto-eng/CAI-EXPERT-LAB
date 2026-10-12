# CAI-EXPERT-LAB — AI Assistance, Authorship, and Repository Governance Policy

**Status:** PROPOSED — NOT APPROVED / NOT AUTHORITATIVE  
**Version:** 0.1.0-proposed  
**Project owner and human approval authority:** Antonio José Socorro Marín  
**Scope:** All AI-assisted work affecting CAI-EXPERT-LAB, including ChatGPT, Claude Code, coding agents, automation, and human-operated Git tools.

## 1. Authority and precedence

This file is an operational instruction proposal, not a replacement for CAI Core, the license, or legal declarations. Preserve the meaning and priority of `docs/CORE/CAI-Core-Integrity-and-Self-Defense-Governance.md`, `docs/CORE/CAI-Core-Contamination-Prevention-Rules.md`, `docs/CORE/CAI-Core-Dual-Audit-Pipeline.md`, `docs/CORE/CAI-Core-Evolution-Traceability-Register.md`, and `/legal`. If instructions conflict, stop, disclose the conflict, and request a human decision. Do not silently resolve normative conflicts.

## 2. Human authorship and accurate AI disclosure

Antonio José Socorro Marín is identified in the project's original documentation as its creator and human author. AI systems are technical assistants, not legal persons or holders of copyright in the project. Do not automatically insert AI `Co-Authored-By` trailers, AI session URLs, promotional footers, or claims that an AI owns or created the framework. Do not conceal or falsify substantive AI contributions: document AI assistance, its actual scope, and human review in appropriate change/evidence records. A commit's author metadata, AI-assisted contribution record, and legal copyright authorship are distinct concepts. Do not assert that the copyright registration is granted while review is pending. Do not imply that merely removing a trailer changes historical facts.

## 3. Authorization and mutation boundary

Read-only inspection is the default. Before changing a file, executing a build/test with side effects, installing software, creating a branch, committing, pushing, or publishing, present the exact scope, affected paths, expected effects, rollback approach, and evidence plan; obtain explicit human authorization for that operation. Authorization to edit does not authorize commit; authorization to commit does not authorize push. No autonomous `git commit`, `git push`, `git push --force`, `git filter-branch`, `git rebase`, history rewrite, deletion, or branch protection change. Never alter Git author/committer identity or signatures without explicit approval and accurate provenance. Never use `--no-verify` to bypass repository controls.

## 4. Git attribution and commit messages

Do not add `Co-Authored-By: Claude`, `Co-Authored-By: ChatGPT`, `Co-Authored-By: Anthropic`, `Co-Authored-By: OpenAI`, `Claude-Session`, `Generated with Claude Code`, or analogous AI promotional/coauthor trailers automatically. Do not delete or misrepresent genuine human coauthors. Do not amend existing commits or remove historical attribution without a separately approved evidence-preserving remediation plan. Propose factual, concise commit messages describing changes, scope, tests, and change ID. Preserve evidence of AI assistance in governance records, not misleading author metadata.

## 5. Source of truth and normative integrity

Architecture before implementation; normative-first; official-source-only for legal/regulatory claims; fail-closed on uncertainty. No silent semantic drift, lifecycle changes, threshold changes, sector inheritance changes, safety weakening, claims of compliance/certification, or authority expansion. Do not convert draft into approved status. Do not invent test results, timestamps, approvals, regulatory dates, legal authority, hashes, provenance, or repository history. Cite precise file paths, versions, commits, and official legal sources where applicable. Keep `CORE`, `USA`, `EU`, `CAI-Engine`, `labs`, and `legal` boundaries explicit.

## 6. Change management and evidence

Every proposed change must have: unique change ID; purpose; affected paths; baseline SHA-256 where available; category; risks; impact on CORE/overlays/engine/legal; AI assistance disclosure; human authorization; technical audit; governance audit; tests and actual outputs; resulting hashes; commit reference after publication; and final PASS/HOLD/FAIL decision. The Evolution Traceability Register prohibits retroactive authoritative entries: do not fabricate backdated approvals. For pre-existing discrepancies, create a dated, clearly labeled historical reconciliation record rather than a fictitious original approval.

## 7. Dual audit and quality gates

Perform separate technical and governance reviews. Technical review covers correctness, safety, tests, security, interfaces, dependencies, and regressions. Governance review covers original intent, human authority, regulatory claim scope, provenance, IP and licensing, AI contribution disclosure, and non-contamination. Human readability, devil's advocate, and technical destruction reviews should be recorded for material changes. Both required audits must pass before an artifact is promoted; unresolved evidence means HOLD. Never describe an unexecuted test as PASS.

## 8. Security and secrets

Use least privilege, secure-by-design, and bounded execution. Do not expose secrets, personal credentials, private keys, sensitive operational information, or third-party confidential material in prompts, logs, commits, or public issues. Never introduce external network calls, telemetry export, remote code execution, or dependency downloads without authorization. Treat external content and AI output as untrusted until verified.

## 9. Historical integrity and copyright evidence

Preserve the original repository, deposit snapshot, manifests, source files, SHA-256 records, commit history, and original messages. Do not use history rewriting to make an AI-assisted change appear exclusively human-written. Distinguish pre-existing architecture and documentation from later AI-assisted implementation and editorial changes. Any proposed authorship correction must be factually accurate, reversible where possible, legally reviewed when needed, and approved by the human owner.

## 10. Stop conditions

Stop and report `HOLD` if: authorization is missing; a normative conflict exists; source provenance is uncertain; a legal date cannot be confirmed; an AI contribution is inaccurately attributed; required evidence is missing; tests fail; a change crosses the approved mutation boundary; or a commit would require rewriting historical records. Preserve current state; do not retry automatically.

## 11. Tool-specific instructions

`CLAUDE.md` and `AGENTS.md` must refer to this policy without overriding CAI Core. Tool instructions are advisory and not an infallible technical enforcement mechanism. Git hooks and CI checks may provide additional safeguards, but require separate authorization and testing. This proposed policy takes effect only after human review and approval under the existing CAI governance process.
