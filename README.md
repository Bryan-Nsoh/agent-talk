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

## Quick Commands

Generate an instance cache (JSONL):

```bash
uv run python -m agent_talk.env.generator --out data/cache.jsonl --n 1000 --size 10 --seed 123
```

Run the main system on the cache:

```bash
uv run python -m agent_talk.runners.batch_eval --cache data/cache.jsonl --system certtalk --out out/certtalk.jsonl
```

Summarise metrics across systems:

```bash
uv run python -m agent_talk.analysis.metrics --inputs out/certtalk.jsonl --out out/summary.csv
```

## Testing

```bash
uv run pytest
```

All tests execute in a few seconds on CPU-only hardware.

## License

MIT
