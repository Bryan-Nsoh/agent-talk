from __future__ import annotations

import json
import pytest

from agent_talk.core.messages import make_message, Msg, MessageError


def test_message_round_trip():
    msg = make_message("ACK", {"ack_of": "TEST", "digest16": 42}, seq=1)
    raw = msg.to_json()
    recovered = Msg.from_json(raw)
    assert recovered.type == msg.type
    assert recovered.payload == msg.payload
    assert recovered.crc16 == msg.crc16


def test_crc_mismatch():
    msg = make_message("ACK", {"ack_of": "TEST", "digest16": 42}, seq=1)
    raw = json.loads(msg.to_json())
    raw["crc16"] ^= 1
    with pytest.raises(MessageError):
        Msg.from_json(json.dumps(raw))
