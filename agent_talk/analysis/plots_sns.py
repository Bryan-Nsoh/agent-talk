"""Seaborn plots for bytes/rounds and message-mix figures.

Usage:
  uv run python -m agent_talk.analysis.plots_sns
This writes PNGs under cert-talk-paper/figs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, Iterator

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def iter_jsonl_records(path: Path) -> Iterator[dict]:
    """Yield dicts from a JSONL file. Be resilient to prefix like "[1/1000] {..}"."""
    patt = re.compile(r"\{.*\}$")
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            s = line.strip()
            if not s:
                continue
            m = patt.search(s)
            if m:
                s = m.group(0)
            try:
                yield json.loads(s)
            except json.JSONDecodeError:
                continue


def load_runs(runs_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, msg_rows = [], []
    for jf in runs_dir.glob("*.jsonl"):
        system = jf.stem.split("_", 1)[0]
        for rec in iter_jsonl_records(jf):
            seed = rec.get("seed")
            outcome = rec.get("outcome")
            rounds = rec.get("rounds")
            totalB = rec.get("bytes")
            ctype = rec.get("certificate_type")
            accepted = rec.get("oracle_accepted")
            trans = rec.get("transcript", [])
            if totalB is None and trans:
                totalB = sum(m.get("bytes", 0) for m in trans)
            rows.append({
                "system": system,
                "seed": seed,
                "rounds": rounds,
                "total_bytes": totalB,
                "certificate_type": ctype,
                "accepted": bool(accepted),
                "n_messages": len(trans),
                "outcome": outcome,
            })
            for i, m in enumerate(trans):
                try:
                    inner = json.loads(m.get("message", "{}"))
                except Exception:
                    inner = {}
                msg_rows.append({
                    "system": system,
                    "seed": seed,
                    "i": i,
                    "bytes": m.get("bytes", 0),
                    "sender": m.get("sender"),
                    "type": inner.get("t"),
                })
    df_runs = pd.DataFrame(rows).dropna(subset=["total_bytes", "rounds"])  # ensure numeric
    df_msgs = pd.DataFrame(msg_rows)
    return df_runs, df_msgs


def style_paper():
    sns.set_theme(style="whitegrid", context="paper")
    plt.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "axes.titlelocation": "left",
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
    })


def ensure_outdir() -> Path:
    out = Path("cert-talk-paper/figs")
    out.mkdir(parents=True, exist_ok=True)
    return out


def plot_bytes(df: pd.DataFrame, outdir: Path, order: list[str]):
    plt.figure()
    ax = sns.boxenplot(data=df, x="system", y="total_bytes", order=order, showfliers=False)
    sns.stripplot(data=df, x="system", y="total_bytes", order=order, alpha=0.25, size=2, ax=ax)
    ax.set(xlabel="", ylabel="Bytes per transcript")
    plt.title("Communication cost", loc="left")
    plt.tight_layout()
    plt.savefig(outdir / "bytes_by_system.pdf")
    plt.close()


def plot_rounds(df: pd.DataFrame, outdir: Path, order: list[str]):
    plt.figure()
    ax = sns.boxenplot(data=df, x="system", y="rounds", order=order, showfliers=False)
    sns.stripplot(data=df, x="system", y="rounds", order=order, alpha=0.25, size=2, ax=ax)
    ax.set(xlabel="", ylabel="Messages (rounds)")
    plt.title("Dialogue length", loc="left")
    plt.tight_layout()
    plt.savefig(outdir / "rounds_by_system.pdf")
    plt.close()


def plot_scatter(df: pd.DataFrame, outdir: Path):
    plt.figure()
    ax = sns.scatterplot(
        data=df, x="rounds", y="total_bytes", hue="system",
        alpha=0.5, s=12, edgecolor="none"
    )
    ax.set(xlabel="Messages (rounds)", ylabel="Bytes per transcript")
    plt.title("Bytes vs. rounds", loc="left")
    plt.tight_layout()
    plt.savefig(outdir / "bytes_vs_rounds.pdf")
    plt.close()


def plot_byte_mix(dm: pd.DataFrame, outdir: Path, order: list[str]):
    by_type = (
        dm.groupby(["system", "type"], observed=True)["bytes"].sum().reset_index()
    )
    tot = by_type.groupby("system", observed=True)["bytes"].transform("sum")
    by_type["pct"] = 100 * by_type["bytes"] / tot
    top_types = by_type.groupby("type")["bytes"].sum().nlargest(6).index
    by_type["type2"] = by_type["type"].where(by_type["type"].isin(top_types), "OTHER")
    wide = (
        by_type.groupby(["system", "type2"], observed=True)["pct"].sum()
        .reset_index().pivot(index="system", columns="type2", values="pct").fillna(0)
        .reindex(order)
    )
    plt.figure()
    bottom = None
    for col in wide.columns:
        plt.bar(wide.index, wide[col], label=col, bottom=bottom)
        bottom = (wide[col] if bottom is None else bottom + wide[col])
    plt.ylabel("Share of bytes by message type (%)")
    plt.xticks(range(len(wide.index)), wide.index)
    plt.title("What the bytes are spent on", loc="left")
    plt.legend(ncol=3, fontsize=8, frameon=False)
    plt.tight_layout()
    plt.savefig(outdir / "byte_mix_stacked.pdf")
    plt.close()


def main():
    style_paper()
    out = ensure_outdir()
    runs_dir = Path("runs")
    df, dm = load_runs(runs_dir)
    order = ["sendall", "certtalk", "greedyprobe", "respondermincut"]
    df["system"] = pd.Categorical(df["system"], categories=order, ordered=True)
    dm["system"] = pd.Categorical(dm["system"], categories=order, ordered=True)

    plot_bytes(df, out, order)
    plot_rounds(df, out, order)
    plot_scatter(df, out)
    if not dm.empty:
        plot_byte_mix(dm, out, order)


if __name__ == "__main__":
    main()
