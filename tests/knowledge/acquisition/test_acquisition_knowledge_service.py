"""
Knowledge service tests.
"""

from athena.knowledge.services.knowledge_service import (
    KnowledgeService,
)

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


def test_knowledge_service_save_and_get():

    repository = (
        MemoryKnowledgeRepository()
    )

    service = KnowledgeService(
        repository
    )

    obj = KnowledgeObject(
        object_type="document",
        title="Athena Service Test",
    )

    service.save(
        obj
    )

    result = service.get(
        obj.object_id
    )

    assert result is not None

    assert (
        result.title
        == "Athena Service Test"
    )


def test_knowledge_service_list():

    repository = (
        MemoryKnowledgeRepository()
    )

    service = KnowledgeService(
        repository
    )

    service.save(
        KnowledgeObject(
            object_type="document"
        )
    )

    assert len(
        service.list_all()
    ) == 1