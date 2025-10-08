"""Simple plotting utilities (optional)."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence

try:
    import matplotlib.pyplot as plt
except ImportError:  # pragma: no cover - optional dependency
    plt = None


def load_records(path: Path) -> List[Dict]:
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def plot_bytes(records: List[Dict], outdir: Path) -> None:
    if plt is None:
        raise RuntimeError("matplotlib not installed; install via `uv pip install .[analysis]`")
    grouped = defaultdict(list)
    for rec in records:
        grouped[(rec["system"], rec["split"])].append(rec["bytes"])

    outdir.mkdir(parents=True, exist_ok=True)
    for (system, split), values in grouped.items():
        fig, ax = plt.subplots()
        ax.hist(values, bins=20)
        ax.set_title(f"bytes distribution: {system} ({split})")
        ax.set_xlabel("bytes")
        ax.set_ylabel("count")
        fig.tight_layout()
        fig.savefig(outdir / f"bytes_{system}_{split}.png")
        plt.close(fig)


def main(args: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Plot basic histograms from evaluation logs.")
    parser.add_argument("--input", type=Path, required=True, help="Input JSONL log.")
    parser.add_argument("--outdir", type=Path, required=True, help="Directory for plots.")
    parsed = parser.parse_args(args)
    records = load_records(parsed.input)
    plot_bytes(records, parsed.outdir)


if __name__ == "__main__":
    main()
