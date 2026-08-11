"""
Assistant execution boundary models.

Defines the interface between
planning and future execution.
"""

from __future__ import annotations

from dataclasses import dataclass

from .plan import AssistantPlan


@dataclass(frozen=True, slots=True)
class AssistantExecutionRequest:
    """
    Request to execute an assistant plan.

    Execution is intentionally not implemented.
    """

    plan: AssistantPlan


@dataclass(frozen=True, slots=True)
class AssistantExecutionResult:
    """
    Result returned by future executors.
    """

    success: bool

    message: str
