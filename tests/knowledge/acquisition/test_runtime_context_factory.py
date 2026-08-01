"""
Knowledge runtime factory tests.
"""

from athena.knowledge.acquisition.runtime.knowledge_runtime_factory import (
    KnowledgeRuntimeFactory,
)


def test_runtime_factory_creates_context():

    provider = object()

    repository = object()

    factory = (
        KnowledgeRuntimeFactory(
            provider_manager=provider,
            knowledge_repository=repository,
        )
    )

    context = (
        factory.create_context()
    )

    assert (
        context.get_service(
            "provider_manager"
        )
        == provider
    )

    assert (
        context.get_service(
            "knowledge_repository"
        )
        == repository
    )