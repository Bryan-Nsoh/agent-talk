"""Instance cache generator."""
from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, Sequence

from agent_talk.env.grid import Grid
from agent_talk.oracle.oracle import compute_ground_truth


@dataclass(slots=True)
class Instance:
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

    def to_json(self) -> str:
        record = {
            "seed": self.seed,
            "H": self.height,
            "W": self.width,
            "A_mask": self.mask_a,
            "B_mask": self.mask_b,
            "s": list(self.start),
            "t": list(self.goal),
            "reachable_in_U": self.reachable,
        }
        if self.reachable:
            record["L_star"] = self.shortest
        else:
            record["K_star"] = self.min_cut
        record["split"] = self.split
        return json.dumps(record, separators=(",", ":"))


def sample_instance(
    seed: int,
    height: int,
    width: int,
    start: tuple[int, int],
    goal: tuple[int, int],
    density_range: tuple[float, float] = (0.15, 0.35),
) -> Instance:
    rng = random.Random(seed)
    for _ in range(512):
        p_a = rng.uniform(*density_range)
        p_b = rng.uniform(*density_range)
        mask_a = _sample_mask(rng, height, width, p_a, start, goal)
        mask_b = _sample_mask(rng, height, width, p_b, start, goal)

        grid_a = Grid.from_flat(height, width, mask_a)
        grid_b = Grid.from_flat(height, width, mask_b)
        union = grid_a.union(grid_b)
        if _isolated(union, start) or _isolated(union, goal):
            continue

        gt = compute_ground_truth(grid_a, grid_b, start, goal)
        instance = Instance(
            seed=seed,
            height=height,
            width=width,
            mask_a=mask_a,
            mask_b=mask_b,
            start=start,
            goal=goal,
            reachable=gt.reachable,
            shortest=gt.shortest_length,
            min_cut=gt.min_cut_size,
            split="all",
        )
        return instance
    raise RuntimeError("unable to sample non-isolated instance")


def _sample_mask(
    rng: random.Random,
    height: int,
    width: int,
    p: float,
    start: tuple[int, int],
    goal: tuple[int, int],
) -> List[int]:
    mask: List[int] = []
    for y in range(height):
        for x in range(width):
            if (x, y) == start or (x, y) == goal:
                mask.append(0)
                continue
            mask.append(1 if rng.random() < p else 0)
    return mask


def _isolated(union: Grid, cell: tuple[int, int]) -> bool:
    from agent_talk.env.grid import neighbors

    for nxt in neighbors(cell, union.height, union.width):
        if not union.is_blocked(nxt):
            return False
    return True


def generate_instances(base_seed: int, count: int, **kwargs) -> Iterator[Instance]:
    for offset in range(count):
        yield sample_instance(base_seed + offset, **kwargs)


def write_cache(path: Path, instances: Iterable[Instance]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for item in instances:
            fh.write(item.to_json())
            fh.write("\n")


def main(args: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Generate occupancy grid instance cache.")
    parser.add_argument("--out", type=Path, required=True, help="Output JSONL path.")
    parser.add_argument("--n", type=int, default=None, help="Total instances (single split).")
    parser.add_argument("--train", type=int, default=700)
    parser.add_argument("--dev", type=int, default=150)
    parser.add_argument("--test", type=int, default=150)
    parser.add_argument("--size", type=int, default=10, help="Grid size (square).")
    parser.add_argument("--seed", type=int, default=123, help="Base random seed.")
    parsed = parser.parse_args(args)

    height = width = parsed.size
    start = (0, 0)
    goal = (width - 1, height - 1)

    instances: List[Instance] = []
    if parsed.n is not None:
        for inst in generate_instances(parsed.seed, parsed.n, height=height, width=width, start=start, goal=goal):
            inst.split = "all"
            instances.append(inst)
    else:
        splits = {"train": parsed.train, "dev": parsed.dev, "test": parsed.test}
        cursor = parsed.seed
        for split, count in splits.items():
            for inst in generate_instances(cursor, count, height=height, width=width, start=start, goal=goal):
                inst.split = split
                instances.append(inst)
            cursor += count
    parsed.out.parent.mkdir(parents=True, exist_ok=True)
    write_cache(parsed.out, instances)


if __name__ == "__main__":
    main()
