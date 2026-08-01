from athena.knowledge.acquisition.indexers.knowledge_indexer import (
    KnowledgeIndexer,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


class FakeIndexingService:

    def __init__(self):
        self.path = None

    def index_document(
        self,
        path,
    ):
        self.path = path
        return []


def test_knowledge_indexer_uses_source_path():

    service = FakeIndexingService()

    indexer = KnowledgeIndexer(
        service
    )

    knowledge = KnowledgeObject(
        title="Athena"
    )

    knowledge.metadata[
        "source_path"
    ] = "document.pdf"

    indexer.index(
        knowledge
    )

    assert (
        str(service.path)
        == "document.pdf"
    )