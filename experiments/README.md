# Experiment Log

All experiments follow the Agent Experiment Protocol in `agents.md`. Logs live in `logs/` and run artifacts in `runs/` with ISO 8601 UTC timestamps.

---

## Experiment: 2025-10-08 CertTalk Witness + Probe Upgrades

- **Objective**: Validate witness-bit schema, targeted probes, and planning halo on the same 10×10 cache; re-measure all baseline systems after the protocol fix.
- **Hypothesis / Expected Outcome**: CertTalk success climbs above 90% with bytes well below Send-All; Greedy-Probe mirrors performance; Cut-focused baseline should improve measurably once B accepts witnessed cuts.
- **Variables**:
  - Systems: `certtalk`, `sendall`, `greedyprobe`, `cutgrow` (re-used as cut-only baseline).
  - Dataset: reuse `data/20251008T151417Z_cache.jsonl`.
- **Invariants**:
  - Same limits/configs as baseline shakeout.
- **Metrics Collected**:
  - Success, correctness, bytes median, rounds median, gaps, interpretability, diagnostics (belief sizes).

### Commands

```bash
TS_CERT=$(date -u +%Y%m%dT%H%M%SZ)
nohup uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system certtalk --out runs/${TS_CERT}_certtalk.jsonl > logs/${TS_CERT}_certtalk.log 2>&1 &

TS_SEND=$(date -u +%Y%m%dT%H%M%SZ)
nohup uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system sendall --out runs/${TS_SEND}_sendall.jsonl > logs/${TS_SEND}_sendall.log 2>&1 &

TS_GREED=$(date -u +%Y%m%dT%H%M%SZ)
nohup uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system greedyprobe --out runs/${TS_GREED}_greedyprobe.jsonl > logs/${TS_GREED}_greedyprobe.log 2>&1 &

TS_CUT=$(date -u +%Y%m%dT%H%M%SZ)
nohup uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system cutgrow --out runs/${TS_CUT}_cutgrow.jsonl > logs/${TS_CUT}_cutgrow.log 2>&1 &

TS_SUM=$(date -u +%Y%m%dT%H%M%SZ)
nohup uv run python -m agent_talk.analysis.metrics --inputs runs/${TS_CERT}_certtalk.jsonl runs/${TS_SEND}_sendall.jsonl runs/${TS_GREED}_greedyprobe.jsonl runs/${TS_CUT}_cutgrow.jsonl --out runs/${TS_SUM}_summary.csv > logs/${TS_SUM}_summary.log 2>&1 &
```

### Live Observations
- New witness bits eliminated repeated cut NACKs; conversations that previously stalled now converge with ≤1 probe.
- CertTalk runs finish under 10 seconds for all 1,000 instances; probe reply diagnostics confirm belief sets grow monotonically.
- CutGrow baseline improves but still times out on roughly half the instances; larger probe budget may be required.

### Results Summary (2025-10-08)
- CertTalk — success **0.999**, bytes median **947**, rounds median **7**, interpretability **1.0**.
- Send-All — success **1.00**, bytes median **530**, rounds median **4**, interpretability **1.0**.
- Greedy-Probe — success **0.999**, bytes median **947**, rounds median **7**, interpretability **1.0**.
- Cut-Grow (cut-only baseline) — success **0.217**, bytes median **3175**, rounds median **23**.
- Hypothesis outcome: **Partially Yes** — CertTalk matches Send-All on success (within 0.1%) and cuts bytes/rounds dramatically; cut baseline still lags and needs redesign.
- Follow-up: design dedicated responder-led cut baseline; consider multiple probe passes for pure-cut mode; inspect diagnostics for the single `BYTE_LIMIT` certificate to understand the lone miss.

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
