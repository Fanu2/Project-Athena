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
                f"Model does not support capability: {request.capability}"
            )

        return model

    def _select_model(
        self,
        request: RuntimeRequest,
    ) -> ModelInfo:
        """Select model without capability validation."""

        if request.preferred_model is not None:
            if self._models.has_model(
                request.preferred_model
            ):
                return self._models.get_model(
                    request.preferred_model
                )

            if not request.allow_fallback:
                raise ValueError(
                    f"Requested model unavailable: {request.preferred_model}"
                )

        return self._models.active_model()
