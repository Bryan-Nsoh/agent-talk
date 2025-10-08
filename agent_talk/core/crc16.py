"""CRC16 utilities using the CCITT-FALSE polynomial."""
from __future__ import annotations

from typing import Iterable

_POLY = 0x1021
_INIT = 0xFFFF


def crc16_ccitt(data: bytes, seed: int = _INIT) -> int:
    """Return the CRC16-CCITT checksum for the provided bytes."""
    crc = seed & 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ _POLY
            else:
                crc <<= 1
            crc &= 0xFFFF
    return crc


def crc16_for_fields(*parts: Iterable[int | bytes | bytearray | str]) -> int:
    """Compute CRC16 over multiple heterogeneous parts."""
    crc = _INIT
    for part in parts:
        if isinstance(part, int):
            chunk = part.to_bytes(4, "little", signed=False)
        elif isinstance(part, str):
            chunk = part.encode("utf-8")
        else:
            chunk = bytes(part)
        crc = crc16_ccitt(chunk, crc)
    return crc
