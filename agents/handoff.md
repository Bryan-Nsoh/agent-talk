# Agent Handoff Notes

- **Last update**: 2025-10-09 (post SCHEMA removal rerun)
- **Context**: Re-ran the fixed 1k cache with SCHEMA-free CertTalk/Greedy-Probe at timestamps `20251009T165448Z` (CertTalk), `20251009T165501Z` (Send-All), `20251009T165507Z` (Greedy-Probe), `20251009T165521Z` (Responder-MinCut). Metrics aggregated at `20251009T165537Z`.
- **Key outcomes**:
  - CertTalk now succeeds on 100% of instances with median **468.5 bytes / 5 rounds**, oracle acceptance 100%.
  - Greedy-Probe mirrors CertTalk’s behaviour (100% success, 635.5 bytes / 5 rounds) and serves as the ablation without path-first bias.
  - Send-All remains the 466-byte / 3-round reference; parity achieved without SCHEMA overhead.
  - Responder-MinCut baseline still delivers 20.5% success with single-probe retry; no regression from handshake removal.
- **Pending work**:
  1. (Optional) Iterate on Responder-MinCut to raise success if a stronger cut-only baseline is desired; otherwise freeze.
  2. Prepare publication assets (plots, paper text) using the 20251009 artefacts.
- **Artifacts**:
  - Dataset cache: `data/20251008T151417Z_cache.jsonl`.
  - Runs: `runs/20251009T165448Z_certtalk.jsonl`, `runs/20251009T165501Z_sendall.jsonl`, `runs/20251009T165507Z_greedyprobe.jsonl`, `runs/20251009T165521Z_respondmincut.jsonl`.
  - Summary: `runs/20251009T165537Z_summary.csv`.
  - Representative transcripts (seed 123): `experiments/transcripts/20251009T1655_*.json`.
  - Prior artefacts (20251008 witness/probe upgrades) retained for historical comparison.
