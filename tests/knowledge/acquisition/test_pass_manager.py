from athena.knowledge.acquisition.engine.pass_manager import (
    PassManager,
)

from athena.knowledge.acquisition.contracts.pipeline_stage import (
    PipelineStage,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


class IncrementStage(PipelineStage):

    @property
    def name(self):
        return "increment"

    def execute(self, context, data):
        return data + 1


def test_register_stage():

    manager = PassManager()

    manager.register(
        IncrementStage()
    )

    assert len(manager.stages) == 1


def test_execute_stages():

    manager = PassManager()

    manager.register(
        IncrementStage()
    )

    manager.register(
        IncrementStage()
    )

    result = manager.execute(
        KnowledgeContext(),
        0,
    )

    assert result == 2