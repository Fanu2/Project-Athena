"""
LLM execution service.
"""

from __future__ import annotations

from athena.ai.llm.execution_error import (
    ExecutionFailedError,
    ExecutionUnavailableError,
)
from athena.ai.llm.exceptions import (
    GenerationError,
    ProviderUnavailableError,
)
from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)
from athena.ai.llm.provider_factory import ProviderFactory
from athena.ai.llm.runtime_router import RuntimeRouter
from athena.ai.llm.runtime_request import RuntimeRequest


class ExecutionService:
    """Execute LLM requests through routed providers."""

    def __init__(
        self,
        router: RuntimeRouter | None = None,
        factory: ProviderFactory | None = None,
    ) -> None:
        """Initialize execution service."""

        self._router = (
            router
            if router is not None
            else RuntimeRouter()
        )

        self._factory = (
            factory
            if factory is not None
            else ProviderFactory()
        )

    def execute(
        self,
        runtime_request: RuntimeRequest,
        request: LLMRequest,
    ) -> LLMResponse:
        """Execute request using selected model."""

        model = self._router.route(
            runtime_request
        )

        provider = self._factory.create(
            model.provider
        )

        try:
            return provider.analyze(request)

        except ProviderUnavailableError as exc:
            raise ExecutionUnavailableError(
                "LLM provider unavailable."
            ) from exc

        except GenerationError as exc:
            raise ExecutionFailedError(
                "LLM execution failed."
            ) from exc
