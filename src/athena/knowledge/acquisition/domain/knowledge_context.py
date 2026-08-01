"""
Athena Knowledge Context

Runtime context shared across Knowledge Compiler stages.

Contains:
- compilation metadata
- runtime services
- provider selection
- execution options
- workspace information
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class KnowledgeContext:
    """
    Runtime context for AKC execution.
    """

    context_id: UUID = field(
        default_factory=uuid4
    )

    pipeline_name: Optional[str] = None

    workspace: Optional[Any] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    options: Dict[str, Any] = field(
        default_factory=dict
    )

    services: Dict[str, Any] = field(
        default_factory=dict
    )

    provider_preferences: Dict[str, str] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda:
            datetime.now(timezone.utc)
    )

    def add_service(
        self,
        name: str,
        service: Any,
    ) -> None:
        """
        Register runtime service.
        """

        self.services[name] = service

    def get_service(
        self,
        name: str,
    ) -> Optional[Any]:
        """
        Retrieve runtime service.
        """

        return self.services.get(
            name
        )

    def has_service(
        self,
        name: str,
    ) -> bool:
        """
        Check service availability.
        """

        return name in self.services

    def set_option(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set compiler option.
        """

        self.options[key] = value

    def get_option(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve compiler option.
        """

        return self.options.get(
            key,
            default,
        )

    def set_provider(
        self,
        capability: str,
        provider: str,
    ) -> None:
        """
        Select provider for capability.

        Example:
            pdf_parser -> docling
        """

        self.provider_preferences[capability] = provider


    def get_provider(
        self,
        capability: str,
    ) -> Optional[str]:
        """
        Return provider for capability.
        """

        return self.provider_preferences.get(
            capability
        )

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add context metadata.
        """

        self.metadata[key] = value

    def get_metadata(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve metadata.
        """

        return self.metadata.get(
            key,
            default,
        )