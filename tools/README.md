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

## md-structure.py

Run `python tools/md-structure.py <document.md>` to inspect a conversion
candidate without writing the document. `OK` means only the implemented
word-sequence comparison passed; it is not semantic, rendering or governance
approval. Review the diff, code fences, lists, tables and rendered output.
Use the applicable document-family and freeze/adoption rules before any write.
Do not bulk-convert historical evidence or assume one layout fits every family.

---

Copyright (c) 2025 Antonio José Socorro Marín. CAI-EXPERT-LAB. All Rights Reserved.
