"""
Tests for controlled assistant executor.
"""

from athena.application.assistant.action import (
    AssistantAction,
)

from athena.application.assistant.controlled_executor import (
    ControlledAssistantExecutor,
)

from athena.application.assistant.execution import (
    AssistantExecutionRequest,
)

from athena.application.assistant.plan import (
    AssistantPlan,
)


class FakeQueryService:
    """
    Minimal query service test double.
    """

    def __init__(self) -> None:
        self.questions = []

    def answer(
        self,
        question: str,
    ):
        self.questions.append(
            question,
        )

        return question


class FakeRetrievalAdapter:
    """
    Minimal retrieval adapter test double.
    """

    def __init__(self) -> None:
        self.queries = []

    def retrieve(
        self,
        query: str,
    ):
        self.queries.append(
            query,
        )

        return [
            "result",
        ]


def create_executor():

    query_service = FakeQueryService()

    retrieval_adapter = FakeRetrievalAdapter()

    executor = ControlledAssistantExecutor(
        query_service,
        retrieval_adapter,
    )

    return (
        executor,
        query_service,
        retrieval_adapter,
    )


def test_executor_executes_response_action():

    (
        executor,
        query_service,
        _,
    ) = create_executor()

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "generate_response",
        ),
        context_notes=(
            "Query: test question",
        ),
        actions=(
            AssistantAction(
                name="generate_response",
                description="Generate response",
            ),
        ),
    )

    result = executor.execute(
        AssistantExecutionRequest(
            plan=plan,
        )
    )

    assert result.success is True
    assert (
        query_service.questions
        ==
        [
            "test question",
        ]
    )


def test_executor_executes_retrieval_action():

    (
        executor,
        _,
        retrieval_adapter,
    ) = create_executor()

    plan = AssistantPlan(
        capability="retrieval",
        steps=(
            "retrieve_information",
        ),
        context_notes=(
            "Query: find documents",
        ),
        actions=(
            AssistantAction(
                name="retrieve_information",
                description="Search workspace documents",
            ),
        ),
    )

    result = executor.execute(
        AssistantExecutionRequest(
            plan=plan,
        )
    )

    assert result.success is True
    assert (
        retrieval_adapter.queries
        ==
        [
            "find documents",
        ]
    )


def test_executor_rejects_unknown_action():

    (
        executor,
        _,
        _,
    ) = create_executor()

    plan = AssistantPlan(
        capability="unknown",
        steps=(),
        actions=(
            AssistantAction(
                name="unknown_action",
                description="Unknown action",
            ),
        ),
    )

    result = executor.execute(
        AssistantExecutionRequest(
            plan=plan,
        )
    )

    assert result.success is False
    assert (
        "Unsupported action"
        in result.message
    )


def test_executor_blocks_confirmation_action():

    (
        executor,
        _,
        _,
    ) = create_executor()

    plan = AssistantPlan(
        capability="test",
        steps=(),
        actions=(
            AssistantAction(
                name="generate_response",
                description="Generate response",
                requires_confirmation=True,
            ),
        ),
    )

    result = executor.execute(
        AssistantExecutionRequest(
            plan=plan,
        )
    )

    assert result.success is False
    assert (
        "requires confirmation"
        in result.message
    )