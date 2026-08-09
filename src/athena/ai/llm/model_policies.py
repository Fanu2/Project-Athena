"""
Default Athena model policies.
"""

from __future__ import annotations

from athena.ai.llm.model_policy import ModelPolicy


FAST_CHAT_POLICY = ModelPolicy(
    name="fast-chat",
    prefer_local=True,
    latency_priority=True,
    quality_priority=False,
)


DEEP_REASONING_POLICY = ModelPolicy(
    name="deep-reasoning",
    prefer_local=True,
    require_reasoning=True,
    quality_priority=True,
)


OFFLINE_PRIVATE_POLICY = ModelPolicy(
    name="offline-private",
    prefer_local=True,
    quality_priority=True,
)