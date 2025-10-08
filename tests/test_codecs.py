from __future__ import annotations

import base64
import random

from agent_talk.core import (
    encode_path_rle4,
    decode_path_rle4,
    encode_cells_delta16,
    decode_cells_delta16,
    coords_to_bytes,
    bytes_to_coords,
)


def random_path(length: int, start: tuple[int, int] = (0, 0)) -> list[tuple[int, int]]:
    x, y = start
    path = [start]
    for _ in range(length):
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        x += dx
        y += dy
        path.append((x, y))
    return path


def test_rle_round_trip():
    rng = random.Random(123)
    for _ in range(10):
        length = rng.randint(1, 20)
        path = random_path(length)
        encoded = encode_path_rle4(path)
        decoded = decode_path_rle4(path[0], encoded)
        assert decoded == path


def test_delta_round_trip():
    points = [(0, 0), (1, 0), (3, 1), (10, 2), (9, 7)]
    encoded = encode_cells_delta16(points)
    decoded = decode_cells_delta16(encoded)
    assert decoded == points


def test_absolute_coords_round_trip():
    coords = [(i, i * 2) for i in range(10)]
    blob = coords_to_bytes(coords)
    decoded = bytes_to_coords(blob)
    assert decoded == coords
