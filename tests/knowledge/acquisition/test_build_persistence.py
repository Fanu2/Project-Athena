"""
BuildPass persistence integration test.
"""

from athena.knowledge.acquisition.pipeline.build_pass import (
    BuildPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.domain.knowledge_candidate import (
    KnowledgeCandidate,
)

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)


def test_build_pass_persists_objects():

    repository = MemoryKnowledgeRepository()

    context = KnowledgeContext()

    context.add_service(
        "knowledge_repository",
        repository,
    )

    candidate = KnowledgeCandidate(
        candidate_type="document",
        value="Athena Knowledge",
        confidence=0.9,
    )

    result = BuildPass().execute(
        context,
        [candidate],
    )

    assert len(result) == 1

    stored = repository.list_all()

    assert len(stored) == 1

    assert (
        stored[0].title
        == "Athena Knowledge"
    )