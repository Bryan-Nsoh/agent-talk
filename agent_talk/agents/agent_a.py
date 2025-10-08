"""Initiator agent A."""
from __future__ import annotations

from typing import List, Optional, Sequence, Set, Tuple

from agent_talk.core.messages import Msg
from agent_talk.agents.fsm_base import AgentConfig, FiniteStateAgent

Coordinate = Tuple[int, int]


class AgentA(FiniteStateAgent):
    """Finite state initiator that favours paths before cuts."""

    def __init__(self, config: AgentConfig) -> None:
        super().__init__(config)
        if config.allow_path:
            self.state = "PLAN_PATH"
        elif config.allow_cut:
            self.state = "PLAN_CUT"
        else:
            self.state = "DONE"
        self.belief_peer_blocks: Set[Coordinate] = set()
        self.path_attempts = 0
        self.current_path: Optional[List[Coordinate]] = None
        self.current_path_digest: Optional[int] = None
        self.current_path_runs: Optional[str] = None
        self.current_cut: Optional[List[Coordinate]] = None
        self.current_cut_digest: Optional[int] = None
        self.current_cut_cells: Optional[str] = None

    def step(self, incoming: Optional[Msg]) -> Msg:
        if incoming is not None:
            self._handle_incoming(incoming)
        return self._next_message()

    def _handle_incoming(self, message: Msg) -> None:
        if self.state == "AWAIT_PATH_RESPONSE":
            if message.type == "ACK" and message.payload.get("ack_of") == "PATH_PROPOSE":
                if int(message.payload.get("digest16")) == self.current_path_digest:
                    self.state = "PREPARE_PATH_CERT"
                else:
                    self.state = "PLAN_PATH"
            elif message.type == "NACK" and message.payload.get("nack_of") == "PATH_PROPOSE":
                conflicts = message.payload.get("conflicts") or []
                self._ingest_conflicts(conflicts)
                self.path_attempts += 1
                if self.path_attempts >= self.config.max_path_attempts or not self.config.allow_path:
                    self.state = "PLAN_CUT"
                else:
                    self.state = "PLAN_PATH"
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
                    self.state = "PREPARE_CUT_CERT"
                else:
                    self.state = "PLAN_CUT"
            elif message.type == "NACK" and message.payload.get("nack_of") == "CUT_PROPOSE":
                conflicts = message.payload.get("conflicts") or []
                self._ingest_conflicts(conflicts)
                self.state = "PLAN_CUT"
        elif self.state == "AWAIT_CUT_CERT_ACK":
            if message.type == "ACK" and message.payload.get("ack_of") == "CUT_CERT":
                if int(message.payload.get("digest16")) == self.current_cut_digest:
                    self.state = "READY_DONE"
                else:
                    self.state = "PLAN_CUT"
        elif self.state == "READY_DONE":
            pass

    def _next_message(self) -> Msg:
        if self.state == "PLAN_PATH":
            if not self.config.allow_path:
                self.state = "PLAN_CUT"
                return self._next_message()
            path = self.plan_path(self.belief_peer_blocks)
            if path is None:
                self.state = "PLAN_CUT"
                return self._next_message()
            runs_b64, digest = self.encode_path(path)
            payload = {
                "s": list(self.config.start),
                "t": list(self.config.goal),
                "encoding": self.config.path_encoding,
                "runs": runs_b64,
                "digest16": digest,
            }
            self.current_path = path
            self.current_path_digest = digest
            self.current_path_runs = runs_b64
            self.state = "AWAIT_PATH_RESPONSE"
            return self.make_message("PATH_PROPOSE", payload)
        if self.state == "PREPARE_PATH_CERT":
            payload = {
                "s": list(self.config.start),
                "t": list(self.config.goal),
                "encoding": self.config.path_encoding,
                "runs": self.current_path_runs or "",
                "digest16": self.current_path_digest,
                "signed_by": ["A", "B"],
            }
            self.state = "AWAIT_PATH_CERT_ACK"
            return self.make_message("PATH_CERT", payload)
        if self.state == "PLAN_CUT":
            if not self.config.allow_cut:
                self.state = "DONE"
                return self.make_message("DONE", {"reason": "CUT_FORBIDDEN"})
            cut = self._plan_cut()
            if not cut:
                self.state = "DONE"
                return self.make_message("DONE", {"reason": "FAILED_TO_FIND_CERT"})
            cells_b64, digest = self.encode_cut(cut)
            payload = {
                "encoding": self.config.cut_encoding,
                "k": len(cut),
                "cells": cells_b64,
                "digest16": digest,
            }
            self.current_cut = cut
            self.current_cut_digest = digest
            self.current_cut_cells = cells_b64
            self.state = "AWAIT_CUT_RESPONSE"
            return self.make_message("CUT_PROPOSE", payload)
        if self.state == "PREPARE_CUT_CERT":
            payload = {
                "encoding": self.config.cut_encoding,
                "k": len(self.current_cut or []),
                "cells": self.current_cut_cells or "",
                "digest16": self.current_cut_digest,
                "signed_by": ["A", "B"],
            }
            self.state = "AWAIT_CUT_CERT_ACK"
            return self.make_message("CUT_CERT", payload)
        if self.state == "READY_DONE":
            self.state = "DONE"
            return self.make_message("DONE", {})
        if self.state == "DONE":
            raise RuntimeError("Agent A requested action after termination")
        raise RuntimeError(f"Agent A in unknown state {self.state}")

    def _plan_cut(self) -> List[Coordinate]:
        cut = self.min_cut(self.belief_peer_blocks)
        cut_sorted = sorted(set(cut))
        return cut_sorted

    def _ingest_conflicts(self, conflicts: Sequence[Sequence[int]]) -> None:
        for item in conflicts:
            if len(item) != 2:
                continue
            self.belief_peer_blocks.add((int(item[0]), int(item[1])))
