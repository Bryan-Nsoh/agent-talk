from __future__ import annotations

import pytest

from agent_talk.core.protocol import ConversationLimits, ProtocolError, enforce_message_size
from agent_talk.core.messages import make_message


def test_message_size_limit():
    limits = ConversationLimits(max_bytes_per_message=20)
    msg = make_message("HELLO", {"pad": "x" * 50}, seq=0)
    with pytest.raises(ProtocolError):
        enforce_message_size(msg.to_json(), limits)


def test_sequence_increasing():
    msg1 = make_message("HELLO", {}, seq=0)
    msg2 = make_message("HELLO", {}, seq=1)
    assert msg2.seq > msg1.seq
