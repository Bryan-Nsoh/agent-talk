#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(git rev-parse --show-toplevel)
PAPER_DIR="$ROOT_DIR/cert-talk-paper"
OUT="$ROOT_DIR/paper_source.txt"

if [[ ! -d "$PAPER_DIR" ]]; then
  echo "Error: $PAPER_DIR not found. Is the submodule initialized?" >&2
  exit 1
fi

{
  echo "# CertTalk Paper Source (plain text)"
  echo "Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo
  echo "This file replaces the old TeX dump at repo root. It points to the canonical LaTeX (in cert-talk-paper) and embeds the exact code that generates all figures/diagrams."
  echo
  echo "## How To Reproduce Figures"
  echo "- Generate statistical figures (bytes/rounds/mix):"
  echo '  $ ./scripts/build_figures.sh'
  echo "- Generate sequence diagrams (Mermaid -> PDF):"
  echo '  $ ./scripts/build_diagrams.sh   # requires: npm i -g @mermaid-js/mermaid-cli'
  echo
  echo "Artifacts are written under cert-talk-paper/figs. The PDF is built via:"
  echo '  $ (cd cert-talk-paper && latexmk -pdf -silent main.tex)'
  echo
  echo "## Certificate Examples (verbatim JSON)"
  # Print first lstlisting block (PATH_CERT)
  echo '```json'
  awk 'BEGIN{n=0;p=0} /\\begin\{lstlisting\}/{n++; if(n==1){p=1;next}} /\\end\{lstlisting\}/{if(p){p=0;print ""}; next} {if(p) print}' "$PAPER_DIR/sections/artifacts_overview.tex"
  echo '```'
  echo
  # Print second lstlisting block (CUT_CERT)
  echo '```json'
  awk 'BEGIN{n=0;p=0} /\\begin\{lstlisting\}/{n++; if(n==2){p=1;next}} /\\end\{lstlisting\}/{if(p){p=0;print ""}; next} {if(p) print}' "$PAPER_DIR/sections/artifacts_overview.tex"
  echo '```'
  echo
  echo "## Python Code That Generates Statistical Figures"
  echo '```python'
  cat "$ROOT_DIR/agent_talk/analysis/plots_sns.py"
  echo '```'
  echo
  echo "## Mermaid Sources For Sequence Diagrams"
  for f in "$ROOT_DIR"/diagrams/seq_*.mmd; do
    name=$(basename "$f")
    echo "### $name"
    echo '```mermaid'
    cat "$f"
    echo '```'
    echo
  done
} > "$OUT"

echo "Wrote $OUT"
