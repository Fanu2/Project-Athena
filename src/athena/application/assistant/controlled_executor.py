"""
Controlled assistant executor.

Executes only approved assistant actions
through existing Athena service boundaries.

No autonomous execution is performed.
"""

from __future__ import annotations

from athena.services.athena_query_service import (
    AthenaQueryService,
)

from .execution import (
    AssistantExecutionRequest,
    AssistantExecutionResult,
)

from .executor import (
    AssistantExecutor,
)

from .retrieval_adapter import (
    AssistantRetrievalAdapter,
)


class ControlledAssistantExecutor(
    AssistantExecutor,
):
    """
    Controlled executor implementation.

    Maps approved assistant actions to
    existing Athena application services.

    Execution is explicit and bounded.
    """


    def __init__(
        self,
        query_service: AthenaQueryService,
        retrieval_adapter: AssistantRetrievalAdapter,
    ) -> None:

        self._query_service = (
            query_service
        )

        self._retrieval_adapter = (
            retrieval_adapter
        )


    def execute(
        self,
        request: AssistantExecutionRequest,
    ) -> AssistantExecutionResult:
        """
        Execute approved assistant actions.

        Unknown actions are rejected.
        """

        if not request.plan.actions:

            return AssistantExecutionResult(
                success=False,
                message=(
                    "No executable actions found"
                ),
            )

        for action in request.plan.actions:

            if action.requires_confirmation:

                return AssistantExecutionResult(
                    success=False,
                    message=(
                        "Action requires confirmation: "
                        f"{action.name}"
                    ),
                )

            if action.name == (
                "retrieve_information"
            ):

                return self._execute_retrieval(
                    request,
                )

            if action.name == (
                "generate_response"
            ):

                return self._execute_response(
                    request,
                )

            return AssistantExecutionResult(
                success=False,
                message=(
                    "Unsupported action: "
                    f"{action.name}"
                ),
            )

        return AssistantExecutionResult(
            success=False,
            message=(
                "No supported actions executed"
            ),
        )


    def _execute_retrieval(
        self,
        request: AssistantExecutionRequest,
    ) -> AssistantExecutionResult:
        """
        Execute retrieval through the
        existing retrieval boundary.
        """

        results = (
            self._retrieval_adapter.retrieve(
                self._extract_query(request),
            )
        )

        return AssistantExecutionResult(
            success=True,
            message=(
                f"Retrieved {len(results)} "
                "results successfully"
            ),
        )


    def _execute_response(
        self,
        request: AssistantExecutionRequest,
    ) -> AssistantExecutionResult:
        """
        Execute response generation.

        Uses existing AthenaQueryService
        application boundary.
        """

        self._query_service.answer(
            self._extract_query(request),
        )

        return AssistantExecutionResult(
            success=True,
            message=(
                "Response generated successfully"
            ),
        )


    def _extract_query(
        self,
        request: AssistantExecutionRequest,
    ) -> str:
        """
        Extract original query from plan context.

        Future execution requests may carry
        richer structured context.
        """

        for note in request.plan.context_notes:

            if note.startswith(
                "Query:",
            ):

                return note.removeprefix(
                    "Query:",
                ).strip()

        return ""