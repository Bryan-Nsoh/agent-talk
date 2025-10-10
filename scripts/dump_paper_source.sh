#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(git rev-parse --show-toplevel)
PAPER_DIR="$ROOT_DIR/cert-talk-paper"
OUT="$ROOT_DIR/paper_source.tex"

if [[ ! -d "$PAPER_DIR" ]]; then
  echo "Error: $PAPER_DIR not found. Is the submodule initialized?" >&2
  exit 1
fi

{
  echo "% Auto-generated concatenation of the paper's TeX sources"
  echo "% Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "% Repo: $(basename "$ROOT_DIR")"
  echo "% Build figures before compiling this standalone source:"
  echo "%   ./scripts/build_figures.sh"
  echo "%   ./scripts/build_diagrams.sh"
  echo "% Then compile the paper inside cert-talk-paper as usual:"
  echo "%   cd cert-talk-paper && latexmk -pdf -silent main.tex"
  echo

  # Write preamble up to \begin{document}
  awk '1; /\\begin{document}/{exit}' "$PAPER_DIR/main.tex"

  echo "\\begin{document}"
  echo "\\maketitle"

  # Extract lines after \begin{document} that include \input{...} and inline them
  awk 'found{print} /\\begin{document}/{found=1}' "$PAPER_DIR/main.tex" | \
  while IFS= read -r line; do
    if [[ "$line" =~ ^\\input\{([^}]+)\} ]]; then
      relpath=${BASH_REMATCH[1]}
      texfile="$PAPER_DIR/${relpath}.tex"
      if [[ -f "$texfile" ]]; then
        echo "% ===== BEGIN: ${relpath}.tex ====="
        cat "$texfile"
        echo "% ===== END: ${relpath}.tex ====="
      else
        # keep literal line if file missing
        echo "$line"
      fi
    else
      echo "$line"
    fi
  done
} > "$OUT"

echo "Wrote $OUT"

