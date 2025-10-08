from __future__ import annotations

from agent_talk.agents import AgentA, AgentB, AgentConfig
from agent_talk.core.protocol import ConversationLimits
from agent_talk.env.grid import Grid
from agent_talk.oracle.oracle import union_grid, verify_path_cert, verify_cut_cert
from agent_talk.runners import simulate_conversation


def make_config(mask, allow_path=True, allow_cut=True):
    return AgentConfig(
        name="test",
        height=3,
        width=3,
        start=(0, 0),
        goal=(2, 0),
        private_mask=mask,
        max_path_attempts=3,
        max_path_length=16,
        allow_path=allow_path,
        allow_cut=allow_cut,
    )


def test_agents_reachable_path_certificate():
    mask_free = [0] * 9
    config_a = make_config(mask_free)
    config_b = make_config(mask_free)
    agent_a = AgentA(config_a)
    agent_b = AgentB(config_b)
    result = simulate_conversation(agent_a, agent_b, ConversationLimits())
    assert result.outcome == "DONE"
    assert result.certificate_type == "PATH_CERT"
    grid = union_grid(Grid.from_flat(3, 3, mask_free), Grid.from_flat(3, 3, mask_free))
    assert verify_path_cert(result.certificate_payload, grid, (0, 0), (2, 0))


def test_agents_unreachable_cut_certificate():
    mask_a = [0] * 9
    mask_b = [0, 1, 0,
              0, 1, 0,
              0, 1, 0]
    config_a = make_config(mask_a)
    config_b = make_config(mask_b)
    agent_a = AgentA(config_a)
    agent_b = AgentB(config_b)
    result = simulate_conversation(agent_a, agent_b, ConversationLimits(max_rounds=50))
    assert result.certificate_type == "CUT_CERT"
    grid = union_grid(Grid.from_flat(3, 3, mask_a), Grid.from_flat(3, 3, mask_b))
    assert verify_cut_cert(result.certificate_payload, grid, (0, 0), (2, 0))
