# Agent Experiment Protocol

Last updated 2025-10-06 — Ground rules for documenting experiments so future runs never guess at intent. Still required: keeps hypotheses, knobs, outcomes, and honest confidence levels legible.

## Experiment Organization Playbook

### 1. Before Launch
- Create or update the experiment README (same folder as scripts/configs) with:
  - Objective (what we are testing or learning)
  - Hypothesis / expected outcome
  - Variables we will change
  - Invariants (what stays fixed)
  - Metrics we will collect
- Name logs and output directories with ISO 8601 timestamps: `logs/<YYYYMMDD_HHMMSSZ>_<label>.log`, `runs/<label>/...`.

### 2. During the Run
- Mirror the command in the README verbatim so it is reproducible.
- Capture live observations (errors, latency jumps, unexpected behavior) in a short bullet list.
- If parameters change mid-run, append “Adjustment” notes with time stamps.
- If the run is failing or clearly uninformative, say so immediately—do not continue just to “get data.”

### 3. After Completion
- Summarize outcomes directly in the README:
  - Key numbers (throughput, accuracy, cost)
  - Did the hypothesis hold? (yes/no/unclear + one sentence of justification)
  - If the run taught us nothing or contradicted expectations, state that candidly.
  - Follow-up actions or next experiments
- Link to artifacts (logs, JSON summaries, exported CSVs) using relative paths.

### 4. Cleanup Checklist
- Ensure `agents/handoff.md` notes the latest run state and where to pick up.
- Archive stray scripts/configs into the experiment folder or delete them—no loose files at repo root.
- Delete artifacts from aborted or superseded runs immediately (logs, `runs/<id>`, resume files)—do not leave half-finished outputs lying around.
- Update the skills catalog or related playbooks if the process changed.
- Never infer “learnings” that the evidence does not support. If a run was inconclusive, mark it inconclusive.
