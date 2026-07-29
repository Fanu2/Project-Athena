"""
Model registry for Athena LLM models.
"""

from __future__ import annotations

from athena.ai.llm.model_info import ModelInfo


class ModelRegistry:
    """Registry of available LLM models."""

    def __init__(self) -> None:
        """Initialize registry."""

        self._models: dict[str, ModelInfo] = {}
        self._active: str | None = None

    def register(
        self,
        model: ModelInfo,
    ) -> None:
        """Register a model."""

        if model.name in self._models:
            raise ValueError(
                f"Model '{model.name}' already registered."
            )

        self._models[model.name] = model

        if self._active is None:
            self._active = model.name

    def unregister(
        self,
        name: str,
    ) -> None:
        """Remove a model."""

        if name not in self._models:
            raise KeyError(name)

        del self._models[name]

        if self._active == name:
            self._active = (
                next(iter(self._models))
                if self._models
                else None
            )

    def get(
        self,
        name: str,
    ) -> ModelInfo:
        """Return model."""

        return self._models[name]

    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether model exists."""

        return name in self._models

    def models(self) -> list[ModelInfo]:
        """Return all models."""

        return list(self._models.values())

    def by_provider(
        self,
        provider: str,
    ) -> list[ModelInfo]:
        """Return models for provider."""

        return [
            model
            for model in self._models.values()
            if model.provider == provider
        ]

    def set_active(
        self,
        name: str,
    ) -> None:
        """Set active model."""

        if name not in self._models:
            raise KeyError(name)

        self._active = name

    def active(self) -> ModelInfo:
        """Return active model."""

        if self._active is None:
            raise RuntimeError(
                "No active model configured."
            )

        return self._models[self._active]
