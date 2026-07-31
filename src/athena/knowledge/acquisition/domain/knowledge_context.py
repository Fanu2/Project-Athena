"""
Athena Knowledge Context

Runtime context passed through the knowledge
compilation pipeline.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeContext:
    """
    Execution context for Athena knowledge processing.

    Carries runtime configuration without
    relying on global state.
    """

    context_id: UUID = field(default_factory=uuid4)

    workspace: Optional[str] = None

    pipeline_name: Optional[str] = None

    options: Dict[str, Any] = field(default_factory=dict)

    provider_preferences: Dict[str, str] = field(
        default_factory=dict
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def set_option(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set pipeline option.
        """
        self.options[key] = value

    def set_provider(
        self,
        capability: str,
        provider: str,
    ) -> None:
        """
        Set preferred provider for a capability.
        """
        self.provider_preferences[capability] = provider