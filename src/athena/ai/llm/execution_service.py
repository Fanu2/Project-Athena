"""
LLM execution service.
"""

from __future__ import annotations

from athena.ai.llm.context import ContextBuilder
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
from athena.ai.llm.session import LLMSession


class ExecutionService:
    """Execute LLM requests through routed providers."""

    def __init__(
        self,
        router: RuntimeRouter | None = None,
        factory: ProviderFactory | None = None,
        context_builder: ContextBuilder | None = None,
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

        self._context = (
            context_builder
            if context_builder is not None
            else ContextBuilder()
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

    def execute_session(
        self,
        runtime_request: RuntimeRequest,
        session: LLMSession,
        user_prompt: str,
    ) -> LLMResponse:
        """Execute request using conversation session."""

        request = self._context.build_request(
            session,
            user_prompt,
        )

        return self.execute(
            runtime_request,
            request,
        )
