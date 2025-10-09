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

