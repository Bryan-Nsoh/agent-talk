#!/usr/bin/env bash
set -euo pipefail

CACHE=${1:-data/cache.jsonl}
OUT=${2:-out}
SYSTEMS=("certtalk" "sendall" "greedyprobe" "cutgrow")

mkdir -p "$OUT"

for system in "${SYSTEMS[@]}"; do
  echo "Running $system..."
  uv run python -m agent_talk.runners.batch_eval --cache "$CACHE" --system "$system" --out "$OUT/${system}.jsonl"
done
