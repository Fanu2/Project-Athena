from athena.knowledge.acquisition.pipeline.index_pass import (
    IndexPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


class FakeIndexer:

    def __init__(self):
        self.called = 0

    def index(
        self,
        knowledge,
    ):
        self.called += 1


def test_index_pass_uses_indexer():

    context = KnowledgeContext()

    indexer = FakeIndexer()

    context.add_service(
        "knowledge_indexer",
        indexer,
    )

    objects = [
        KnowledgeObject(
            title="Athena"
        )
    ]

    result = IndexPass().execute(
        context,
        objects,
    )

    assert len(result) == 1

    assert indexer.called == 1