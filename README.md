# Beta: Proof-of-Path Agent Talk

This repository contains a reference implementation of the **Beta: Proof-of-Path Agent Talk** experiment. Two deterministic finite-state agents exchange typed JSON messages to establish whether a start cell can reach a goal cell on the union of their private binary occupancy grids. Conversations terminate with machine-checkable certificates—either a path witness or a cut witness—that an oracle verifies exactly.

## Getting Started

The project targets Python 3.11 and has no mandatory third-party dependencies.

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

Optional analysis utilities live under the `analysis` extra:

```bash
uv pip install -e ".[analysis]"
```

## Repository Layout

```
agent_talk/
  core/        # codecs, CRC16, message schema, protocol utilities
  env/         # grid models and instance generation
  agents/      # deterministic FSM agents
  oracle/      # union-map verifier and flow routines
  runners/     # single-run and batch evaluation drivers
  analysis/    # metric aggregation and plotting
  io/          # cache and log interfaces
configs/       # YAML configs for main and ablation runs
scripts/       # convenience CLI wrappers
tests/         # unit tests covering codecs, messages, oracle, protocol, agents
```

## Latest Results (2025-10-09 SCHEMA-free rerun)

- CertTalk: success 1.000, median 468.5 bytes / 5 rounds.
- Send-All: success 1.000, median 466.0 bytes / 3 rounds.
- Greedy-Probe: success 1.000, median 635.5 bytes / 5 rounds.
- Responder-MinCut: success 0.205, median 667.0 bytes / 6 rounds.

Full summaries live in `runs/20251009T165537Z_summary.csv` with transcripts under `experiments/transcripts/`.

## Reproduce the 1k Run

Generate the shared cache:

```bash
uv run python -m agent_talk.env.generator --out data/20251008T151417Z_cache.jsonl --n 1000 --size 10 --seed 123
```

Run CertTalk and baselines (SCHEMA-free protocol):

```bash
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system certtalk --out runs/20251009T165448Z_certtalk.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system sendall --out runs/20251009T165501Z_sendall.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system greedyprobe --out runs/20251009T165507Z_greedyprobe.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system respondermincut --out runs/20251009T165521Z_respondmincut.jsonl
```

Aggregate metrics:

```bash
uv run python -m agent_talk.analysis.metrics --inputs \
  runs/20251009T165448Z_certtalk.jsonl \
  runs/20251009T165501Z_sendall.jsonl \
  runs/20251009T165507Z_greedyprobe.jsonl \
  runs/20251009T165521Z_respondmincut.jsonl \
  --out runs/20251009T165537Z_summary.csv
```

## Testing

```bash
uv run pytest
```

All tests execute in a few seconds on CPU-only hardware.

## License

MIT
