"""
SQLite knowledge repository tests.
"""

from athena.knowledge.repositories.sqlite_knowledge_repository import (
    SQLiteKnowledgeRepository,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


def test_sqlite_knowledge_repository(
    tmp_path,
):

    database = (
        tmp_path / "athena.db"
    )

    repository = SQLiteKnowledgeRepository(
        str(database)
    )

    knowledge = KnowledgeObject(
        object_type="document",
        title="Athena Demo",
        confidence=0.9,
    )

    repository.save(
        knowledge
    )

    result = (
        repository.list_all()
    )

    assert len(result) == 1

    assert (
        result[0].title
        == "Athena Demo"
    )

    loaded = (
        repository.get(
            knowledge.object_id
        )
    )

    assert loaded is not None

    assert (
        loaded.title
        == "Athena Demo"
    )