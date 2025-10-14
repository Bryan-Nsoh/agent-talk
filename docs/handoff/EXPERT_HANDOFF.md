Last updated: 2025-10-09T20:10Z (UTC)

## Summary (raw)
```text
system,split,count,success_rate,correctness,bytes_median,rounds_median,path_gap_median,cut_gap_median,interpretability
certtalk,all,1000,1.0,1.0,468.5,5.0,0.0,0.0,1.0
sendall,all,1000,1.0,1.0,364.0,3.0,0.0,0.0,1.0
greedyprobe,all,1000,1.0,1.0,468.5,5.0,0.0,0.0,1.0
respondermincut,all,1000,0.205,0.205,506.0,6.0,,0,0.205
```


## Dataset sample (raw)
```json
{"seed":123,"H":10,"W":10,"A_mask":[0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,1,0,1,0,0,0,0,0,0],"B_mask":[0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],"s":[0,0],"t":[9,9],"reachable_in_U":false,"K_star":4,"split":"all"}
{"seed":124,"H":10,"W":10,"A_mask":[0,1,0,0,0,1,1,0,0,1,0,0,1,1,1,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,0,0,1,1,0,0,1,0,1,1,1,1,0,0,0,1,1,0,0,0,0,1,1,1,0,1,0,0],"B_mask":[0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,1,1,1,0,1,0,0],"s":[0,0],"t":[9,9],"reachable_in_U":false,"K_star":3,"split":"all"}
{"seed":125,"H":10,"W":10,"A_mask":[0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0],"B_mask":[0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],"s":[0,0],"t":[9,9],"reachable_in_U":false,"K_star":5,"split":"all"}
```


## Representative transcripts/logs (raw)
```text
{"system":"certtalk","split":"all","seed":123,"outcome":"DONE","bytes":276,"rounds":3,"certificate_type":"CUT_CERT","oracle_accepted":true,"path_gap":null,"cut_gap":0,"reason":null,"ablation":null,"transcript":[{"sender":"A","message":"{\"c\":10141,\"p\":{\"cs\":\"AAACAAEAAf4AAQ==\",\"d\":46585,\"k\":4,\"w\":\"AA==\"},\"q\":0,\"s\":\"v1\",\"t\":\"CUT_PROPOSE\"}","bytes":101},{"sender":"B","message":"{\"c\":4584,\"p\":{\"cs\":\"AAACAAEAAf4AAQ==\",\"d\":46585,\"k\":4,\"sb\":[\"B\"],\"w\":\"AA==\"},\"q\":0,\"s\":\"v1\",\"t\":\"CUT_CERT\"}","bytes":108},{"sender":"A","message":"{\"c\":36481,\"p\":{\"a\":\"CUT_CERT\",\"d\":46585},\"q\":1,\"s\":\"v1\",\"t\":\"ACK\"}","bytes":67,"terminal":true}],"diagnostics":{"a_belief_blocks":0,"a_belief_free":0,"a_failed_path_digests":0,"a_failed_cut_digests":0,"b_peer_blocks_from_a":4}}
```

```text
{"system":"certtalk","split":"all","seed":126,"outcome":"DONE","bytes":1013,"rounds":11,"certificate_type":"CUT_CERT","oracle_accepted":true,"path_gap":null,"cut_gap":0,"reason":null,"ablation":null,"transcript":[{"sender":"A","message":"{\"c\":19235,\"p\":{\"d\":55788,\"r\":\"RIFDgUGGQYE=\"},\"q\":0,\"s\":\"v1\",\"t\":\"PATH_PROPOSE\"}","bytes":80},{"sender":"B","message":"{\"c\":28346,\"p\":{\"mask\":\"GBAA\",\"n\":\"PATH_PROPOSE\",\"reason\":\"BLOCKED\"},\"q\":0,\"s\":\"v1\",\"t\":\"NACK\"}","bytes":95},{"sender":"A","message":"{\"c\":22500,\"p\":{\"d\":7265,\"r\":\"QoFFhEGDQYE=\"},\"q\":1,\"s\":\"v1\",\"t\":\"PATH_PROPOSE\"}","bytes":79},{"sender":"B","message":"{\"c\":39901,\"p\":{\"mask\":\"AAQA\",\"n\":\"PATH_PROPOSE\",\"reason\":\"BLOCKED\"},\"q\":1,\"s\":\"v1\",\"t\":\"NACK\"}","bytes":95},{"sender":"A","message":"{\"c\":59809,\"p\":{\"d\":18065,\"r\":\"QoRFgUGDQYE=\"},\"q\":2,\"s\":\"v1\",\"t\":\"PATH_PROPOSE\"}","bytes":80},{"sender":"B","message":"{\"c\":12669,\"p\":{\"mask\":\"UAEA\",\"n\":\"PATH_PROPOSE\",\"reason\":\"BLOCKED\"},\"q\":2,\"s\":\"v1\",\"t\":\"NACK\"}","bytes":95},{"sender":"A","message":"{\"c\":57787,\"p\":{\"d\":9624,\"r\":\"g0GCQYFBgUWBQYE=\"},\"q\":3,\"s\":\"v1\",\"t\":\"PATH_PROPOSE\"}","bytes":83},{"sender":"B","message":"{\"c\":51842,\"p\":{\"mask\":\"VgIA\",\"n\":\"PATH_PROPOSE\",\"reason\":\"BLOCKED\"},\"q\":3,\"s\":\"v1\",\"t\":\"NACK\"}","bytes":95},{"sender":"A","message":"{\"c\":40618,\"p\":{\"cs\":\"AAABAAEBAQABAQH/AQEB/wEBAQEB/w==\",\"d\":33788,\"k\":10,\"w\":\"hQE=\"},\"q\":4,\"s\":\"v1\",\"t\":\"CUT_PROPOSE\"}","bytes":118},{"sender":"B","message":"{\"c\":65004,\"p\":{\"cs\":\"AAABAAEBAQABAQH/AQEB/wEBAQEB/w==\",\"d\":33788,\"k\":10,\"sb\":[\"B\"],\"w\":\"hQE=\"},\"q\":4,\"s\":\"v1\",\"t\":\"CUT_CERT\"}","bytes":126},{"sender":"A","message":"{\"c\":65187,\"p\":{\"a\":\"CUT_CERT\",\"d\":33788},\"q\":5,\"s\":\"v1\",\"t\":\"ACK\"}","bytes":67,"terminal":true}],"diagnostics":{"a_belief_blocks":12,"a_belief_free":33,"a_failed_path_digests":4,"a_failed_cut_digests":0,"b_peer_blocks_from_a":6}}
```

```text
{"system":"respondermincut","split":"all","seed":131,"outcome":"DONE","bytes":558,"rounds":6,"certificate_type":"CUT_CERT","oracle_accepted":true,"path_gap":null,"cut_gap":1,"reason":null,"ablation":null,"transcript":[{"sender":"A","message":"{\"c\":64959,\"p\":{\"cut_enc\":\"DELTA16_v1\",\"path_enc\":\"RLE4_v1\",\"s\":[0,0],\"size\":[10,10],\"t\":[9,9]},\"q\":0,\"s\":\"v1\",\"t\":\"SCHEMA\"}","bytes":124},{"sender":"B","message":"{\"c\":24093,\"p\":{\"cs\":\"CQAEAP8B/gEBAP4BAQEBAQ==\",\"d\":48350,\"k\":7,\"sb\":[\"B\"],\"w\":\"fw==\"},\"q\":0,\"s\":\"v1\",\"t\":\"CUT_CERT\"}","bytes":117},{"sender":"A","message":"{\"c\":11739,\"p\":{\"n\":\"CUT_PROPOSE\",\"reason\":\"BLOCKED\",\"x\":[[9,4],[8,5],[6,6],[7,6],[5,7],[6,8],[7,9]]},\"q\":1,\"s\":\"v1\",\"t\":\"NACK\"}","bytes":128},{"sender":"B","message":"{\"c\":8151,\"p\":{\"cs\":[[9,4],[8,5],[6,6],[7,6],[5,7],[6,8]],\"wht\":\"CELLS\"},\"q\":1,\"s\":\"v1\",\"t\":\"PROBE\"}","bytes":100},{"sender":"A","message":"{\"c\":26486,\"p\":{},\"q\":2,\"s\":\"v1\",\"t\":\"HELLO\"}","bytes":45},{"sender":"B","message":"{\"c\":22322,\"p\":{},\"q\":2,\"s\":\"v1\",\"t\":\"DONE\"}","bytes":44}],"diagnostics":{}}
```


## Reproduction commands (raw)
```
uv venv && source .venv/bin/activate && uv pip install -e .[dev]
uv run python -m agent_talk.env.generator --out data/20251008T151417Z_cache.jsonl --n 1000 --size 10 --seed 123
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system certtalk --out runs/20251009T201009Z_certtalk.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system sendall --out runs/20251009T201024Z_sendall.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system greedyprobe --out runs/20251009T201034Z_greedyprobe.jsonl
uv run python -m agent_talk.runners.batch_eval --cache data/20251008T151417Z_cache.jsonl --system respondermincut --out runs/20251009T201043Z_respondmincut.jsonl
uv run python -m agent_talk.analysis.metrics --inputs runs/20251009T201009Z_certtalk.jsonl runs/20251009T201024Z_sendall.jsonl runs/20251009T201034Z_greedyprobe.jsonl runs/20251009T201043Z_respondmincut.jsonl --out runs/20251009T201059Z_summary.csv
```

## Code (verbatim, raw)
```python
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
```

```python
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
```

```python
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
```

```python
"""Typed message helpers."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, Literal

from .crc16 import crc16_for_fields

# Optional compact schema toggle (short keys to trim bytes)
COMPACT_SCHEMA: bool = False

TOP_MAP = {"type": "t", "payload": "p", "schema": "s", "seq": "q", "crc16": "c"}
REV_TOP_MAP = {v: k for k, v in TOP_MAP.items()}

PAYLOAD_MAP = {
    "encoding": "e",
    "digest16": "d",
    "witness": "w",
    "signed_by": "sb",
    "ack_of": "a",
    "nack_of": "n",
    "conflicts": "x",
    "cells": "cs",
    "runs": "r",
    "blocked": "b",
    "what": "wht",
}
REV_PAYLOAD_MAP = {v: k for k, v in PAYLOAD_MAP.items()}


def set_compact_schema(flag: bool) -> None:
    global COMPACT_SCHEMA
    COMPACT_SCHEMA = bool(flag)

SchemaLiteral = Literal["v1"]


class MessageError(ValueError):
    """Raised for malformed messages."""


def _canonical_payload_bytes(payload: Dict[str, Any]) -> bytes:
    try:
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise MessageError(f"payload not JSON-serialisable: {exc}") from exc


@dataclass(slots=True)
class Msg:
    """Structured message with CRC validation."""

    type: str
    payload: Dict[str, Any]
    schema: SchemaLiteral = "v1"
    seq: int = 0
    crc16: int = field(init=False)

    def __post_init__(self) -> None:
        if not isinstance(self.payload, dict):
            raise MessageError("payload must be a dict")
        if self.schema != "v1":
            raise MessageError(f"unsupported schema {self.schema}")
        if self.seq < 0:
            raise MessageError("seq must be non-negative")
        self.crc16 = self.compute_crc()

    def compute_crc(self) -> int:
        payload_bytes = _canonical_payload_bytes(self.payload)
        return crc16_for_fields(self.type, payload_bytes)

    def to_json(self) -> str:
        if not COMPACT_SCHEMA:
            out = {
                "type": self.type,
                "payload": self.payload,
                "schema": self.schema,
                "seq": self.seq,
                "crc16": self.crc16,
            }
            return json.dumps(out, separators=(",", ":"), sort_keys=True)
        # Compact top-level and payload keys
        compact_payload = {
            (PAYLOAD_MAP.get(k, k)): v for k, v in self.payload.items()
        }
        out = {
            TOP_MAP["type"]: self.type,
            TOP_MAP["payload"]: compact_payload,
            TOP_MAP["schema"]: self.schema,
            TOP_MAP["seq"]: self.seq,
            TOP_MAP["crc16"]: self.crc16,
        }
        return json.dumps(out, separators=(",", ":"), sort_keys=True)

    @staticmethod
    def from_json(data: str) -> "Msg":
        try:
            raw = json.loads(data)
        except json.JSONDecodeError as exc:
            raise MessageError(f"invalid JSON: {exc}") from exc
        # Support both standard and compact forms
        if "type" not in raw and "t" in raw:
            # Expand compact
            payload = raw.get("p", {})
            expanded_payload = {REV_PAYLOAD_MAP.get(k, k): v for k, v in payload.items()}
            raw = {
                "type": raw.get("t"),
                "payload": expanded_payload,
                "schema": raw.get("s"),
                "seq": raw.get("q"),
                "crc16": raw.get("c"),
            }
        required = {"type", "payload", "schema", "seq", "crc16"}
        if not required.issubset(raw):
            missing = required - raw.keys()
            raise MessageError(f"missing fields {missing}")
        msg = Msg(type=raw["type"], payload=raw["payload"], schema=raw["schema"], seq=raw["seq"])
        if msg.crc16 != raw["crc16"]:
            raise MessageError("CRC16 mismatch")
        return msg


def make_message(msg_type: str, payload: Dict[str, Any], seq: int) -> Msg:
    """Convenience wrapper to construct a validated message."""
    return Msg(type=msg_type, payload=payload, seq=seq)
```

```python
"""Protocol helpers: message validation, limits, transcript entries."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Literal, Optional

from .messages import Msg, MessageError, make_message

MessageType = Literal[
    "HELLO",
    "SCHEMA",
    "PROBE",
    "PROBE_REPLY",
    "YIELD",
    "PATH_PROPOSE",
    "PATH_CERT",
    "CUT_PROPOSE",
    "CUT_CERT",
    "ACK",
    "NACK",
    "DONE",
]


@dataclass(slots=True)
class ConversationLimits:
    """Limits enforced during a conversation."""

    max_rounds: int = 64
    max_bytes_per_message: int = 256
    max_total_bytes: int = 3 * 1024


@dataclass(slots=True)
class TranscriptEntry:
    """Record of a single turn."""

    sender: str
    message: Msg
    raw: str
    bytes_used: int


class ProtocolError(RuntimeError):
    """Raised when protocol invariants are violated."""


def encode_message(msg: Msg) -> str:
    """Return the canonical JSON string for the message."""
    return msg.to_json()


def enforce_message_size(raw: str, limits: ConversationLimits) -> int:
    """Ensure `raw` is under per-message and cumulative caps."""
    size = len(raw.encode("utf-8"))
    if size > limits.max_bytes_per_message:
        raise ProtocolError(f"message exceeds {limits.max_bytes_per_message} bytes (got {size})")
    return size


def build_message(msg_type: MessageType, payload: Dict, seq: int, limits: ConversationLimits) -> TranscriptEntry:
    """Construct a message and ensure it satisfies size limits."""
    msg = make_message(msg_type, payload, seq)
    raw = encode_message(msg)
    size = enforce_message_size(raw, limits)
    return TranscriptEntry(sender="", message=msg, raw=raw, bytes_used=size)


def validate_incoming_message(
    msg_json: str,
    prev_seq: int,
    limits: ConversationLimits,
) -> Msg:
    """Validate an incoming message string."""
    msg = Msg.from_json(msg_json)
    enforce_message_size(msg_json, limits)
    if msg.seq <= prev_seq:
        raise ProtocolError(f"sequence must increase (prev {prev_seq}, got {msg.seq})")
    return msg


def accumulate_bytes(total_so_far: int, entry: TranscriptEntry, limits: ConversationLimits) -> int:
    """Ensure cumulative byte budget is not exceeded."""
    total = total_so_far + entry.bytes_used
    if total > limits.max_total_bytes:
        raise ProtocolError(f"conversation exceeded total byte limit {limits.max_total_bytes}")
    return total
```

```python
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
```

```python
"""Dinic max-flow implementation tailored for vertex cuts."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Callable, List, Optional


INF = 10**9


@dataclass(slots=True)
class Edge:
    to: int
    rev: int
    cap: int


class Dinic:
    """Lightweight Dinic max-flow."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.graph: List[List[Edge]] = [[] for _ in range(n)]

    def add_edge(self, u: int, v: int, cap: int) -> None:
        forward = Edge(to=v, rev=len(self.graph[v]), cap=cap)
        backward = Edge(to=u, rev=len(self.graph[u]), cap=0)
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def max_flow(self, source: int, sink: int) -> int:
        flow = 0
        level = [-1] * self.n
        while self._bfs(source, sink, level):
            it = [0] * self.n
            while True:
                pushed = self._dfs(source, sink, INF, level, it)
                if pushed == 0:
                    break
                flow += pushed
        return flow

    def min_cut_reachable(self, source: int) -> List[bool]:
        """Return nodes reachable in the residual graph from source."""
        visited = [False] * self.n
        q: deque[int] = deque([source])
        visited[source] = True
        while q:
            u = q.popleft()
            for edge in self.graph[u]:
                if edge.cap > 0 and not visited[edge.to]:
                    visited[edge.to] = True
                    q.append(edge.to)
        return visited

    def _bfs(self, source: int, sink: int, level: List[int]) -> bool:
        for i in range(self.n):
            level[i] = -1
        q: deque[int] = deque([source])
        level[source] = 0
        while q:
            u = q.popleft()
            for edge in self.graph[u]:
                if edge.cap > 0 and level[edge.to] < 0:
                    level[edge.to] = level[u] + 1
                    q.append(edge.to)
        return level[sink] >= 0

    def _dfs(self, u: int, sink: int, f: int, level: List[int], it: List[int]) -> int:
        if u == sink:
            return f
        for i in range(it[u], len(self.graph[u])):
            it[u] = i
            edge = self.graph[u][i]
            if edge.cap <= 0 or level[u] >= level[edge.to]:
                continue
            d = self._dfs(edge.to, sink, min(f, edge.cap), level, it)
            if d > 0:
                edge.cap -= d
                rev_edge = self.graph[edge.to][edge.rev]
                rev_edge.cap += d
                return d
        return 0
```

```python
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
```

```python
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
```

```python
"""Initiator agent A."""
from __future__ import annotations

import base64
from typing import Dict, List, Optional, Sequence, Set, Tuple

from agent_talk.core.coords import decode_witness_bits
from agent_talk.core.messages import Msg
from agent_talk.agents.fsm_base import AgentConfig, FiniteStateAgent

Coordinate = Tuple[int, int]


class AgentA(FiniteStateAgent):
    """Finite state initiator that favours paths before cuts."""

    PROBE_LIMIT = 6
    HALO_TTL = 2
    NACK_YIELD_THRESHOLD = 1_000_000

    def __init__(self, config: AgentConfig) -> None:
        super().__init__(config)
        self.state = "PLAN_PATH" if self.config.allow_path else "PLAN_CUT"
        self.belief_peer_blocks: Set[Coordinate] = set()
        self.belief_peer_free: Set[Coordinate] = set()
        self.path_attempts = 0
        self.cut_attempts = 0
        self.current_path: Optional[List[Coordinate]] = None
        self.current_path_digest: Optional[int] = None
        self.current_path_runs: Optional[str] = None
        self.current_cut: Optional[List[Coordinate]] = None
        self.current_cut_digest: Optional[int] = None
        self.current_cut_cells: Optional[str] = None
        self.current_cut_witness: Optional[str] = None
        self.failed_path_digests: Set[int] = set()
        self.failed_cut_digests: Set[int] = set()
        self.halo_blocks: Dict[Coordinate, int] = {}
        self.pending_probe: Optional[List[Coordinate]] = None
        self.awaiting_probe_reply = False
        self.probe_used = False
        self.total_nacks = 0
        self.yield_sent = False
        self.follow_mode = False
        self.pending_reply: Optional[Tuple[str, dict]] = None
        self.peer_path_digest: Optional[int] = None
        self.peer_cut_digest: Optional[int] = None

    def step(self, incoming: Optional[Msg]) -> Msg:
        if incoming is not None:
            self._handle_incoming(incoming)
        return self._next_message()

    def _handle_incoming(self, message: Msg) -> None:
        if message.type == "NACK":
            self.total_nacks += 1
        elif message.type == "ACK" and message.payload.get("ack_of") != "PROBE":
            self.total_nacks = 0

        if message.type == "PROBE_REPLY" and self.awaiting_probe_reply:
            self._handle_probe_reply(message)
            return
        # Fast-path receptions: respond with ACK to certificate and finish
        if self.state in {"AWAIT_PATH_RESPONSE", "PLAN_PATH"} and message.type == "PATH_CERT":
            digest = int(message.payload.get("digest16", 0))
            self.pending_reply = ("ACK", {"ack_of": "PATH_CERT", "digest16": digest})
            self.state = "SEND_REPLY"
            return
        if self.state in {"AWAIT_CUT_RESPONSE", "PLAN_CUT"} and message.type == "CUT_CERT":
            digest = int(message.payload.get("digest16", 0))
            self.pending_reply = ("ACK", {"ack_of": "CUT_CERT", "digest16": digest})
            self.state = "SEND_REPLY"
            return

        if self.state == "AWAIT_PATH_RESPONSE":
            if message.type == "ACK" and message.payload.get("ack_of") == "PATH_PROPOSE":
                if int(message.payload.get("digest16")) == self.current_path_digest:
                    self.path_attempts = 0
                    self.probe_used = False
                    self.state = "PREPARE_PATH_CERT"
                else:
                    self.state = "PLAN_PATH"
            elif message.type == "NACK" and message.payload.get("nack_of") == "PATH_PROPOSE":
                mask_b64 = message.payload.get("mask")
                conflicts = []
                if mask_b64 and self.current_path:
                    try:
                        bits = decode_witness_bits(base64.b64decode(mask_b64, validate=True), len(self.current_path))
                    except Exception:
                        bits = []
                    for cell, bit in zip(self.current_path, bits):
                        if bit:
                            self.belief_peer_blocks.add(cell)
                        else:
                            self.belief_peer_free.add(cell)
                else:
                    conflicts = message.payload.get("conflicts") or []
                    self._ingest_conflicts(conflicts, mode="PATH")
                self._update_halo(conflicts)
                if self.current_path_digest is not None:
                    self.failed_path_digests.add(self.current_path_digest)
                self.path_attempts += 1
                if self.path_attempts >= self.config.max_path_attempts or not self.config.allow_path:
                    self.state = "PLAN_CUT"
                else:
                    self.state = "PLAN_PATH"
                if not self.yield_sent and self.total_nacks >= self.NACK_YIELD_THRESHOLD:
                    self.pending_probe = None
                    self.awaiting_probe_reply = False
                    self.state = "SEND_YIELD"
                    self.yield_sent = True
                    return
            else:
                self.state = "PLAN_PATH"
        elif self.state == "AWAIT_PATH_CERT_ACK":
            if message.type == "ACK" and message.payload.get("ack_of") == "PATH_CERT":
                if int(message.payload.get("digest16")) == self.current_path_digest:
                    self.state = "READY_DONE"
                else:
                    self.state = "PLAN_PATH"
        elif self.state == "AWAIT_CUT_RESPONSE":
            if message.type == "ACK" and message.payload.get("ack_of") == "CUT_PROPOSE":
                if int(message.payload.get("digest16")) == self.current_cut_digest:
                    self.cut_attempts = 0
                    self.probe_used = False
                    self.state = "PREPARE_CUT_CERT"
                else:
                    self.state = "PLAN_CUT"
            elif message.type == "NACK" and message.payload.get("nack_of") == "CUT_PROPOSE":
                conflicts = message.payload.get("conflicts") or []
                self._ingest_conflicts(conflicts, mode="CUT")
                if self.current_cut_digest is not None:
                    self.failed_cut_digests.add(self.current_cut_digest)
                if not self.probe_used:
                    probe_cells = self._select_probe_cells(conflicts)
                    if probe_cells:
                        self.pending_probe = probe_cells
                        self.probe_used = True
                        self.state = "SEND_PROBE"
                        return
                self.state = "PLAN_CUT"
                if not self.yield_sent and self.total_nacks >= self.NACK_YIELD_THRESHOLD:
                    self.pending_probe = None
                    self.awaiting_probe_reply = False
                    self.state = "SEND_YIELD"
                    self.yield_sent = True
                    return
        elif self.state == "AWAIT_CUT_CERT_ACK":
            if message.type == "ACK" and message.payload.get("ack_of") == "CUT_CERT":
                if int(message.payload.get("digest16")) == self.current_cut_digest:
                    self.state = "READY_DONE"
                else:
                    self.state = "PLAN_CUT"
        elif self.state == "AWAIT_YIELD_ACK":
            if message.type == "ACK" and message.payload.get("ack_of") == "YIELD":
                self.follow_mode = True
                self.state = "FOLLOW"
            else:
                self.state = "PLAN_CUT"
        elif self.state == "FOLLOW":
            self._handle_follow_message(message)
        elif self.state == "READY_DONE":
            pass

    def _next_message(self) -> Msg:
        while True:
            if self.state == "SEND_PROBE" and self.pending_probe:
                cells_payload = [list(cell) for cell in self.pending_probe]
                self.awaiting_probe_reply = True
                self.state = "AWAIT_PROBE_REPLY"
                msg = self.make_message("PROBE", {"what": "CELLS", "cells": cells_payload})
                self.pending_probe = None
                return msg

            if self.state == "AWAIT_PROBE_REPLY":
                raise RuntimeError("Agent A awaiting probe reply")

            if self.state == "SEND_YIELD":
                self.state = "AWAIT_YIELD_ACK"
                return self.make_message("YIELD", {})

            if self.state == "SEND_REPLY" and self.pending_reply is not None:
                msg_type, payload = self.pending_reply
                self.pending_reply = None
                self.state = "FOLLOW"
                return self.make_message(msg_type, payload)

            if self.state == "PLAN_PATH":
                if not self.config.allow_path:
                    self.state = "PLAN_CUT"
                    continue
                self._decay_halo()
                extra_blocks = set(self.belief_peer_blocks) | self._halo_set()
                path = self.plan_path(extra_blocks, self.belief_peer_free)
                if path is None:
                    self.state = "PLAN_CUT"
                    continue
                runs_b64, digest = self.encode_path(path)
                if digest in self.failed_path_digests and self.config.allow_cut:
                    self.state = "PLAN_CUT"
                    continue
                payload = {"runs": runs_b64, "digest16": digest}
                self.current_path = path
                self.current_path_digest = digest
                self.current_path_runs = runs_b64
                self.cut_attempts = 0
                self.state = "AWAIT_PATH_RESPONSE"
                return self.make_message("PATH_PROPOSE", payload)

            if self.state == "PREPARE_PATH_CERT":
                payload = {"runs": self.current_path_runs or "", "digest16": self.current_path_digest, "signed_by": ["A", "B"]}
                self.state = "AWAIT_PATH_CERT_ACK"
                return self.make_message("PATH_CERT", payload)

            if self.state == "PLAN_CUT":
                if self.config.allow_path and self.cut_attempts >= max(self.config.max_path_attempts, 1):
                    self.state = "PLAN_PATH"
                    continue
                if not self.config.allow_cut:
                    self.state = "DONE"
                    return self.make_message("DONE", {"reason": "CUT_FORBIDDEN"})
                cut = self._plan_cut()
                if not cut:
                    if self.config.allow_path:
                        self.path_attempts = 0
                        self.state = "PLAN_PATH"
                        continue
                    self.state = "DONE"
                    return self.make_message("DONE", {"reason": "FAILED_TO_FIND_CERT"})
                cells_b64, digest, witness_b64 = self.encode_cut(cut, self.belief_peer_blocks)
                if digest in self.failed_cut_digests and self.config.allow_path:
                    self.state = "PLAN_PATH"
                    continue
                payload = {"k": len(cut), "cells": cells_b64, "digest16": digest, "witness": witness_b64}
                self.current_cut = cut
                self.current_cut_digest = digest
                self.current_cut_cells = cells_b64
                self.current_cut_witness = witness_b64
                self.cut_attempts += 1
                self.state = "AWAIT_CUT_RESPONSE"
                return self.make_message("CUT_PROPOSE", payload)

            if self.state == "PREPARE_CUT_CERT":
                payload = {"k": len(self.current_cut or []), "cells": self.current_cut_cells or "", "digest16": self.current_cut_digest, "witness": self.current_cut_witness or "", "signed_by": ["A", "B"]}
                self.state = "AWAIT_CUT_CERT_ACK"
                return self.make_message("CUT_CERT", payload)

            if self.state == "READY_DONE":
                self.state = "DONE"
                return self.make_message("DONE", {})

            if self.state == "DONE":
                raise RuntimeError("Agent A requested action after termination")

            raise RuntimeError(f"Agent A in unknown state {self.state}")

    def _handle_probe_reply(self, message: Msg) -> None:
        payload = message.payload
        cells_raw = payload.get("cells", [])
        blocked_b64 = payload.get("blocked")
        cells: List[Coordinate] = [tuple(map(int, cell)) for cell in cells_raw if len(cell) == 2]
        if blocked_b64 is not None:
            try:
                bitmap = decode_witness_bits(base64.b64decode(blocked_b64, validate=True), len(cells))
            except Exception:
                bitmap = [0] * len(cells)
        else:
            bitmap = [0] * len(cells)
        for cell, bit in zip(cells, bitmap):
            if bit:
                self.belief_peer_blocks.add(cell)
                self.belief_peer_free.discard(cell)
            else:
                self.belief_peer_free.add(cell)
                self.belief_peer_blocks.discard(cell)
        self.awaiting_probe_reply = False
        self.probe_used = False
        self.state = "PLAN_CUT"

    def _select_probe_cells(self, conflicts: Sequence[Sequence[int]]) -> List[Coordinate]:
        if not self.current_cut:
            return []
        unknown = [cell for cell in self.current_cut if cell not in self.belief_peer_blocks and cell not in self.belief_peer_free]
        for entry in conflicts:
            if len(entry) != 2:
                continue
            cell = (int(entry[0]), int(entry[1]))
            if cell not in unknown and cell not in self.belief_peer_blocks and cell not in self.belief_peer_free:
                unknown.append(cell)
        return unknown[: self.PROBE_LIMIT]

    def _update_halo(self, conflicts: Sequence[Sequence[int]]) -> None:
        for entry in conflicts:
            if len(entry) != 2:
                continue
            x, y = int(entry[0]), int(entry[1])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    cell = (x + dx, y + dy)
                    self.halo_blocks[cell] = self.HALO_TTL

    def _decay_halo(self) -> None:
        expired = [cell for cell, ttl in self.halo_blocks.items() if ttl <= 1]
        for cell in expired:
            self.halo_blocks.pop(cell, None)
        for cell in list(self.halo_blocks):
            self.halo_blocks[cell] -= 1

    def _halo_set(self) -> Set[Coordinate]:
        return {cell for cell, ttl in self.halo_blocks.items() if ttl > 0}

    def _plan_cut(self) -> List[Coordinate]:
        cut = self.min_cut(self.belief_peer_blocks, self.belief_peer_free)
        cut_sorted = sorted(set(cut))
        return cut_sorted

    def _ingest_conflicts(self, conflicts: Sequence[Sequence[int]], mode: str) -> None:
        for item in conflicts:
            if len(item) != 2:
                continue
            cell = (int(item[0]), int(item[1]))
            if mode == "PATH":
                self.belief_peer_blocks.add(cell)
                self.belief_peer_free.discard(cell)
            elif mode == "CUT":
                self.belief_peer_free.add(cell)
                self.belief_peer_blocks.discard(cell)
```

```python
"""Responder agent B."""
from __future__ import annotations

import base64
from typing import Iterable, List, Optional, Sequence, Set, Tuple

from agent_talk.agents.fsm_base import AgentConfig, FiniteStateAgent, WITNESS_MAP
from agent_talk.core.messages import Msg
from agent_talk.core.rle import decode_path_rle4, PathCodecError
from agent_talk.core.coords import (
    decode_cells_delta16,
    CodecError,
    bytes_to_coords,
    decode_witness_bits,
    encode_witness_bits,
)
from agent_talk.core.crc16 import crc16_ccitt
from agent_talk.env.grid import neighbors

Coordinate = Tuple[int, int]


class AgentB(FiniteStateAgent):
    """Responder that validates proposals against its private map."""

    def __init__(self, config: AgentConfig) -> None:
        super().__init__(config)
        self.last_path_digest: Optional[int] = None
        self.last_cut_digest: Optional[int] = None
        self.peer_blocks_from_a: Set[Coordinate] = set()

    def step(self, incoming: Optional[Msg]) -> Msg:
        if incoming is None:
            raise RuntimeError("Agent B requires an incoming message")
        handler = getattr(self, f"_handle_{incoming.type.lower()}", None)
        if handler is None:
            return self.make_message("NACK", {"nack_of": incoming.type, "reason": "FORMAT"})
        return handler(incoming)

    # Message handlers -----------------------------------------------------

    def _handle_path_propose(self, message: Msg) -> Msg:
        payload = message.payload
        digest = int(payload.get("digest16"))
        try:
            path = self._decode_path(payload)
        except ValueError as exc:
            return self.make_message("NACK", {"nack_of": "PATH_PROPOSE", "reason": "FORMAT", "detail": str(exc)})
        blocked_bits = [1 if self.grid.is_blocked(cell) else 0 for cell in path]
        if any(blocked_bits):
            from agent_talk.core.coords import encode_witness_bits
            mask = encode_witness_bits(blocked_bits)
            import base64
            return self.make_message(
                "NACK",
                {"nack_of": "PATH_PROPOSE", "reason": "BLOCKED", "mask": base64.b64encode(mask).decode("ascii")},
            )
        # Fast-path: can certify now
        self.last_path_digest = digest
        return self.make_message(
            "PATH_CERT",
            {
                "runs": payload.get("runs"),
                "digest16": digest,
                "signed_by": ["B"],
            },
        )

    def _handle_path_cert(self, message: Msg) -> Msg:
        payload = message.payload
        digest = int(payload.get("digest16"))
        if self.last_path_digest != digest:
            return self.make_message(
                "NACK", {"nack_of": "PATH_CERT", "reason": "INVALID", "detail": "digest mismatch"}
            )
        try:
            path = self._decode_path(payload)
        except ValueError as exc:
            return self.make_message("NACK", {"nack_of": "PATH_CERT", "reason": "FORMAT", "detail": str(exc)})
        if any(self.grid.is_blocked(cell) for cell in path):
            return self.make_message("NACK", {"nack_of": "PATH_CERT", "reason": "INVALID"})
        return self.make_message("ACK", {"ack_of": "PATH_CERT", "digest16": digest})

    def _handle_cut_propose(self, message: Msg) -> Msg:
        payload = message.payload
        digest = int(payload.get("digest16"))
        try:
            cells, witnesses = self._decode_cut(payload)
        except ValueError as exc:
            return self.make_message("NACK", {"nack_of": "CUT_PROPOSE", "reason": "FORMAT", "detail": str(exc)})
        conflicts = []
        for cell, witness in zip(cells, witnesses):
            if witness == WITNESS_MAP["A"]:
                self.peer_blocks_from_a.add(cell)
            blocked_local = self.grid.is_blocked(cell)
            if not blocked_local and witness != WITNESS_MAP["A"]:
                conflicts.append(list(cell))
        if conflicts:
            conflicts = conflicts[:8]
            return self.make_message("NACK", {"nack_of": "CUT_PROPOSE", "reason": "BLOCKED", "conflicts": conflicts})
        if self._connected_without_cut(cells):
            return self.make_message("NACK", {"nack_of": "CUT_PROPOSE", "reason": "INVALID"})
        # Fast-path: issue certificate immediately
        self.last_cut_digest = digest
        return self.make_message(
            "CUT_CERT",
            {
                "k": len(cells),
                "cells": payload.get("cells"),
                "digest16": digest,
                "witness": payload.get("witness", ""),
                "signed_by": ["B"],
            },
        )

    def _handle_cut_cert(self, message: Msg) -> Msg:
        payload = message.payload
        digest = int(payload.get("digest16"))
        if self.last_cut_digest != digest:
            return self.make_message(
                "NACK", {"nack_of": "CUT_CERT", "reason": "INVALID", "detail": "digest mismatch"}
            )
        try:
            cells, witnesses = self._decode_cut(payload)
        except ValueError as exc:
            return self.make_message("NACK", {"nack_of": "CUT_CERT", "reason": "FORMAT", "detail": str(exc)})
        invalid = False
        for cell, witness in zip(cells, witnesses):
            if witness == WITNESS_MAP["A"]:
                self.peer_blocks_from_a.add(cell)
            if not self.grid.is_blocked(cell) and witness != WITNESS_MAP["A"]:
                invalid = True
                break
        if invalid or self._connected_without_cut(cells):
            return self.make_message("NACK", {"nack_of": "CUT_CERT", "reason": "INVALID"})
        return self.make_message("ACK", {"ack_of": "CUT_CERT", "digest16": digest})

    def _handle_probe(self, message: Msg) -> Msg:
        payload = message.payload
        if payload.get("what") == "CELLS":
            cells_raw = payload.get("cells", [])
            cells = [tuple(map(int, cell)) for cell in cells_raw if len(cell) == 2]
            bits = [1 if self.grid.is_blocked(cell) else 0 for cell in cells]
            bits_bytes = encode_witness_bits(bits)
            return self.make_message(
                "PROBE_REPLY",
                {
                    "cells": [list(cell) for cell in cells],
                    "blocked": base64.b64encode(bits_bytes).decode("ascii"),
                },
            )
        return self.make_message("NACK", {"nack_of": "PROBE", "reason": "FORMAT"})

    def _handle_done(self, message: Msg) -> Msg:
        return self.make_message("DONE", {})

    def _handle_hello(self, message: Msg) -> Msg:
        return self.make_message("ACK", {"ack_of": "HELLO", "digest16": 0})

    def _handle_schema(self, message: Msg) -> Msg:
        return self.make_message("ACK", {"ack_of": "SCHEMA", "digest16": 0})

    # Utilities ------------------------------------------------------------

    def _decode_path(self, payload: dict) -> List[Coordinate]:
        encoding = payload.get("encoding", "RLE4_v1")
        runs_b64 = payload.get("runs", "")
        try:
            runs = base64.b64decode(runs_b64, validate=True)
        except (ValueError, base64.binascii.Error) as exc:  # type: ignore[attr-defined]
            raise ValueError(f"invalid base64 runs: {exc}") from exc
        if crc16_ccitt(runs) != int(payload.get("digest16")):
            raise ValueError("digest mismatch")
        start = tuple(payload.get("s", self.config.start))  # type: ignore[assignment]
        end = tuple(payload.get("t", self.config.goal))
        if start != self.config.start or end != self.config.goal:  # type: ignore[arg-type]
            raise ValueError("endpoint mismatch")
        if encoding == "RLE4_v1":
            try:
                path = decode_path_rle4(self.config.start, runs)
            except PathCodecError as exc:
                raise ValueError(str(exc)) from exc
        elif encoding == "ABS16_v1":
            coords = bytes_to_coords(runs)
            if not coords or coords[0] != self.config.start or coords[-1] != self.config.goal:
                raise ValueError("invalid absolute path")
            for a, b in zip(coords, coords[1:]):
                if abs(a[0] - b[0]) + abs(a[1] - b[1]) != 1:
                    raise ValueError("non-Manhattan step in absolute path")
            path = coords
        else:
            raise ValueError("unsupported encoding")
        return path

    def _decode_cut(self, payload: dict) -> Tuple[List[Coordinate], List[int]]:
        encoding = payload.get("encoding", "DELTA16_v1")
        cells_b64 = payload.get("cells", "")
        try:
            cells_bytes = base64.b64decode(cells_b64, validate=True)
        except (ValueError, base64.binascii.Error) as exc:  # type: ignore[attr-defined]
            raise ValueError(f"invalid base64 cells: {exc}") from exc
        if crc16_ccitt(cells_bytes) != int(payload.get("digest16")):
            raise ValueError("digest mismatch")
        if encoding == "DELTA16_v1":
            try:
                cells = decode_cells_delta16(cells_bytes)
            except CodecError as exc:
                raise ValueError(str(exc)) from exc
        elif encoding == "ABS16_v1":
            cells = bytes_to_coords(cells_bytes)
        else:
            raise ValueError("unsupported encoding")
        if len(cells) != int(payload.get("k")):
            raise ValueError("length mismatch")
        witness_b64 = payload.get("witness")
        if witness_b64 is None:
            raise ValueError("missing witness bits")
        try:
            witness_bytes = base64.b64decode(witness_b64, validate=True)
        except (ValueError, base64.binascii.Error) as exc:  # type: ignore[attr-defined]
            raise ValueError(f"invalid base64 witness: {exc}") from exc
        witnesses = decode_witness_bits(witness_bytes, len(cells))
        return cells, witnesses

    def _connected_without_cut(self, cut_cells: Sequence[Coordinate]) -> bool:
        cut = set(cut_cells)
        if self.config.start in cut or self.config.goal in cut:
            return False
        stack = [self.config.start]
        seen = {self.config.start}
        while stack:
            cell = stack.pop()
            if cell == self.config.goal:
                return True
            for nxt in neighbors(cell, self.config.height, self.config.width):
                if nxt in seen or nxt in cut:
                    continue
                seen.add(nxt)
                stack.append(nxt)
        return False
```

```python
"""Responder-led MinCut baseline.

Agent B computes a cut on its private map and sends a CUT_CERT signed by B.
Agent A validates on its private map and ACKs or NACKs with conflicts.
On NACK, B performs at most one tiny PROBE on the conflicting cells, updates
its view of peer-blocked cells, recomputes the cut, and resends a CUT_CERT.
No further loops.
"""
from __future__ import annotations

import base64
from typing import List, Optional, Sequence, Set, Tuple

from agent_talk.agents.fsm_base import AgentConfig, FiniteStateAgent, WITNESS_MAP
from agent_talk.core.messages import Msg
from agent_talk.core.coords import (
    decode_cells_delta16,
    CodecError,
    bytes_to_coords,
    decode_witness_bits,
    encode_witness_bits,
)
from agent_talk.core.crc16 import crc16_ccitt
from agent_talk.env.grid import neighbors

Coordinate = Tuple[int, int]


class ResponderMinCutA(FiniteStateAgent):
    """Initiator that sends SCHEMA then validates B's min-cut certificate."""

    def __init__(self, config: AgentConfig) -> None:
        super().__init__(config)
        self.state = "SEND_SCHEMA"

    def step(self, incoming: Optional[Msg]) -> Msg:
        if incoming is not None:
            if incoming.type == "CUT_CERT":
                ok, conflicts = self._validate_cut_cert(incoming.payload)
                if ok:
                    return self.make_message("ACK", {"ack_of": "CUT_CERT", "digest16": int(incoming.payload.get("digest16", 0))})
                return self.make_message(
                    "NACK",
                    {"nack_of": "CUT_PROPOSE", "reason": "BLOCKED", "conflicts": [list(c) for c in conflicts[:8]]},
                )
            if incoming.type == "PROBE_REPLY":
                # A is not the probed side in this baseline; ignore.
                return self.make_message("NACK", {"nack_of": "PROBE_REPLY", "reason": "FORMAT"})
        if self.state == "SEND_SCHEMA":
            self.state = "WAIT"
            return self.make_message(
                "SCHEMA",
                {
                    "s": list(self.config.start),
                    "t": list(self.config.goal),
                    "size": [self.config.width, self.config.height],
                    "path_enc": "RLE4_v1",
                    "cut_enc": "DELTA16_v1",
                },
            )
        return self.make_message("HELLO", {})

    def _validate_cut_cert(self, payload: dict) -> Tuple[bool, List[Coordinate]]:
        # Decode cells
        encoding = payload.get("encoding", "DELTA16_v1")
        cells_b64 = payload.get("cells", "")
        try:
            cells_bytes = base64.b64decode(cells_b64, validate=True)
        except (ValueError, base64.binascii.Error) as exc:  # type: ignore[attr-defined]
            return False, []
        if crc16_ccitt(cells_bytes) != int(payload.get("digest16", -1)):
            return False, []
        if encoding == "DELTA16_v1":
            try:
                cells = decode_cells_delta16(cells_bytes)
            except CodecError:
                return False, []
        elif encoding == "ABS16_v1":
            cells = bytes_to_coords(cells_bytes)
        else:
            return False, []
        if len(cells) != int(payload.get("k", -1)):
            return False, []
        # Witness bits
        witness_b64 = payload.get("witness")
        if not witness_b64:
            return False, []
        try:
            witness_bytes = base64.b64decode(witness_b64, validate=True)
        except (ValueError, base64.binascii.Error):  # type: ignore[attr-defined]
            return False, []
        witnesses = decode_witness_bits(witness_bytes, len(cells))
        # Validate against A's map: any unwitnessed-free cell is a conflict
        conflicts: List[Coordinate] = []
        for cell, w in zip(cells, witnesses):
            blocked_local = self.grid.is_blocked(cell)
            if not blocked_local and w != WITNESS_MAP["A"]:
                conflicts.append(cell)
        if conflicts:
            return False, conflicts
        # Check disconnection in A's potential grid
        if self._connected_without_cut(cells):
            return False, []
        return True, []

    def _connected_without_cut(self, cut_cells: Sequence[Coordinate]) -> bool:
        cut = set(cut_cells)
        if self.config.start in cut or self.config.goal in cut:
            return False
        stack = [self.config.start]
        seen = {self.config.start}
        while stack:
            cell = stack.pop()
            if cell == self.config.goal:
                return True
            for nxt in neighbors(cell, self.config.height, self.config.width):
                if nxt in seen or nxt in cut:
                    continue
                seen.add(nxt)
                stack.append(nxt)
        return False


class ResponderMinCutB(FiniteStateAgent):
    """Responder that sends CUT_CERT, probes once on conflicts, and retries once."""

    PROBE_LIMIT = 6

    def __init__(self, config: AgentConfig) -> None:
        super().__init__(config)
        self.state = "WAIT_SCHEMA"
        self.peer_blocks: Set[Coordinate] = set()
        self.sent_digest: Optional[int] = None
        self.retry_done = False

    def step(self, incoming: Optional[Msg]) -> Msg:
        if incoming is None:
            raise RuntimeError("ResponderMinCutB requires incoming message")
        if self.state == "WAIT_SCHEMA":
            # On any first message, send certificate
            self.state = "WAIT_CUT_ACK"
            return self._send_cut_cert()
        if self.state == "WAIT_CUT_ACK":
            if incoming.type == "ACK" and incoming.payload.get("ack_of") == "CUT_CERT":
                return self.make_message("DONE", {})
            if incoming.type == "NACK" and incoming.payload.get("nack_of") in {"CUT_PROPOSE", "CUT_CERT"} and not self.retry_done:
                conflicts = [tuple(map(int, c)) for c in incoming.payload.get("conflicts", []) if len(c) == 2]
                probe_cells = conflicts[: self.PROBE_LIMIT]
                if probe_cells:
                    self.state = "WAIT_PROBE_REPLY"
                    return self.make_message("PROBE", {"what": "CELLS", "cells": [list(c) for c in probe_cells]})
                # No conflicts provided; terminate
                self.retry_done = True
                return self._send_cut_cert()
            # Any other response: terminate attempt
            return self.make_message("DONE", {})
        if self.state == "WAIT_PROBE_REPLY":
            if incoming.type == "PROBE_REPLY":
                self._ingest_probe_reply(incoming)
                self.retry_done = True
                self.state = "WAIT_CUT_ACK"
                return self._send_cut_cert()
            return self.make_message("DONE", {})
        return self.make_message("DONE", {})

    def _send_cut_cert(self) -> Msg:
        cut = self.min_cut(self.peer_blocks, set())
        cells_b64, digest, witness_b64 = self.encode_cut(cut, self.peer_blocks)
        self.sent_digest = digest
        payload = {"k": len(cut), "cells": cells_b64, "digest16": digest, "witness": witness_b64, "signed_by": ["B"]}
        return self.make_message("CUT_CERT", payload)

    def _ingest_probe_reply(self, message: Msg) -> None:
        payload = message.payload
        cells_raw = payload.get("cells", [])
        blocked_b64 = payload.get("blocked")
        cells: List[Coordinate] = [tuple(map(int, cell)) for cell in cells_raw if len(cell) == 2]
        bits = []
        if blocked_b64 is not None:
            try:
                bits = decode_witness_bits(base64.b64decode(blocked_b64, validate=True), len(cells))
            except Exception:
                bits = []
        for cell, bit in zip(cells, bits):
            if bit:
                self.peer_blocks.add(cell)
```

```python
"""Single conversation runner."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List, Optional

from agent_talk.agents.agent_a import AgentA
from agent_talk.agents.agent_b import AgentB
from agent_talk.core.messages import Msg
from agent_talk.core.protocol import ConversationLimits, ProtocolError


@dataclass(slots=True)
class SimulationResult:
    transcript: List[Dict[str, object]]
    bytes_used: int
    rounds: int
    outcome: str
    certificate_type: Optional[str]
    certificate_payload: Optional[dict]
    reason: Optional[str]
    diagnostics: Dict[str, object]

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def simulate_conversation(agent_a: AgentA, agent_b: AgentB, limits: Optional[ConversationLimits] = None) -> SimulationResult:
    limits = limits or ConversationLimits()
    transcript: List[Dict[str, object]] = []
    prev_seq = {"A": -1, "B": -1}
    bytes_used = 0
    rounds = 0
    outcome = "UNKNOWN"
    certificate_type: Optional[str] = None
    certificate_payload: Optional[dict] = None

    incoming_for_a: Optional[Msg] = None
    incoming_for_b: Optional[Msg] = None
    sender = "A"

    guard_used = False
    while True:
        if rounds >= limits.max_rounds:
            outcome = "ROUND_LIMIT"
            break
        if sender == "A":
            message = agent_a.step(incoming_for_a)
        else:
            message = agent_b.step(incoming_for_b)

        if message.seq <= prev_seq[sender]:
            raise ProtocolError(f"sequence monotonicity violated for {sender}")
        prev_seq[sender] = message.seq

        raw = message.to_json()
        size = len(raw.encode("utf-8"))
        if size > limits.max_bytes_per_message:
            raise ProtocolError(f"message exceeds size limit ({size}>{limits.max_bytes_per_message})")
        bytes_used += size
        if bytes_used > limits.max_total_bytes:
            outcome = "BYTE_LIMIT"
            break

        transcript.append({"sender": sender, "message": raw, "bytes": size})
        rounds += 1

        if message.type in {"PATH_CERT", "CUT_CERT"}:
            certificate_type = message.type
            certificate_payload = message.payload

        # Treat ACK on a certificate as terminal (ACK-terminates)
        if message.type == "ACK" and message.payload.get("ack_of") in {"PATH_CERT", "CUT_CERT"}:
            outcome = "DONE"
            transcript[-1]["terminal"] = True
            break

        if message.type == "DONE":
            outcome = "DONE"
            break

        if sender == "A":
            incoming_for_b = message
            sender = "B"
        else:
            incoming_for_a = message
            sender = "A"

    reason = None if outcome == "DONE" else outcome
    diagnostics: Dict[str, object] = {}
    if hasattr(agent_a, "belief_peer_blocks"):
        diagnostics["a_belief_blocks"] = len(getattr(agent_a, "belief_peer_blocks", []))
        diagnostics["a_belief_free"] = len(getattr(agent_a, "belief_peer_free", []))
        diagnostics["a_failed_path_digests"] = len(getattr(agent_a, "failed_path_digests", []))
        diagnostics["a_failed_cut_digests"] = len(getattr(agent_a, "failed_cut_digests", []))
    if hasattr(agent_b, "peer_blocks_from_a"):
        diagnostics["b_peer_blocks_from_a"] = len(getattr(agent_b, "peer_blocks_from_a", []))
    return SimulationResult(
        transcript=transcript,
        bytes_used=bytes_used,
        rounds=rounds,
        outcome=outcome,
        certificate_type=certificate_type,
        certificate_payload=certificate_payload,
        reason=reason,
        diagnostics=diagnostics,
    )
```

```python
"""Batch evaluation runner."""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Tuple

from agent_talk.agents import (
    AgentA,
    AgentB,
    AgentConfig,
    SendAllAgentA,
    SendAllAgentB,
    ResponderMinCutA,
    ResponderMinCutB,
)
from agent_talk.core.coords import bytes_to_coords, decode_cells_delta16
from agent_talk.core.rle import decode_path_rle4
from agent_talk.core.protocol import ConversationLimits
from agent_talk.core.messages import set_compact_schema
from agent_talk.env.grid import Grid
from agent_talk.io import CacheEntry, iter_cache, append_log
from agent_talk.oracle.oracle import OracleError, verify_cut_cert, verify_path_cert, union_grid
from agent_talk.runners import simulate_conversation

try:  # optional dependency
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None


def load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is not None:
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    return simple_yaml_load(path.read_text(encoding="utf-8"))


def simple_yaml_load(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    stack: list[Tuple[int, Dict[str, Any]]] = [(0, data)]
    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.lstrip().partition(":")
        key = key.strip()
        value = value.strip()
        while stack and indent < stack[-1][0]:
            stack.pop()
        container = stack[-1][1]
        if not value:
            new_dict: Dict[str, Any] = {}
            container[key] = new_dict
            stack.append((indent + 2, new_dict))
        else:
            container[key] = parse_scalar(value)
    return data


def parse_scalar(value: str) -> Any:
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def make_limits(cfg: Dict[str, Any]) -> ConversationLimits:
    return ConversationLimits(
        max_rounds=int(cfg.get("max_rounds", 64)),
        max_bytes_per_message=int(cfg.get("max_bytes_per_message", 256)),
        max_total_bytes=int(cfg.get("max_total_bytes", 3 * 1024)),
    )


def apply_ablation(system_cfg: Dict[str, Any], ablation_cfg: Dict[str, Any]) -> Dict[str, Any]:
    merged = json.loads(json.dumps(system_cfg))
    if not ablation_cfg:
        return merged
    if "encoding" in ablation_cfg:
        merged.setdefault("encoding", {}).update(ablation_cfg["encoding"])
    if ablation_cfg.get("forbid_path"):
        merged["allow_path"] = False
    if ablation_cfg.get("forbid_cut"):
        merged["allow_cut"] = False
    if "grid_size" in ablation_cfg:
        merged["grid_size"] = ablation_cfg["grid_size"]
    return merged


def make_agent_configs(entry: CacheEntry, system: str, cfg: Dict[str, Any]) -> Tuple[AgentConfig, AgentConfig, Dict[str, Any]]:
    grid_override = cfg.get("grid_size")
    if grid_override and entry.height != grid_override:
        raise ValueError("grid size mismatch for ablation")

    encoding_cfg = cfg.get("encoding", {})
    base_params = {
        "max_path_attempts": cfg.get("max_path_attempts", cfg.get("max_probes", 6)),
        "max_path_length": cfg.get("max_path_length", 64),
        "allow_path": cfg.get("allow_path", True),
        "allow_cut": cfg.get("allow_cut", True),
        "path_encoding": encoding_cfg.get("paths", "RLE4_v1"),
        "cut_encoding": encoding_cfg.get("cuts", "DELTA16_v1"),
    }
    config_a = AgentConfig(
        name="A",
        height=entry.height,
        width=entry.width,
        start=entry.start,
        goal=entry.goal,
        private_mask=entry.mask_a,
        **base_params,
    )
    config_b = AgentConfig(
        name="B",
        height=entry.height,
        width=entry.width,
        start=entry.start,
        goal=entry.goal,
        private_mask=entry.mask_b,
        **base_params,
    )
    return config_a, config_b, cfg


def instantiate_agents(system: str, config_a: AgentConfig, config_b: AgentConfig, system_cfg: Dict[str, Any]):
    if system == "certtalk" or system == "greedyprobe":
        return AgentA(config_a), AgentB(config_b)
    if system == "cutgrow":
        config_a.allow_path = False
        config_b.allow_path = False
        return AgentA(config_a), AgentB(config_b)
    if system == "sendall":
        chunk_size = system_cfg.get("chunk_size", 32)
        return SendAllAgentA(config_a, chunk_size=chunk_size), SendAllAgentB(config_b, chunk_size=chunk_size)
    if system in {"respondmincut", "respondermincut"}:
        # B leads with cut cert; A initiates with SCHEMA and validates.
        # For symmetry, use allow_cut only.
        config_a.allow_path = False
        config_b.allow_path = False
        return ResponderMinCutA(config_a), ResponderMinCutB(config_b)
    raise ValueError(f"unknown system {system}")


def decode_path_length(payload: Dict[str, Any], start: Tuple[int, int]) -> int:
    encoding = payload.get("encoding", "RLE4_v1")
    data = base64.b64decode(payload.get("runs", ""), validate=True)
    if encoding == "RLE4_v1":
        path = decode_path_rle4(start, data)
    elif encoding == "ABS16_v1":
        path = bytes_to_coords(data)
    else:
        raise ValueError("unknown path encoding")
    return max(0, len(path) - 1)


def decode_cut_size(payload: Dict[str, Any]) -> int:
    encoding = payload.get("encoding", "DELTA16_v1")
    data = base64.b64decode(payload.get("cells", ""), validate=True)
    if encoding == "DELTA16_v1":
        cells = decode_cells_delta16(data)
    elif encoding == "ABS16_v1":
        cells = bytes_to_coords(data)
    else:
        raise ValueError("unknown cut encoding")
    return len(cells)


def run(cache: Path, system: str, out: Path, config_path: Path, ablation: Optional[str], ablation_path: Optional[Path], split: Optional[str]) -> None:
    base_cfg = load_yaml(config_path) if config_path else {}
    system_cfg = base_cfg.get("systems", {}).get(system, {})
    limits_cfg = base_cfg.get("limits", {})
    ablation_cfg: Dict[str, Any] = {}
    if ablation and ablation_path:
        ablations = load_yaml(ablation_path)
        ablation_cfg = ablations.get(ablation, {}) if isinstance(ablations, dict) else {}
    merged_cfg = apply_ablation(system_cfg, ablation_cfg)
    limits = make_limits(limits_cfg)
    # Optional compact schema toggle (per system)
    set_compact_schema(bool(merged_cfg.get("compact_schema", False)))

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        pass  # truncate

    for entry in iter_cache(cache):
        if split and entry.split != split:
            continue
        try:
            config_a, config_b, effective_cfg = make_agent_configs(entry, system, merged_cfg)
        except ValueError:
            continue
        agent_a, agent_b = instantiate_agents(system, config_a, config_b, effective_cfg)
        result = simulate_conversation(agent_a, agent_b, limits)

        grid_a = Grid.from_flat(entry.height, entry.width, entry.mask_a)
        grid_b = Grid.from_flat(entry.height, entry.width, entry.mask_b)
        union = union_grid(grid_a, grid_b)

        oracle_ok = False
        path_gap = None
        cut_gap = None
        if result.certificate_type and result.certificate_payload:
            try:
                if result.certificate_type == "PATH_CERT":
                    oracle_ok = verify_path_cert(result.certificate_payload, union, entry.start, entry.goal)
                    if entry.shortest is not None:
                        path_gap = decode_path_length(result.certificate_payload, entry.start) - entry.shortest
                elif result.certificate_type == "CUT_CERT":
                    oracle_ok = verify_cut_cert(result.certificate_payload, union, entry.start, entry.goal)
                    if entry.min_cut is not None:
                        cut_gap = decode_cut_size(result.certificate_payload) - entry.min_cut
            except OracleError:
                oracle_ok = False

        record = {
            "system": system,
            "split": entry.split,
            "seed": entry.seed,
            "outcome": result.outcome,
            "bytes": result.bytes_used,
            "rounds": result.rounds,
            "certificate_type": result.certificate_type,
            "oracle_accepted": oracle_ok,
            "path_gap": path_gap,
            "cut_gap": cut_gap,
            "reason": result.reason,
            "ablation": ablation,
            "transcript": result.transcript,
            "diagnostics": result.diagnostics,
        }
        append_log(out, record)


def main(argv: Optional[Iterable[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Run batch evaluations.")
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--system", type=str, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("configs/base.yaml"))
    parser.add_argument("--ablation", type=str, default=None)
    parser.add_argument("--ablations-config", type=Path, default=Path("configs/ablations.yaml"))
    parser.add_argument("--split", type=str, default=None)
    args = parser.parse_args(list(argv) if argv is not None else None)

    run(
        cache=args.cache,
        system=args.system,
        out=args.out,
        config_path=args.config,
        ablation=args.ablation,
        ablation_path=args.ablations_config,
        split=args.split,
    )


if __name__ == "__main__":
    main()
```

