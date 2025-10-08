# Experiment Log

All experiments follow the Agent Experiment Protocol in `agents.md`. Logs live in `logs/` and run artifacts in `runs/` with ISO 8601 UTC timestamps.

---

## Experiment: 2025-10-08 CertTalk Baseline Shakeout

- **Objective**: Validate end-to-end evaluation stack on the default 10×10 dataset; capture baseline metrics for CertTalk versus Send-All, Greedy-Probe, and Cut-Grow.
- **Hypothesis / Expected Outcome**: CertTalk matches Send-All on success while using ≥25% fewer bytes and ≤2 fewer median rounds than Greedy-Probe on this sample; baseline systems run without protocol violations.
- **Variables**:
  - System under test: `certtalk`, `sendall`, `greedyprobe`, `cutgrow`.
  - Dataset sample size: 1000 instances (`--n 1000`).
- **Invariants**:
  - Grid size 10×10, seeds starting at 123, base protocol limits from `configs/base.yaml`.
  - Message schema `schema=v1` and default RLE/delta encodings.
- **Metrics Collected**:
  - Success rate, correctness, bytes median, rounds median, path gap median, cut gap median, interpretability.

### Planned Commands

```bash
# Generate dataset cache
uv run python -m agent_talk.env.generator --out data/20251008T151417Z_cache.jsonl --n 1000 --size 10 --seed 123

# Evaluate all systems
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system certtalk --out runs/20251008T151417Z_certtalk.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system sendall --out runs/20251008T151417Z_sendall.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system greedyprobe --out runs/20251008T151417Z_greedyprobe.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system cutgrow --out runs/20251008T151417Z_cutgrow.jsonl

# Summarise metrics
uv run python -m agent_talk.analysis.metrics --inputs runs/20251008T151417Z_*.jsonl --out runs/20251008T151417Z_summary.csv
```

### Live Observations
- 15:14 UTC: Initial `cutgrow` batch evaluation hit the 10s CLI timeout; relaunched under `nohup` and completed without stdout output (log file remains empty).
- Runs completed without protocol exceptions; dataset generation produced exactly 1000 instances.

### Results Summary
- Key metrics (test split = all, 1000 instances):
  - CertTalk — success 0.23, bytes median 3128, rounds median 21, path gap 0, interpretability 0.23.
  - Send-All — success 1.00, bytes median 516, rounds median 4, path gap 0, interpretability 1.00.
  - Greedy-Probe — success 0.24, bytes median 3126, rounds median 20, path gap 0, interpretability 0.24.
  - Cut-Grow — success 0.00, bytes median 3139, rounds median 22, interpretability 0.00.
- Hypothesis outcome: **No** — CertTalk underperformed Send-All on both success rate and bytes; additional debugging required before rerunning baseline comparison.
- Follow-up: Investigate why CertTalk (and Cut-Grow) stall at ~23% success despite zero path gaps on successful cases; inspect transcripts in `runs/20251008T151417Z_*.jsonl` and adjust agent policies.

---
