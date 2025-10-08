"""Instance cache IO helpers."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Sequence


@dataclass(slots=True)
class CacheEntry:
    seed: int
    height: int
    width: int
    mask_a: List[int]
    mask_b: List[int]
    start: tuple[int, int]
    goal: tuple[int, int]
    reachable: bool
    shortest: Optional[int]
    min_cut: Optional[int]
    split: str


def load_cache(path: Path) -> List[CacheEntry]:
    return list(iter_cache(path))


def iter_cache(path: Path) -> Iterator[CacheEntry]:
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            record = json.loads(line)
            yield CacheEntry(
                seed=int(record["seed"]),
                height=int(record["H"]),
                width=int(record["W"]),
                mask_a=[int(x) for x in record["A_mask"]],
                mask_b=[int(x) for x in record["B_mask"]],
                start=tuple(record["s"]),
                goal=tuple(record["t"]),
                reachable=bool(record["reachable_in_U"]),
                shortest=record.get("L_star"),
                min_cut=record.get("K_star"),
                split=record.get("split", "all"),
            )
