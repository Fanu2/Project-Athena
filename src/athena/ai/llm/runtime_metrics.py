"""
Runtime metrics model for Athena LLM execution.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeMetric:
    """Execution metric for an LLM model."""

    model: str

    provider: str

    latency_ms: float

    success: bool = True

    tokens_used: int = 0

    error: str | None = None

    @property
    def failure(self) -> bool:
        """Return whether execution failed."""

        return not self.success