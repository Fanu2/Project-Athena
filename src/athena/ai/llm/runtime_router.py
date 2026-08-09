"""
Runtime router for Athena LLM execution.
"""

from __future__ import annotations

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_manager import ModelManager
from athena.ai.llm.model_scorer import ModelScoringService
from athena.ai.llm.model_validator import ModelValidator
from athena.ai.llm.runtime_request import RuntimeRequest
from athena.ai.providers.health_status import HealthStatus
from athena.ai.providers.provider_health import ProviderHealth
from athena.ai.providers.provider_health_service import (
    ProviderHealthService,
)


class RuntimeRouter:
    """Route runtime requests to models."""

    def __init__(
        self,
        model_manager: ModelManager | None = None,
        validator: ModelValidator | None = None,
        health_service: ProviderHealthService | None = None,
        scorer: ModelScoringService | None = None,
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

        self._health_service = (
            health_service
            if health_service is not None
            else ProviderHealthService()
        )

        self._scorer = (
            scorer
            if scorer is not None
            else ModelScoringService()
        )

    def route(
        self,
        request: RuntimeRequest,
    ) -> ModelInfo:
        """Select compatible model for request."""

        model = self._select_model(
            request,
        )

        metadata = self._models.provider_metadata(
            model,
        )

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

    def get_provider_health(
        self,
    ) -> list[ProviderHealth]:
        """Return health information for providers."""

        health: list[ProviderHealth] = []

        for model in self._models.models():
            health.append(
                self._health_service.check_provider(
                    provider_id=model.provider,
                    model=model.name,
                    capabilities=self._capabilities(
                        model,
                    ),
                )
            )

        return health

    def _select_model(
        self,
        request: RuntimeRequest,
    ) -> ModelInfo:
        """Select model using routing intelligence."""

        if request.preferred_model is not None:
            if self._models.has_model(
                request.preferred_model,
            ):
                return self._models.get_model(
                    request.preferred_model,
                )

            if not request.allow_fallback:
                raise ValueError(
                    f"Requested model unavailable: "
                    f"{request.preferred_model}"
                )

        if request.allow_fallback:
            candidates = self._models.models_by_capability(
                request.capability,
            )

            if candidates:
                healthy = (
                    self._filter_healthy_candidates(
                        candidates,
                    )
                )

                if healthy:
                    return self._rank_candidates(
                        healthy,
                    )[0]

                return self._rank_candidates(
                    candidates,
                )[0]

        return self._models.active_model()

    def _filter_healthy_candidates(
        self,
        candidates: list[ModelInfo],
    ) -> list[ModelInfo]:
        """Return only online candidates."""

        healthy: list[ModelInfo] = []

        for model in candidates:
            health = self._health_service.check_provider(
                provider_id=model.provider,
                model=model.name,
                capabilities=self._capabilities(
                    model,
                ),
            )

            if health.status == HealthStatus.ONLINE:
                healthy.append(model)

        return healthy

    def _rank_candidates(
        self,
        candidates: list[ModelInfo],
    ) -> list[ModelInfo]:
        """Rank candidates using scoring service."""

        return self._scorer.rank(
            candidates,
        )

    def _capabilities(
        self,
        model: ModelInfo,
    ) -> tuple[str, ...]:
        """Return enabled model capabilities."""

        return tuple(
            capability
            for capability, enabled in {
                "chat": model.capabilities.chat,
                "streaming": model.capabilities.streaming,
                "tools": model.capabilities.tools,
                "vision": model.capabilities.vision,
                "embedding": model.capabilities.embeddings,
                "reasoning": model.capabilities.reasoning,
                "reranking": model.capabilities.reranking,
            }.items()
            if enabled
        )

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