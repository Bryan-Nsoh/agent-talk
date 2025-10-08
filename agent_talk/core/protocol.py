"""Protocol helpers: message validation, limits, transcript entries."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Literal, Optional

from .messages import Msg, MessageError, make_message

MessageType = Literal[
    "HELLO",
    "SCHEMA",
    "PROBE",
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
