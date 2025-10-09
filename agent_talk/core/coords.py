"""Coordinate utilities and delta encoders."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Iterator, List, Sequence, Tuple
import struct

Coordinate = Tuple[int, int]

_ABS_SENTINEL = (-128, -128)


class CodecError(ValueError):
    """Raised when an encoding or decoding operation fails."""


def encode_cells_delta16(cells: Sequence[Coordinate]) -> bytes:
    """Encode a list of coordinates using the DELTA16_v1 format.

    The first coordinate is stored as absolute little-endian uint16 pairs.
    Subsequent coordinates store signed int8 deltas relative to the previous
    coordinate. When a delta exceeds the int8 range, a restart marker (-128,-128)
    is emitted followed by an absolute uint16 pair.
    """
    if not cells:
        return b""

    output = bytearray()
    prev = cells[0]
    output.extend(struct.pack("<HH", prev[0], prev[1]))

    for current in cells[1:]:
        dx = current[0] - prev[0]
        dy = current[1] - prev[1]
        if not -128 < dx < 128 or not -128 < dy < 128:
            output.extend(struct.pack("<bbHH", *_ABS_SENTINEL, current[0], current[1]))
        else:
            output.extend(struct.pack("<bb", dx, dy))
        prev = current
    return bytes(output)


def decode_cells_delta16(data: bytes) -> List[Coordinate]:
    """Inverse of :func:`encode_cells_delta16`."""
    if not data:
        return []
    if len(data) < 4:
        raise CodecError("delta16 payload too short")

    view = memoryview(data)
    offset = 0
    x0, y0 = struct.unpack_from("<HH", view, offset)
    offset += 4
    cells: List[Coordinate] = [(int(x0), int(y0))]
    prev = cells[-1]

    while offset < len(view):
        if offset + 2 > len(view):
            raise CodecError("dangling delta byte")
        dx, dy = struct.unpack_from("<bb", view, offset)
        offset += 2
        if (dx, dy) == _ABS_SENTINEL:
            if offset + 4 > len(view):
                raise CodecError("dangling absolute restart")
            x, y = struct.unpack_from("<HH", view, offset)
            offset += 4
            prev = (int(x), int(y))
            cells.append(prev)
            continue
        prev = (prev[0] + dx, prev[1] + dy)
        cells.append(prev)
    return cells


def coords_to_bytes(coords: Iterable[Coordinate]) -> bytes:
    """Helper to encode coordinates as raw little-endian uint16 pairs."""
    buf = bytearray()
    for (x, y) in coords:
        buf.extend(struct.pack("<HH", x, y))
    return bytes(buf)


def bytes_to_coords(data: bytes) -> List[Coordinate]:
    """Decode raw little-endian uint16 coordinate pairs."""
    if len(data) % 4 != 0:
        raise CodecError("coordinate byte length must be multiple of 4")
    result = []
    view = memoryview(data)
    for offset in range(0, len(data), 4):
        x, y = struct.unpack_from("<HH", view, offset)
        result.append((int(x), int(y)))
    return result


def encode_witness_bits(bits: Sequence[int]) -> bytes:
    """Pack a sequence of 0/1 witness bits into bytes (LSB-first)."""
    out = bytearray()
    byte = 0
    count = 0
    for bit in bits:
        if bit not in (0, 1):
            raise CodecError("witness bits must be 0 or 1")
        byte |= (bit & 1) << count
        count += 1
        if count == 8:
            out.append(byte)
            byte = 0
            count = 0
    if count:
        out.append(byte)
    return bytes(out)


def decode_witness_bits(data: bytes, length: int) -> List[int]:
    """Unpack witness bits into a list of length `length`."""
    bits: List[int] = []
    for byte in data:
        for i in range(8):
            bits.append((byte >> i) & 1)
            if len(bits) == length:
                return bits
    if len(bits) < length:
        raise CodecError("witness bit payload too short")
    return bits[:length]
