# Agent Handoff Notes

- **Last update**: 2025-10-08
- **Context**: Baseline experiment `20251008T151417Z` completed for systems CertTalk, Send-All, Greedy-Probe, Cut-Grow on 1000 generated 10×10 instances.
- **Key outcomes**:
  - CertTalk success 0.23 vs Send-All 1.00; bytes and rounds significantly higher than expected.
  - Greedy-Probe mirrors CertTalk success (~0.24).
  - Cut-Grow failed entirely (0.00 success).
- **Pending work**:
  1. Inspect representative transcripts in `runs/20251008T151417Z_certtalk.jsonl` and `runs/20251008T151417Z_cutgrow.jsonl` to diagnose failure modes (likely repeated NACK loops or premature DONE messages).
  2. Update agent policies or fallback heuristics to improve success beyond 90% before rerunning the baseline comparison.
  3. Once fixes land, repeat the experiment following the existing README checklist and append new results.
- **Artifacts**: Dataset cache `data/20251008T151417Z_cache.jsonl`, run logs/outputs under `logs/` and `runs/` with matching timestamps.
