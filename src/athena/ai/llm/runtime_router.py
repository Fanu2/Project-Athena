"""
Runtime router for Athena LLM execution.
"""

from __future__ import annotations

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_manager import ModelManager
from athena.ai.llm.model_validator import ModelValidator
from athena.ai.llm.runtime_request import RuntimeRequest


class RuntimeRouter:
    """Route runtime requests to models."""

    def __init__(
        self,
        model_manager: ModelManager | None = None,
        validator: ModelValidator | None = None,
    ) -> None:
        """Initialize router."""

        self._models = (
            model_manager
            if model_manager is not None
            else ModelManager()
        )

        self._validator = (
            validator
            if validator is not None
            else ModelValidator()
        )

    def route(
        self,
        request: RuntimeRequest,
    ) -> ModelInfo:
        """Select compatible model for request."""

        model = self._select_model(request)

        metadata = self._models.provider_metadata(model)

        if not self._validator.validate_capability(
            model,
            metadata,
            request.capability,
        ):
            raise ValueError(
                f"Model does not support capability: "
                f"{request.capability}"
            )

        return model

    def _select_model(
        self,
        request: RuntimeRequest,
    ) -> ModelInfo:
        """Select model using capability-aware routing."""

        # Explicit model selection always wins.
        # Capability validation happens in route().
        if request.preferred_model is not None:
            if self._models.has_model(
                request.preferred_model
            ):
                return self._models.get_model(
                    request.preferred_model
                )

            if not request.allow_fallback:
                raise ValueError(
                    f"Requested model unavailable: "
                    f"{request.preferred_model}"
                )

        # Prefer active model if compatible.
        active = self._models.active_model()

        if self._supports_capability(
            active,
            request.capability,
        ):
            return active

        # Discover compatible fallback models.
        if request.allow_fallback:
            candidates = self._models.models_by_capability(
                request.capability
            )

            if candidates:
                return candidates[-1]

        return active

    def _supports_capability(
        self,
        model: ModelInfo,
        capability: str,
    ) -> bool:
        """Return whether model supports capability."""

        capability_map = {
            "chat": model.capabilities.chat,
            "streaming": model.capabilities.streaming,
            "tools": model.capabilities.tools,
            "vision": model.capabilities.vision,
            "embedding": model.capabilities.embeddings,
            "reasoning": model.capabilities.reasoning,
            "reranking": model.capabilities.reranking,
        }

        if capability not in capability_map:
            return False

        return capability_map[capability]