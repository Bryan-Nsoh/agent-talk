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
