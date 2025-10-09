"""Base utilities for deterministic FSM agents."""
from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Set, Tuple

from agent_talk.core.crc16 import crc16_ccitt
from agent_talk.core.messages import Msg, make_message
from agent_talk.core.rle import encode_path_rle4
from agent_talk.core.coords import (
    encode_cells_delta16,
    coords_to_bytes,
    encode_witness_bits,
)
from agent_talk.env.grid import Grid, bfs_free
from agent_talk.oracle.oracle import min_vertex_cut_potential

Coordinate = Tuple[int, int]


@dataclass(slots=True)
class AgentConfig:
    name: str
    height: int
    width: int
    start: Coordinate
    goal: Coordinate
    private_mask: Sequence[int]
    max_path_attempts: int = 6
    max_path_length: int = 64
    allow_path: bool = True
    allow_cut: bool = True
    path_encoding: str = "RLE4_v1"
    cut_encoding: str = "DELTA16_v1"


WITNESS_MAP = {"A": 0, "B": 1}


class FiniteStateAgent:
    """Shared plumbing for both agents."""

    def __init__(self, config: AgentConfig) -> None:
        self.config = config
        self.seq = 0
        self.private_mask = list(config.private_mask)
        self.grid = Grid.from_flat(config.height, config.width, self.private_mask)

    def next_seq(self) -> int:
        val = self.seq
        self.seq += 1
        return val

    def make_message(self, msg_type: str, payload: dict) -> Msg:
        return make_message(msg_type, payload, self.next_seq())

    def grid_with_blocks(
        self,
        extra_blocks: Iterable[Coordinate],
        forced_free: Iterable[Coordinate] = (),
    ) -> Grid:
        mask = self.private_mask.copy()
        for x, y in extra_blocks:
            idx = y * self.config.width + x
            if 0 <= idx < len(mask):
                mask[idx] = 1
        for x, y in forced_free:
            idx = y * self.config.width + x
            if 0 <= idx < len(mask):
                if self.private_mask[idx] == 0:
                    mask[idx] = 0
        return Grid.from_flat(self.config.height, self.config.width, mask)

    def plan_path(
        self,
        extra_blocks: Iterable[Coordinate] = (),
        forced_free: Iterable[Coordinate] = (),
    ) -> List[Coordinate] | None:
        grid = self.grid_with_blocks(extra_blocks, forced_free)
        path = bfs_free(grid, self.config.start, self.config.goal)
        if path is not None and len(path) - 1 <= self.config.max_path_length:
            return path
        return None

    def encode_path(self, path: Sequence[Coordinate]) -> tuple[str, int]:
        if self.config.path_encoding == "RLE4_v1":
            payload = encode_path_rle4(path)
        elif self.config.path_encoding == "ABS16_v1":
            payload = coords_to_bytes(path)
        else:
            raise ValueError(f"unsupported path encoding {self.config.path_encoding}")
        digest = crc16_ccitt(payload)
        return base64.b64encode(payload).decode("ascii"), digest

    def min_cut(
        self,
        extra_blocks: Set[Coordinate],
        forced_free: Set[Coordinate],
    ) -> List[Coordinate]:
        union_grid = self.grid_with_blocks(extra_blocks, forced_free)
        return min_vertex_cut_potential(union_grid, self.config.start, self.config.goal)

    def encode_cut(
        self,
        cells: Sequence[Coordinate],
        peer_blocks: Set[Coordinate],
    ) -> tuple[str, int, str]:
        if self.config.cut_encoding == "DELTA16_v1":
            payload = encode_cells_delta16(list(cells))
        elif self.config.cut_encoding == "ABS16_v1":
            payload = coords_to_bytes(cells)
        else:
            raise ValueError(f"unsupported cut encoding {self.config.cut_encoding}")
        digest = crc16_ccitt(payload)
        witness_bits = []
        sender_bit = WITNESS_MAP.get(self.config.name, 0)
        peer_bit = WITNESS_MAP.get("B" if self.config.name == "A" else "A", 1)
        for x, y in cells:
            idx = y * self.config.width + x
            if 0 <= idx < len(self.private_mask) and self.private_mask[idx]:
                witness_bits.append(sender_bit)
            elif (x, y) in peer_blocks:
                witness_bits.append(peer_bit)
            else:
                witness_bits.append(sender_bit)
        witness_bytes = encode_witness_bits(witness_bits)
        return (
            base64.b64encode(payload).decode("ascii"),
            digest,
            base64.b64encode(witness_bytes).decode("ascii"),
        )
