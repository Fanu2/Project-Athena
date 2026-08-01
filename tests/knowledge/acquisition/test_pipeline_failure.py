"""
Pipeline failure handling tests.

Validates that AKC captures failed stages
correctly.
"""

import pytest

from athena.knowledge.acquisition.engine.pass_manager import (
    PassManager,
)

from athena.knowledge.acquisition.exceptions.exceptions import (
    PipelineExecutionError,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.contracts.pipeline_stage import (
    PipelineStage,
)


class FailingStage(PipelineStage):
    """
    Test stage that always fails.
    """

    @property
    def name(self) -> str:
        return "failing_stage"

    def execute(
        self,
        context: KnowledgeContext,
        input_data,
    ):
        raise ValueError(
            "intentional failure"
        )


def test_pipeline_failure_is_wrapped():

    manager = PassManager()

    manager.register(
        FailingStage()
    )

    context = KnowledgeContext()

    with pytest.raises(
        PipelineExecutionError
    ) as error:

        manager.execute(
            context,
            "test",
        )

    assert (
        error.value.stage_name
        == "failing_stage"
    )

    assert (
        "intentional failure"
        in error.value.message
    )


def test_failed_stage_record_created():

    manager = PassManager()

    manager.register(
        FailingStage()
    )

    context = KnowledgeContext()

    try:

        manager.execute(
            context,
            "test",
        )

    except PipelineExecutionError:
        pass

    assert len(
        manager.execution_records
    ) == 1

    record = (
        manager.execution_records[0]
    )

    assert (
        record.status
        == "failed"
    )

    assert (
        record.stage_name
        == "failing_stage"
    )