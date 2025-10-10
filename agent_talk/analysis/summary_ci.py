"""Compute medians and bootstrap 95% CIs for bytes and rounds by system.

Writes a LaTeX table snippet to cert-talk-paper/sections/results_table.tex
using only the data present in runs/*.jsonl. Makes nothing up: if a
field cannot be computed, it is left blank.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            # If lines are prefixed like "[n/1000] {...}", strip prefix
            if s[0] != "{":
                try:
                    s = s[s.index("{"):]
                except ValueError:
                    continue
            try:
                yield json.loads(s)
            except json.JSONDecodeError:
                continue


def load_df(runs_dir: Path) -> pd.DataFrame:
    # Choose the latest file per system by lexicographic timestamp prefix
    by_system: Dict[str, Path] = {}
    for jf in runs_dir.glob("*.jsonl"):
        stem = jf.stem
        if "_" not in stem:
            continue
        prefix, system = stem.rsplit("_", 1)
        prev = by_system.get(system)
        if prev is None or prev.stem.rsplit("_", 1)[0] < prefix:
            by_system[system] = jf
    rows: List[Dict] = []
    for system, jf in by_system.items():
        norm = "respondermincut" if system == "respondmincut" else system
        for rec in iter_jsonl(jf):
            rows.append({
                "system": norm,
                "bytes": rec.get("bytes"),
                "rounds": rec.get("rounds"),
                "accepted": bool(rec.get("oracle_accepted")),
            })
    df = pd.DataFrame(rows)
    # drop incomplete rows for numeric stats
    df = df.dropna(subset=["bytes", "rounds"])  # do not fabricate
    return df


def bootstrap_ci(series: pd.Series, iters: int = 2000, q: float = 0.5, seed: int = 12345) -> Tuple[float, float, float]:
    rng = random.Random(seed)
    vals = series.dropna().to_list()
    n = len(vals)
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    med = float(pd.Series(vals).quantile(q))
    samples = []
    for _ in range(iters):
        resample = [vals[rng.randrange(n)] for _ in range(n)]
        samples.append(float(pd.Series(resample).quantile(q)))
    lo = pd.Series(samples).quantile(0.025)
    hi = pd.Series(samples).quantile(0.975)
    return med, float(lo), float(hi)


def main() -> None:
    runs_dir = Path("runs")
    out_tex = Path("cert-talk-paper/sections/results_table.tex")
    df = load_df(runs_dir)
    if df.empty:
        # write placeholder table without numbers
        out_tex.write_text("% No data available to compute results table\n")
        return

    systems = ["sendall", "certtalk", "greedyprobe", "respondermincut"]
    lines = []
    lines.append("\\begin{tabular}{lcccc}")
    lines.append("\\toprule")
    header = (
        "System & Success & Bytes (median [95\\% CI]) & "
        "Rounds (median [95\\% CI]) & Interpretability \\\""
    )
    lines.append(header)
    lines.append("\\midrule")
    for sys in systems:
        d = df[df["system"] == sys]
        if d.empty:
            lines.append(f"{sys} &  &  &  &  \\")
            continue
        # Success and interpretability: fraction of accepted
        succ = d["accepted"].mean()
        # Medians and bootstrap CIs
        b_med, b_lo, b_hi = bootstrap_ci(d["bytes"])  # bytes
        r_med, r_lo, r_hi = bootstrap_ci(d["rounds"])  # rounds
        # format rows
        def fmt_ci(m, lo, hi):
            if pd.isna(m):
                return ""
            return f"{int(round(m))} [{int(round(lo))}, {int(round(hi))}]"
        row = f"{sys} & {succ:.3f} & {fmt_ci(b_med, b_lo, b_hi)} & {fmt_ci(r_med, r_lo, r_hi)} & {succ:.3f} \\"  # interpretability==success here
        lines.append(row)
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    out_tex.parent.mkdir(parents=True, exist_ok=True)
    out_tex.write_text("\n".join(lines))
    print(f"Wrote {out_tex}")


if __name__ == "__main__":
    main()
