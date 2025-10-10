#!/usr/bin/env bash
set -euo pipefail

out_dir="cert-talk-paper/figs"
mkdir -p "$out_dir"

for name in seq_certtalk seq_sendall seq_greedyprobe seq_respondermincut; do
  mmdc -i "diagrams/${name}.mmd" -o "${out_dir}/${name}.pdf" -b transparent -w 1400 || {
    echo "mmdc failed for ${name}; ensure @mermaid-js/mermaid-cli is installed" >&2
    exit 1
  }
done

echo "Mermaid diagrams (PDF) written to ${out_dir}"
