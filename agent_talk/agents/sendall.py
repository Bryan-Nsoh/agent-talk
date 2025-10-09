"""Send-All baseline agents."""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Set, Tuple

from agent_talk.agents.fsm_base import AgentConfig, FiniteStateAgent
from agent_talk.core.messages import Msg
from agent_talk.env.grid import Grid, bfs_free
from agent_talk.oracle.oracle import min_vertex_cut_potential

Coordinate = Tuple[int, int]


class SendAllAgentA(FiniteStateAgent):
    def __init__(self, config: AgentConfig, chunk_size: int = 32) -> None:
        super().__init__(config)
        self.chunk_size = max(1, chunk_size)
        self.blocked_indices = [i for i, v in enumerate(self.private_mask) if v]
        self.total_chunks = max(1, (len(self.blocked_indices) + self.chunk_size - 1) // self.chunk_size)
        self.chunk_idx = 0
        self.state = "SEND_CHUNK"
        self.received_cert: Optional[Msg] = None

    def step(self, incoming: Optional[Msg]) -> Msg:
        if incoming is not None:
            self._handle_incoming(incoming)
        return self._next_message()

    def _handle_incoming(self, message: Msg) -> None:
        if self.state == "AWAIT_ACK" and message.type == "ACK" and message.payload.get("ack_of") == "PROBE":
            self.chunk_idx += 1
            self.state = "SEND_CHUNK"
        elif self.state == "AWAIT_CERT" and message.type in {"PATH_CERT", "CUT_CERT"}:
            self.received_cert = message
            self.state = "ACK_CERT"
        elif self.state == "WAIT_DONE" and message.type == "DONE":
            self.state = "SEND_DONE"

    def _next_message(self) -> Msg:
        if self.state == "SEND_CHUNK":
            start = self.chunk_idx * self.chunk_size
            end = min(len(self.blocked_indices), start + self.chunk_size)
            chunk = self.blocked_indices[start:end]
            final = self.chunk_idx == self.total_chunks - 1
            payload = {
                "what": "CELLS",
                "chunk": self.chunk_idx,
                "total": self.total_chunks,
                "final": final,
                "indices": chunk,
            }
            self.state = "AWAIT_CERT" if final else "AWAIT_ACK"
            return self.make_message("PROBE", payload)
        if self.state == "ACK_CERT":
            if not self.received_cert:
                raise RuntimeError("no certificate to acknowledge")
            cert = self.received_cert
            digest = int(cert.payload.get("digest16"))
            self.state = "WAIT_DONE"
            return self.make_message("ACK", {"ack_of": cert.type, "digest16": digest})
        if self.state == "SEND_DONE":
            self.state = "DONE"
            return self.make_message("DONE", {})
        if self.state in {"AWAIT_ACK", "AWAIT_CERT", "WAIT_DONE"}:
            raise RuntimeError(f"Agent A idle without incoming message in state {self.state}")
        if self.state == "DONE":
            raise RuntimeError("Agent A already done")
        raise RuntimeError(f"Agent A unknown state {self.state}")


class SendAllAgentB(FiniteStateAgent):
    def __init__(self, config: AgentConfig, chunk_size: int = 32) -> None:
        super().__init__(config)
        self.chunk_size = chunk_size
        self.received_indices: Set[int] = set()
        self.expected_chunks: Optional[int] = None
        self.state = "EXPECT_CHUNK"
        self.cached_union: Optional[Grid] = None
        self.last_certificate: Optional[Msg] = None

    def step(self, incoming: Optional[Msg]) -> Msg:
        if incoming is None:
            raise RuntimeError("Agent B requires incoming message")
        if self.state == "EXPECT_CHUNK" and incoming.type == "PROBE":
            return self._handle_probe(incoming)
        if self.state == "WAIT_CERT_ACK" and incoming.type == "ACK":
            return self._handle_cert_ack(incoming)
        if incoming.type == "DONE":
            return self.make_message("DONE", {})
        return self.make_message("NACK", {"nack_of": incoming.type, "reason": "FORMAT"})

    def _handle_probe(self, message: Msg) -> Msg:
        payload = message.payload
        chunk = int(payload.get("chunk", 0))
        total = int(payload.get("total", 1))
        indices = [int(i) for i in payload.get("indices", [])]
        self.expected_chunks = total
        self.received_indices.update(indices)
        if payload.get("final"):
            certificate = self._build_certificate()
            self.last_certificate = certificate
            self.state = "WAIT_CERT_ACK"
            return certificate
        return self.make_message("ACK", {"ack_of": "PROBE", "chunk": chunk})

    def _handle_cert_ack(self, message: Msg) -> Msg:
        if not self.last_certificate:
            return self.make_message("NACK", {"nack_of": "ACK", "reason": "FORMAT"})
        digest = int(message.payload.get("digest16", -1))
        if digest != int(self.last_certificate.payload.get("digest16")):
            return self.make_message("NACK", {"nack_of": "ACK", "reason": "INVALID"})
        if message.payload.get("ack_of") != self.last_certificate.type:
            return self.make_message("NACK", {"nack_of": "ACK", "reason": "FORMAT"})
        self.last_certificate = None
        self.state = "SEND_DONE"
        return self._send_done()

    def _send_done(self) -> Msg:
        self.state = "DONE"
        return self.make_message("DONE", {})

    def _build_certificate(self) -> Msg:
        union_grid = self._union_grid()
        path = bfs_free(union_grid, self.config.start, self.config.goal)
        if path is not None:
            encoded, digest = self.encode_path(path)
            payload = {
                "s": list(self.config.start),
                "t": list(self.config.goal),
                "encoding": self.config.path_encoding,
                "runs": encoded,
                "digest16": digest,
                "signed_by": ["B"],
            }
            return self.make_message("PATH_CERT", payload)
        cut = min_vertex_cut_potential(union_grid, self.config.start, self.config.goal)
        peer_blocks = { (idx % self.config.width, idx // self.config.width) for idx in self.received_indices }
        encoded, digest, witness = self.encode_cut(cut, peer_blocks)
        payload = {
            "encoding": self.config.cut_encoding,
            "k": len(cut),
            "cells": encoded,
            "digest16": digest,
            "witness": witness,
            "signed_by": ["B"],
        }
        return self.make_message("CUT_CERT", payload)

    def _union_grid(self) -> Grid:
        if self.cached_union is not None:
            return self.cached_union
        total_cells = self.config.height * self.config.width
        mask_a = [0] * total_cells
        for idx in self.received_indices:
            if 0 <= idx < total_cells:
                mask_a[idx] = 1
        union_mask = [1 if mask_a[i] or self.private_mask[i] else 0 for i in range(total_cells)]
        self.cached_union = Grid.from_flat(self.config.height, self.config.width, union_mask)
        return self.cached_union
