"""
Tests for ModelScoringService.
"""

from __future__ import annotations

from athena.ai.llm.capabilities import ModelCapabilities
from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_policies import (
    DEEP_REASONING_POLICY,
)
from athena.ai.llm.model_scorer import ModelScoringService
from athena.ai.llm.runtime_metrics import RuntimeMetric
from athena.ai.llm.runtime_metrics_store import (
    RuntimeMetricsStore,
)


def test_reasoning_model_scores_higher() -> None:
    scorer = ModelScoringService()

    basic = ModelInfo(
        name="basic",
        provider="ollama",
        capabilities=ModelCapabilities(
            chat=True,
            local=True,
        ),
    )

    reasoning = ModelInfo(
        name="reasoning",
        provider="ollama",
        capabilities=ModelCapabilities(
            chat=True,
            reasoning=True,
            local=True,
        ),
    )

    assert (
        scorer.score(reasoning).total
        >
        scorer.score(basic).total
    )


def test_best_model_selection() -> None:
    scorer = ModelScoringService()

    models = [
        ModelInfo(
            name="basic",
            provider="ollama",
            capabilities=ModelCapabilities(
                chat=True,
            ),
        ),
        ModelInfo(
            name="reasoning",
            provider="ollama",
            capabilities=ModelCapabilities(
                chat=True,
                reasoning=True,
            ),
        ),
    ]

    result = scorer.best(
        models,
    )

    assert result.name == "reasoning"


def test_runtime_metrics_improve_score() -> None:
    store = RuntimeMetricsStore()

    store.record(
        RuntimeMetric(
            model="fast-model",
            provider="ollama",
            latency_ms=100.0,
            success=True,
        )
    )

    store.record(
        RuntimeMetric(
            model="fast-model",
            provider="ollama",
            latency_ms=120.0,
            success=True,
        )
    )

    scorer = ModelScoringService(
        metrics_store=store,
    )

    model = ModelInfo(
        name="fast-model",
        provider="ollama",
        capabilities=ModelCapabilities(
            chat=True,
        ),
    )

    assert (
        scorer.score(model).total
        >
        60.0
    )


def test_failed_runtime_metrics_reduce_advantage() -> None:
    store = RuntimeMetricsStore()

    store.record(
        RuntimeMetric(
            model="unstable-model",
            provider="ollama",
            latency_ms=800.0,
            success=False,
        )
    )

    scorer = ModelScoringService(
        metrics_store=store,
    )

    model = ModelInfo(
        name="unstable-model",
        provider="ollama",
        capabilities=ModelCapabilities(
            chat=True,
        ),
    )

    assert (
        scorer.score(model).health_score
        <
        5.0
    )


def test_policy_increases_reasoning_score() -> None:
    scorer = ModelScoringService()

    model = ModelInfo(
        name="reasoning",
        provider="ollama",
        capabilities=ModelCapabilities(
            chat=True,
            reasoning=True,
            local=True,
        ),
    )

    normal_score = scorer.score(
        model,
    )

    policy_score = scorer.score(
        model,
        DEEP_REASONING_POLICY,
    )

    assert (
        policy_score.total
        >
        normal_score.total
    )