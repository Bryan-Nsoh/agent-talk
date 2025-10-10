#!/usr/bin/env bash
set -euo pipefail

uv run python -m agent_talk.analysis.plots_sns
echo "Wrote figures under cert-talk-paper/figs"

