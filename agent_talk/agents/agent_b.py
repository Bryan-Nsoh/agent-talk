"""Responder agent B."""
from __future__ import annotations

import base64
from typing import Iterable, List, Optional, Sequence, Tuple

from agent_talk.agents.fsm_base import AgentConfig, FiniteStateAgent
from agent_talk.core.messages import Msg
from agent_talk.core.rle import decode_path_rle4, PathCodecError
from agent_talk.core.coords import decode_cells_delta16, CodecError, bytes_to_coords
from agent_talk.core.crc16 import crc16_ccitt
from agent_talk.env.grid import neighbors

Coordinate = Tuple[int, int]


class AgentB(FiniteStateAgent):
    """Responder that validates proposals against its private map."""

    def __init__(self, config: AgentConfig) -> None:
        super().__init__(config)
        self.last_path_digest: Optional[int] = None
        self.last_cut_digest: Optional[int] = None

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
        conflicts = [list(cell) for cell in path if self.grid.is_blocked(cell)]
        if conflicts:
            return self.make_message(
                "NACK",
                {"nack_of": "PATH_PROPOSE", "reason": "BLOCKED", "conflicts": conflicts},
            )
        self.last_path_digest = digest
        return self.make_message("ACK", {"ack_of": "PATH_PROPOSE", "digest16": digest})

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
        blocked = [list(cell) for cell in path if self.grid.is_blocked(cell)]
        if blocked:
            return self.make_message(
                "NACK", {"nack_of": "PATH_CERT", "reason": "BLOCKED", "conflicts": blocked}
            )
        return self.make_message("ACK", {"ack_of": "PATH_CERT", "digest16": digest})

    def _handle_cut_propose(self, message: Msg) -> Msg:
        payload = message.payload
        digest = int(payload.get("digest16"))
        try:
            cells = self._decode_cut(payload)
        except ValueError as exc:
            return self.make_message("NACK", {"nack_of": "CUT_PROPOSE", "reason": "FORMAT", "detail": str(exc)})
        conflicts = [list(cell) for cell in cells if not self.grid.is_blocked(cell)]
        if conflicts:
            return self.make_message(
                "NACK",
                {"nack_of": "CUT_PROPOSE", "reason": "BLOCKED", "conflicts": conflicts},
            )
        if self._connected_without_cut(cells):
            return self.make_message(
                "NACK",
                {"nack_of": "CUT_PROPOSE", "reason": "INVALID"},
            )
        self.last_cut_digest = digest
        return self.make_message("ACK", {"ack_of": "CUT_PROPOSE", "digest16": digest})

    def _handle_cut_cert(self, message: Msg) -> Msg:
        payload = message.payload
        digest = int(payload.get("digest16"))
        if self.last_cut_digest != digest:
            return self.make_message(
                "NACK", {"nack_of": "CUT_CERT", "reason": "INVALID", "detail": "digest mismatch"}
            )
        try:
            cells = self._decode_cut(payload)
        except ValueError as exc:
            return self.make_message("NACK", {"nack_of": "CUT_CERT", "reason": "FORMAT", "detail": str(exc)})
        if any(not self.grid.is_blocked(cell) for cell in cells) or self._connected_without_cut(cells):
            return self.make_message(
                "NACK", {"nack_of": "CUT_CERT", "reason": "INVALID"}
            )
        return self.make_message("ACK", {"ack_of": "CUT_CERT", "digest16": digest})

    def _handle_done(self, message: Msg) -> Msg:
        return self.make_message("DONE", {})

    def _handle_hello(self, message: Msg) -> Msg:
        return self.make_message("ACK", {"ack_of": "HELLO", "digest16": 0})

    def _handle_schema(self, message: Msg) -> Msg:
        return self.make_message("ACK", {"ack_of": "SCHEMA", "digest16": 0})

    # Utilities ------------------------------------------------------------

    def _decode_path(self, payload: dict) -> List[Coordinate]:
        encoding = payload.get("encoding")
        runs_b64 = payload.get("runs", "")
        try:
            runs = base64.b64decode(runs_b64, validate=True)
        except (ValueError, base64.binascii.Error) as exc:  # type: ignore[attr-defined]
            raise ValueError(f"invalid base64 runs: {exc}") from exc
        if crc16_ccitt(runs) != int(payload.get("digest16")):
            raise ValueError("digest mismatch")
        start = tuple(payload.get("s"))  # type: ignore[assignment]
        if start != self.config.start or tuple(payload.get("t")) != self.config.goal:  # type: ignore[arg-type]
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

    def _decode_cut(self, payload: dict) -> List[Coordinate]:
        encoding = payload.get("encoding")
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
        return cells

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
