"""
Assistant execution boundary.

Defines controlled execution interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .execution import (
    AssistantExecutionRequest,
)

from .execution import (
    AssistantExecutionResult,
)


class AssistantExecutor(ABC):
    """
    Boundary for future assistant executors.
    """

    @abstractmethod
    def execute(
        self,
        request: AssistantExecutionRequest,
    ) -> AssistantExecutionResult:
        """
        Execute an assistant plan.

        Implementations must provide
        controlled execution.
        """
        raise NotImplementedError


class DisabledAssistantExecutor(
    AssistantExecutor,
):
    """
    Default executor.

    Execution intentionally disabled.
    """

    def execute(
        self,
        request: AssistantExecutionRequest,
    ) -> AssistantExecutionResult:

        return AssistantExecutionResult(
            success=False,
            message=(
                "Assistant execution is "
                "not enabled"
            ),
        )
