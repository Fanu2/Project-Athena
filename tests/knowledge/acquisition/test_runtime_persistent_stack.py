"""
Persistent runtime stack tests.
"""

from athena.knowledge.acquisition.runtime.knowledge_runtime_factory import (
    KnowledgeRuntimeFactory,
)


def test_runtime_factory_registers_persistence_stack():

    factory = KnowledgeRuntimeFactory(
        knowledge_repository="knowledge-db",
        evidence_repository="evidence-db",
        citation_repository="citation-db",
    )

    context = (
        factory.create_context()
    )

    assert (
        context.get_service(
            "knowledge_repository"
        )
        == "knowledge-db"
    )

    assert (
        context.get_service(
            "evidence_repository"
        )
        == "evidence-db"
    )

    assert (
        context.get_service(
            "citation_repository"
        )
        == "citation-db"
    )