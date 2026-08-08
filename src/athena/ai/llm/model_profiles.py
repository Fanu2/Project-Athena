"""
Default Athena model profiles.
"""

from __future__ import annotations

from athena.ai.llm.model_profile import ModelProfile


DEFAULT_MODEL_PROFILES = [
    ModelProfile(
        name="default-chat",
        capability="chat",
        model_name="qwen3:4b",
    ),
    ModelProfile(
        name="default-vision",
        capability="vision",
        model_name="llava",
    ),
    ModelProfile(
        name="default-embedding",
        capability="embedding",
        model_name="nomic-embed-text",
    ),
]