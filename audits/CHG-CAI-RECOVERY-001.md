# CHG-CAI-RECOVERY-001 — Documentation recovery and provenance

**Status:** PROPOSED — pending independent technical/governance review and owner approval for integration.
**Baseline commit:** `5fb11ce4ff6009d980d6d0862e7a507fca642ee5`
**Scope:** `README.md`, `CAI-Engine/README.md`, this audit record only.
**Category:** Documentation clarification; no changes to CORE, policy, license, code, tests or Git history.

## Observations

- Git stores the two README blobs with LF line endings; Windows working copies may use CRLF. Verification uses Git's configured normalization and compares against the pinned baseline blob IDs.
- The CAI Engine README contains a second plain-text rendition after `End of DocumentCAI Engine`. Semantic equivalence has **not** been proven. **No part of that rendition is deleted in this patch.**
- The reference implementation and proposed MCP security design must not be conflated with verified operational enforcement.
- The seven-stage operational lifecycle remains unchanged; it is an operational expression of CAI, not the entire CAI CORE definition.

## Controls and evidence

1. Pinned HEAD, clean worktree, exact normalized Git blob hashes and single known marker.
2. Diff and SHA-256 evidence for each proposed output, generated outside the repository.
3. Independent technical review of scope, rendering, references, provenance and semantic preservation.
4. Independent governance review and separate owner approval before integration, commit or publication.
5. AI-assisted drafting disclosed here; human authorship and legal ownership remain unchanged.

## Rollback

Discard the isolated worktree after review. Do not rewrite history, force push, or use `git reset --hard`.

## Open issue

The appended rendition requires a line-by-line semantic equivalence matrix before any future removal or consolidation. No deletion is authorized by this change.
