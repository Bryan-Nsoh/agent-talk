# Figure Build Notes

This repository produces two families of figures for the paper:

1) Sequence diagrams (Mermaid → PDF)
2) Statistical plots (Seaborn/Matplotlib → PDF)

Everything is rendered to vector PDFs under `cert-talk-paper/figs/` and included in LaTeX.

## 1) Mermaid sequence diagrams

Sources:

- `diagrams/seq_certtalk.mmd`
- `diagrams/seq_sendall.mmd`
- `diagrams/seq_greedyprobe.mmd`
- `diagrams/seq_respondermincut.mmd`

Build all (PDF):

```
npm install -g @mermaid-js/mermaid-cli
./scripts/build_diagrams.sh
```

Direct single-file render (example):

```
mmdc -i diagrams/seq_certtalk.mmd -o cert-talk-paper/figs/seq_certtalk.pdf -b transparent -w 1400
```

LaTeX includes (see `sections/communication_patterns.tex`):

```
\includegraphics[width=\linewidth]{figs/seq_certtalk.pdf}
```

## 2) Seaborn plots from JSONL logs

Script:

- `agent_talk/analysis/plots_sns.py`

Dependencies:

```
uv pip install -e .[analysis]
```

Build all plot PDFs:

```
./scripts/build_figures.sh
```

This writes:

- `figs/bytes_by_system.pdf`
- `figs/rounds_by_system.pdf`
- `figs/bytes_vs_rounds.pdf`
- `figs/byte_mix_stacked.pdf`

LaTeX includes (see `sections/results.tex`).

## 3) Compile the paper

```
cd cert-talk-paper
latexmk -pdf -silent main.tex
```

Vector-only policy: The paper includes PDF figures only. Raster PNGs are ignored by `.gitignore` and not referenced by LaTeX.

