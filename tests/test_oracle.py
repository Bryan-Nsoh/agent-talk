from __future__ import annotations

import base64

from agent_talk.core.rle import encode_path_rle4
from agent_talk.core.coords import encode_cells_delta16, encode_witness_bits
from agent_talk.core.crc16 import crc16_ccitt
from agent_talk.env.grid import Grid
from agent_talk.oracle.oracle import verify_path_cert, verify_cut_cert, union_grid


def build_grid(mask):
    return Grid.from_flat(3, 3, mask)


def test_verify_path_cert():
    start = (0, 0)
    goal = (2, 0)
    mask = [0] * 9
    grid = build_grid(mask)
    union = union_grid(grid, grid)
    path = [start, (1, 0), goal]
    runs = encode_path_rle4(path)
    digest = crc16_ccitt(runs)
    payload = {
        "s": list(start),
        "t": list(goal),
        "encoding": "RLE4_v1",
        "runs": base64.b64encode(runs).decode("ascii"),
        "digest16": digest,
    }
    assert verify_path_cert(payload, union, start, goal)


def test_verify_cut_cert():
    start = (0, 0)
    goal = (2, 0)
    mask = [0, 1, 0,
            0, 1, 0,
            0, 1, 0]
    grid = build_grid(mask)
    union = union_grid(grid, grid)
    cells = [(1, 0), (1, 1), (1, 2)]
    encoded = encode_cells_delta16(cells)
    digest = crc16_ccitt(encoded)
    witness = encode_witness_bits([0] * len(cells))
    payload = {
        "encoding": "DELTA16_v1",
        "k": len(cells),
        "cells": base64.b64encode(encoded).decode("ascii"),
        "digest16": digest,
        "witness": base64.b64encode(witness).decode("ascii"),
    }
    assert verify_cut_cert(payload, union, start, goal)
