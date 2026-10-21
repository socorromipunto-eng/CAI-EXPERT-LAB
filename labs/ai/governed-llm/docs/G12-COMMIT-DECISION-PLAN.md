# G12-GIT-001 — When to commit (PROPOSED, NOT AUTHORIZED)

Default proposal: GATE 15, after G12 executable outcome proof, G13 adversarial evaluation, G14 independent human technical/governance assessment, and G15 integration preflight and staged-diff inspection.

An **earlier documentation or source checkpoint** after G12 is a valid alternative only if owner separately approves (1) the exact copy/staging scope, (2) the reviewed staged diff and target branch/baseline, (3) the specific commit, and (4) the later push. Each decision is independent; mere approval of G12 authorizes only isolated development, not copy/commit.

Proposed eventual destination, NOT created by this bundle:
`C:\CAI-EXPERT-LAB\docs\Extensions\CAI-Governed-LLM\` for reviewed documentation; an approved source tree must be separately designated outside CORE, with explicit segregation from historical draft bundles. Never assume `v0.3.4` can replace an existing path without checking its state.

Preflight: verify real HEAD, clean/expected worktree, named files only, no tracked-path collisions, integrity SHA, copyright, provenance, no secrets/key files, manifest, Git diff --check and deterministic tests. Capture reviewer's name/time and independent audit dispositions. Copy ≠ stage ≠ commit ≠ push; rollback via copy deletion before commit and approved Git revert after commit. No force push.
