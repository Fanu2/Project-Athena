"""
Provider metadata model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProviderMetadata:
    """Describes an LLM provider."""

    name: str

    display_name: str

    local: bool

    requires_api_key: bool

    supports_chat: bool

    supports_streaming: bool

    supports_tools: bool

    supports_vision: bool
