"""Aggregate metrics from batch evaluation logs."""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Dict, Iterable, List, Optional, Sequence


def load_records(paths: Sequence[Path]) -> List[Dict]:
    records: List[Dict] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                records.append(json.loads(line))
    return records


def summarise(records: Iterable[Dict]) -> List[Dict]:
    grouped: Dict[tuple[str, str], List[Dict]] = defaultdict(list)
    for record in records:
        key = (record["system"], record["split"])
        grouped[key].append(record)

    rows: List[Dict] = []
    for (system, split), items in grouped.items():
        n = len(items)
        successes = [r for r in items if r.get("outcome") == "DONE" and r.get("oracle_accepted")]
        success_rate = len(successes) / n if n else 0.0
        correctness = sum(1 for r in items if r.get("oracle_accepted")) / n if n else 0.0
        bytes_values = [r.get("bytes", 0) for r in items]
        rounds_values = [r.get("rounds", 0) for r in items]
        path_gaps = [r["path_gap"] for r in items if r.get("path_gap") is not None]
        cut_gaps = [r["cut_gap"] for r in items if r.get("cut_gap") is not None]
        interpretability = sum(
            1 for r in items if r.get("certificate_type") in {"PATH_CERT", "CUT_CERT"} and r.get("oracle_accepted")
        )
        rows.append(
            {
                "system": system,
                "split": split,
                "count": n,
                "success_rate": round(success_rate, 3),
                "correctness": round(correctness, 3),
                "bytes_median": median(bytes_values) if bytes_values else 0,
                "rounds_median": median(rounds_values) if rounds_values else 0,
                "path_gap_median": median(path_gaps) if path_gaps else None,
                "cut_gap_median": median(cut_gaps) if cut_gaps else None,
                "interpretability": round(interpretability / n, 3) if n else 0.0,
            }
        )
    return rows


def write_csv(rows: Iterable[Dict], path: Path) -> None:
    rows = list(rows)
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main(args: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Summarise evaluation logs.")
    parser.add_argument("--inputs", type=Path, nargs="+", required=True, help="Input JSONL files.")
    parser.add_argument("--out", type=Path, required=True, help="Output CSV path.")
    parsed = parser.parse_args(args)
    records = load_records(parsed.inputs)
    rows = summarise(records)
    parsed.out.parent.mkdir(parents=True, exist_ok=True)
    write_csv(rows, parsed.out)


if __name__ == "__main__":
    main()
