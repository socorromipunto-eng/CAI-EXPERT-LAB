# tools/

Build and packaging utilities for CAI-EXPERT-LAB. These scripts are not part
of the framework or of the execution engine.

## build-publication.ps1

Merges the Markdown in `CAI-Engine`, `docs`, `labs` and `legal`, followed by
`LICENSE.md`, into a single Word document for the copyright-deposit edition,
`CAI-EXPERT-LAB-Copyright-Edition.docx`.

- Requires PowerShell 7 (`pwsh`) and `pandoc`.
- Run it from the repository root:

  ```
  pwsh -NoProfile -File ./tools/build-publication.ps1
  ```

- It resolves the repository root from its own location, so it works from
  `tools/`.
- Output is written to `output/` at the repository root. The script deletes
  and recreates that folder on every run.
- The GitLab pipeline (`.gitlab-ci.yml`) runs this same script and publishes
  `output/` as a build artifact.

---

Copyright (c) 2025 Antonio José Socorro Marín. CAI-EXPERT-LAB. All Rights Reserved.
