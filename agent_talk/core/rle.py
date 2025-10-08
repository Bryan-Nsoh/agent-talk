"""RLE4 path codec."""
from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

Coordinate = Tuple[int, int]

_DIR_TO_CODE = {(0, -1): 0, (1, 0): 1, (0, 1): 2, (-1, 0): 3}
_CODE_TO_DIR = {v: k for k, v in _DIR_TO_CODE.items()}


class PathCodecError(ValueError):
    """Raised when encoding or decoding fails."""


def encode_path_rle4(path: Sequence[Coordinate]) -> bytes:
    """Encode a path as RLE4 (direction runs)."""
    if len(path) < 2:
        return b""
    runs = bytearray()
    prev = path[0]
    current_dir = None
    run_len = 0

    for point in path[1:]:
        dx = point[0] - prev[0]
        dy = point[1] - prev[1]
        if (dx, dy) not in _DIR_TO_CODE:
            raise PathCodecError(f"non-Manhattan step from {prev} to {point}")
        step_dir = _DIR_TO_CODE[(dx, dy)]
        if current_dir is None:
            current_dir = step_dir
            run_len = 1
        elif step_dir == current_dir and run_len < 63:
            run_len += 1
        else:
            runs.append((current_dir & 0b11) << 6 | (run_len & 0b111111))
            current_dir = step_dir
            run_len = 1
        prev = point
    if current_dir is not None:
        runs.append((current_dir & 0b11) << 6 | (run_len & 0b111111))
    return bytes(runs)


def decode_path_rle4(start: Coordinate, runs: bytes) -> List[Coordinate]:
    """Decode RLE4 bytes into a path starting at `start`."""
    path = [start]
    x, y = start
    for byte in runs:
        direction = (byte >> 6) & 0b11
        length = byte & 0b111111
        if length == 0:
            raise PathCodecError("zero-length run encountered")
        dx, dy = _CODE_TO_DIR.get(direction, (None, None))
        if dx is None:
            raise PathCodecError(f"invalid direction code {direction}")
        for _ in range(length):
            x += dx
            y += dy
            path.append((x, y))
    return path
