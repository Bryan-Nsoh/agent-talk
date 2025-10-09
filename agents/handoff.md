# Agent Handoff Notes

- **Last update**: 2025-10-08 (post witness/probe upgrades)
- **Context**: Reruns at timestamps `20251008T173026Z` (CertTalk), `20251008T173537Z` (Send-All), `20251008T173601Z` (Greedy-Probe), `20251008T173800Z` (cut-only baseline) on the original 1k cache.
- **Key outcomes**:
  - CertTalk success 99.9%, median bytes ≈947, rounds ≈7, oracle acceptance 100%.
  - Greedy-Probe now matches CertTalk (uses the same improved policy).
  - Send-All unchanged (success 100%, 516 median bytes).
  - Existing cut-only baseline improved to ~22% success but still not competitive.
- **Pending work**:
  1. Design and implement the responder-led min-cut baseline to replace the weak `cutgrow` variant.
  2. Consider enabling multi-probe loops for pure cut mode (A-only) to push baseline success higher.
  3. Explore whether role handoff (`YIELD`) is still required now that probes clean up most loops; prototype if necessary.
  4. Once baseline is ready, rerun the 1k cache for all systems and regenerate summary plots.
- **Artifacts**:
  - Dataset cache `data/20251008T151417Z_cache.jsonl`.
  - New runs/logs under `runs/20251008T1730*_*.jsonl` and `logs/20251008T1730*_*.log`.
  - Diagnostics (belief sizes, failed digest counts) embedded in each run record.
