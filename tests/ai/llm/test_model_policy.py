"""
Tests for model policies.
"""

from athena.ai.llm.model_policies import (
    DEEP_REASONING_POLICY,
    FAST_CHAT_POLICY,
)


def test_fast_policy_prefers_latency() -> None:
    assert FAST_CHAT_POLICY.latency_priority


def test_reasoning_policy_requires_quality() -> None:
    assert DEEP_REASONING_POLICY.require_reasoning