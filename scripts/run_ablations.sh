#!/usr/bin/env bash
set -euo pipefail

CACHE=${1:-data/cache.jsonl}
OUT=${2:-out/ablations}
ABLAS=("delta_off" "rle_off" "cut_only" "path_only" "grid16")

mkdir -p "$OUT"

for tag in "${ABLAS[@]}"; do
  echo "Running ablation $tag..."
  uv run python -m agent_talk.runners.batch_eval --cache "$CACHE" --system "certtalk" --ablation "$tag" --out "$OUT/${tag}.jsonl"
done
