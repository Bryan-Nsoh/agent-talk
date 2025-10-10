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
        self.pending_reply: Optional[Tuple[str, dict]] = None

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
                self.state = "PLAN_CUT"
            else:
                self.state = "PLAN_CUT"
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
                self.state = "READY_DONE"
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
