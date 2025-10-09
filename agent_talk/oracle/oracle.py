"""Oracle that verifies certificates and computes ground truth."""
from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from agent_talk.core.coords import decode_cells_delta16, bytes_to_coords, decode_witness_bits
from agent_talk.core.crc16 import crc16_ccitt
from agent_talk.core.rle import decode_path_rle4, PathCodecError
from agent_talk.env.grid import Grid, bfs_free, neighbors
from .flow import Dinic, INF

Coordinate = Tuple[int, int]


class OracleError(RuntimeError):
    """Raised when certificates fail validation."""


def union_grid(grid_a: Grid, grid_b: Grid) -> Grid:
    return grid_a.union(grid_b)


def _decode_base64(data: str) -> bytes:
    try:
        return base64.b64decode(data, validate=True)
    except (ValueError, base64.binascii.Error) as exc:  # type: ignore[attr-defined]
        raise OracleError(f"invalid base64 payload: {exc}") from exc


def verify_path_cert(cert: Dict, union: Grid, start: Coordinate, goal: Coordinate) -> bool:
    encoding = cert.get("encoding", "RLE4_v1")
    # If s/t present, enforce match; otherwise rely on provided start/goal
    if "s" in cert and "t" in cert:
        if cert.get("s") != list(start) or cert.get("t") != list(goal):
            raise OracleError("start or goal mismatch")
    runs_bytes = _decode_base64(cert.get("runs", ""))
    expected_digest = int(cert.get("digest16"))
    if crc16_ccitt(runs_bytes) != expected_digest:
        raise OracleError("digest mismatch for path certificate")
    if encoding == "RLE4_v1":
        try:
            path = decode_path_rle4(start, runs_bytes)
        except PathCodecError as exc:
            raise OracleError(f"failed to decode path: {exc}") from exc
    elif encoding == "ABS16_v1":
        path = bytes_to_coords(runs_bytes)
        if not path or path[0] != start or path[-1] != goal:
            raise OracleError("absolute path endpoints incorrect")
        for a, b in zip(path, path[1:]):
            if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
                raise OracleError("absolute path not 4-connected")
    else:
        raise OracleError("unsupported path encoding")
    if not path or path[0] != start or path[-1] != goal:
        raise OracleError("path endpoints incorrect")
    for cell in path:
        x, y = cell
        if not (0 <= x < union.width and 0 <= y < union.height):
            raise OracleError("path leaves grid bounds")
        if union.is_blocked(cell):
            raise OracleError(f"path traverses blocked cell {cell}")
    return True


def verify_cut_cert(cert: Dict, union: Grid, start: Coordinate, goal: Coordinate) -> bool:
    encoding = cert.get("encoding", "DELTA16_v1")
    cells_bytes = _decode_base64(cert.get("cells", ""))
    expected_digest = int(cert.get("digest16"))
    if crc16_ccitt(cells_bytes) != expected_digest:
        raise OracleError("digest mismatch for cut certificate")
    if encoding == "DELTA16_v1":
        cells = decode_cells_delta16(cells_bytes)
    elif encoding == "ABS16_v1":
        cells = bytes_to_coords(cells_bytes)
    else:
        raise OracleError("unsupported cut encoding")
    if len(cells) != int(cert.get("k")):
        raise OracleError("cut length mismatch")
    witness_b64 = cert.get("witness")
    if witness_b64 is not None:
        witness_bytes = _decode_base64(witness_b64)
        witness_bits = decode_witness_bits(witness_bytes, len(cells))
        if len(witness_bits) != len(cells):
            raise OracleError("witness bit length mismatch")
    cut_set = set()
    for cell in cells:
        x, y = cell
        if not (0 <= x < union.width and 0 <= y < union.height):
            raise OracleError(f"cut cell out of bounds: {cell}")
        if not union.is_blocked(cell):
            raise OracleError(f"cut cell {cell} not blocked in union")
        cut_set.add(cell)
    if not cut_set:
        raise OracleError("cut set empty")
    if _connected_without_cut(union, start, goal, cut_set):
        raise OracleError("cut does not disconnect start and goal")
    return True


def _connected_without_cut(union: Grid, start: Coordinate, goal: Coordinate, cut: Iterable[Coordinate]) -> bool:
    """Return True if s and t remain connected when removing cut cells from potential grid."""
    cut_set = set(cut)
    if start in cut_set or goal in cut_set:
        return False
    queue: List[Coordinate] = [start]
    visited = {start}
    while queue:
        cell = queue.pop()
        if cell == goal:
            return True
        for nxt in neighbors(cell, union.height, union.width):
            if nxt in cut_set or nxt in visited:
                continue
            visited.add(nxt)
            queue.append(nxt)
    return False


def min_vertex_cut_potential(union: Grid, start: Coordinate, goal: Coordinate) -> List[Coordinate]:
    """Minimum vertex cut comprised of obstacle cells only."""
    node_count = union.height * union.width * 2
    dinic = Dinic(node_count)

    def node_index(cell: Coordinate) -> int:
        x, y = cell
        idx = y * union.width + x
        return idx * 2

    for y in range(union.height):
        for x in range(union.width):
            cell = (x, y)
            idx_in = node_index(cell)
            idx_out = idx_in + 1
            capacity = 1 if union.is_blocked(cell) else INF
            dinic.add_edge(idx_in, idx_out, capacity)
    for y in range(union.height):
        for x in range(union.width):
            cell = (x, y)
            idx_out = node_index(cell) + 1
            for nxt in neighbors(cell, union.height, union.width):
                idx_in = node_index(nxt)
                dinic.add_edge(idx_out, idx_in, INF)

    source = node_index(start) + 1  # s_out
    sink = node_index(goal)         # t_in
    dinic.max_flow(source, sink)
    reachable = dinic.min_cut_reachable(source)

    cut_cells: List[Coordinate] = []
    for y in range(union.height):
        for x in range(union.width):
            cell = (x, y)
            if not union.is_blocked(cell):
                continue
            idx_in = node_index(cell)
            idx_out = idx_in + 1
            if reachable[idx_in] and not reachable[idx_out]:
                cut_cells.append(cell)
    return cut_cells


@dataclass(slots=True)
class GroundTruth:
    reachable: bool
    shortest_length: Optional[int]
    min_cut_size: Optional[int]


def compute_ground_truth(grid_a: Grid, grid_b: Grid, start: Coordinate, goal: Coordinate) -> GroundTruth:
    union = union_grid(grid_a, grid_b)
    path = bfs_free(union, start, goal)
    if path is not None:
        return GroundTruth(reachable=True, shortest_length=len(path) - 1, min_cut_size=None)
    cut = min_vertex_cut_potential(union, start, goal)
    return GroundTruth(reachable=False, shortest_length=None, min_cut_size=len(cut))
