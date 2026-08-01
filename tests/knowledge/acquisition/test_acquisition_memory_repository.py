"""
Memory repository tests.
"""

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


def test_memory_repository_save_and_get():

    repository = (
        MemoryKnowledgeRepository()
    )

    obj = KnowledgeObject(
        object_type="document",
        title="Athena Test",
    )

    repository.save(
        obj
    )

    result = repository.get(
        obj.object_id
    )

    assert result == obj


def test_memory_repository_list():

    repository = (
        MemoryKnowledgeRepository()
    )

    repository.save(
        KnowledgeObject(
            object_type="document"
        )
    )

    assert len(
        repository.list_all()
    ) == 1