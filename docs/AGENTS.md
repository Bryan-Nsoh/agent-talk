# AGENT WORKFLOW HANDBOOK

_Last updated 2025-10-13_

This handbook documents how we organize experiments, documentation, and handoffs. It complements the codebase and keeps every run reproducible without guesswork.

## 1. Repository Landmarks

- `cert-talk-paper/`
  - `main.tex` — full paper.
  - `previews/main-idea.tex` & `previews/main-idea.pdf` — protocol overview and methodology reference.
  - `previews/main-brief.tex` & `previews/main-brief.pdf` — two-page idea brief.
  - `sections/` — shared LaTeX sections; edits here affect all paper variants.
- `docs/`
  - `AGENTS.md` — this handbook.
  - `notes/` — working notes (`paper_improvement_notes.md`, `paper_source.txt`).
  - `handoff/` — expert handoff templates and instructions.
- `agents_talk/` (Python package) and supporting folders (`configs/`, `scripts/`, `tests/`, `runs/`, `logs/`, `experiments/`).

## 2. Paper & Brief Maintenance

1. **Editing sections**
   - Modify files under `cert-talk-paper/sections/`.
   - Keep prose ASCII; avoid em-dashes.
2. **Regenerating PDFs** (run inside `cert-talk-paper/`):
   - Full paper: `make`
   - Methodology preview: `make preview` → outputs `previews/main-idea.pdf`
   - Two-page brief: `make brief` → outputs `previews/main-brief.pdf`
3. **Preview hygiene**
   - Do not hand-edit generated PDFs; always rebuild via `latexmk` through the make targets.
   - Commit `.tex` sources and PDFs; LaTeX auxiliary files are ignored.
4. **When adding a new variant**
   - Place sources under `cert-talk-paper/previews/` (or a dedicated subfolder) and adjust the Makefile accordingly.
   - Document the new artifact under “Documentation quick links” in `README.md`.

## 3. Experiment Organization Playbook

### 3.1 Before Launch
- Create or update an experiment README in the experiment folder with:
  - Objective and hypothesis.
  - Variables that will change and invariants that stay fixed.
  - Metrics to collect.
- Stage directories up front:
  - Logs: `logs/<YYYYMMDD_HHMMSSZ>_<label>.log`
  - Outputs: `runs/<YYYYMMDD_HHMMSSZ>_<label>/...`

### 3.2 During the Run
- Record the exact command in the README for reproducibility.
- Capture live observations (errors, latency swings, anomalies) while they happen.
- If parameters change mid-run, append _Adjustment_ notes with timestamps.
- Abort clearly failing runs; log that they were stopped and why.

### 3.3 After Completion
- Summarize in the experiment README:
  - Key numbers (throughput, bytes, success rate, etc.).
  - Whether the hypothesis held (yes/no/unclear + a sentence).
  - Any surprises or inconclusive outcomes.
  - Next actions or follow-up experiments.
- Link to artifacts (logs, JSONL outputs, CSV summaries) using relative paths.

### 3.4 Cleanup Checklist
- Archive temporary scripts/configs inside the experiment folder or delete them.
- Remove artifacts from aborted/superseded runs immediately.
- Update skill playbooks or this handbook if the process changes.
- Never infer conclusions unsupported by evidence; mark inconclusive runs explicitly.

## 4. File & Folder Discipline
- Keep documentation in `docs/` and the paper submodule—avoid scattering loose markdown or text files at the root.
- Committers must ensure new artifacts appear in `README.md` and, when relevant, in this handbook.
- Generated code snapshots (`ALL_PY_CODE.txt`) and large exports live under `docs/notes/` or a dedicated archive folder—do not leave them in the root.
- When introducing new tooling, document installation and usage beside the tool (`scripts/README.md` or similar).

## 5. Handoff Expectations
- Use templates in `docs/handoff/` for expert bundles.
- Populate every section honestly; note unknowns rather than omitting content.
- Include reproducible commands and reference the corresponding experiment folders.

## 6. Contact & Ownership
- Paper authors and documentation points of contact are listed in `CONTRIBUTORS.md` and mirrored in the LaTeX author blocks.
- Questions about the protocol or paper layout → ping the paper maintainers.
- Questions about experiments or pipelines → ping the core agents team.

```text
Version history:
2025-10-13  Reorganized doc structure and added paper build instructions.
2025-10-06  Initial experiment protocol draft.
```
