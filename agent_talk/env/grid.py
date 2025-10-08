"""Grid utilities for occupancy maps."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple

Coordinate = Tuple[int, int]


def neighbors(cell: Coordinate, height: int, width: int) -> Iterator[Coordinate]:
    """Yield 4-neighbour coordinates within bounds."""
    x, y = cell
    if y > 0:
        yield (x, y - 1)
    if x + 1 < width:
        yield (x + 1, y)
    if y + 1 < height:
        yield (x, y + 1)
    if x > 0:
        yield (x - 1, y)


@dataclass(slots=True)
class Grid:
    """Simple immutable view over a binary occupancy mask."""

    height: int
    width: int
    blocked: Tuple[Tuple[int, ...], ...]

    @classmethod
    def from_iterable(cls, data: Iterable[Iterable[int]]) -> "Grid":
        blocked_rows: List[Tuple[int, ...]] = []
        width: Optional[int] = None
        for row in data:
            row_tuple = tuple(1 if bool(v) else 0 for v in row)
            if width is None:
                width = len(row_tuple)
            elif len(row_tuple) != width:
                raise ValueError("inconsistent row widths in grid data")
            blocked_rows.append(row_tuple)
        if not blocked_rows:
            raise ValueError("grid cannot be empty")
        return cls(height=len(blocked_rows), width=width, blocked=tuple(blocked_rows))

    @classmethod
    def from_flat(cls, height: int, width: int, data: Sequence[int]) -> "Grid":
        if len(data) != height * width:
            raise ValueError("flat data length mismatch")
        rows = [
            tuple(1 if data[r * width + c] else 0 for c in range(width)) for r in range(height)
        ]
        return cls(height=height, width=width, blocked=tuple(rows))

    def is_blocked(self, cell: Coordinate) -> bool:
        x, y = cell
        return bool(self.blocked[y][x])

    def union(self, other: "Grid") -> "Grid":
        if self.height != other.height or self.width != other.width:
            raise ValueError("grid size mismatch")
        rows = []
        for y in range(self.height):
            rows.append(
                tuple(1 if self.blocked[y][x] or other.blocked[y][x] else 0 for x in range(self.width))
            )
        return Grid(height=self.height, width=self.width, blocked=tuple(rows))

    def iter_free(self) -> Iterator[Coordinate]:
        for y in range(self.height):
            for x in range(self.width):
                if not self.blocked[y][x]:
                    yield (x, y)


def bfs_free(occ: Grid, start: Coordinate, goal: Coordinate) -> Optional[List[Coordinate]]:
    """Breadth-first search over free cells."""
    if occ.is_blocked(start) or occ.is_blocked(goal):
        return None
    q: deque[Coordinate] = deque([start])
    parents: dict[Coordinate, Optional[Coordinate]] = {start: None}

    while q:
        current = q.popleft()
        if current == goal:
            return _reconstruct_path(parents, goal)
        for nxt in neighbors(current, occ.height, occ.width):
            if occ.is_blocked(nxt) or nxt in parents:
                continue
            parents[nxt] = current
            q.append(nxt)
    return None


def _reconstruct_path(parents: dict[Coordinate, Optional[Coordinate]], last: Coordinate) -> List[Coordinate]:
    path: List[Coordinate] = []
    node: Optional[Coordinate] = last
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()
    return path
