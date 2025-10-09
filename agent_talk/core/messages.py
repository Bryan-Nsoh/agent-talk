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
