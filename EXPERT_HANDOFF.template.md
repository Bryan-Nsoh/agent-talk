Last updated: 2025-10-09 (UTC)

## Summary (raw)
<include path="runs/20251009T141250Z_summary.csv" lang="text" block="code"/>

## Dataset sample (raw)
<include path="data/20251008T151417Z_cache.jsonl" lang="json" head="3" block="code"/>

## Representative transcripts/logs (raw)
<include path="runs/20251009T141144Z_certtalk.jsonl" jsonl_match="seed=123" block="code"/>
<include path="runs/20251009T141144Z_certtalk.jsonl" jsonl_match="seed=129" block="code"/>

## Reproduction commands (raw)
```
uv venv && source .venv/bin/activate && uv pip install -e .[dev]
uv run python -m agent_talk.env.generator --out data/20251008T151417Z_cache.jsonl --n 1000 --size 10 --seed 123
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system certtalk --out runs/20251009T141144Z_certtalk.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system sendall --out runs/20251009T141244Z_sendall.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system greedyprobe --out runs/20251009T141246Z_greedyprobe.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system respondermincut --out runs/20251009T141248Z_respondmincut.jsonl
uv run python -m agent_talk.analysis.metrics --inputs runs/20251009T141144Z_certtalk.jsonl runs/20251009T141244Z_sendall.jsonl runs/20251009T141246Z_greedyprobe.jsonl runs/20251009T141248Z_respondmincut.jsonl --out runs/20251009T141250Z_summary.csv
```

## Code (verbatim, raw)
<include path="agent_talk/core/crc16.py" lang="python" block="code"/>
<include path="agent_talk/core/coords.py" lang="python" block="code"/>
<include path="agent_talk/core/rle.py" lang="python" block="code"/>
<include path="agent_talk/core/messages.py" lang="python" block="code"/>
<include path="agent_talk/core/protocol.py" lang="python" block="code"/>
<include path="agent_talk/env/grid.py" lang="python" block="code"/>
<include path="agent_talk/oracle/flow.py" lang="python" block="code"/>
<include path="agent_talk/oracle/oracle.py" lang="python" block="code"/>
<include path="agent_talk/agents/fsm_base.py" lang="python" block="code"/>
<include path="agent_talk/agents/agent_a.py" lang="python" block="code"/>
<include path="agent_talk/agents/agent_b.py" lang="python" block="code"/>
<include path="agent_talk/agents/responder_mincut.py" lang="python" block="code"/>
<include path="agent_talk/runners/simulate.py" lang="python" block="code"/>
<include path="agent_talk/runners/batch_eval.py" lang="python" block="code"/>

