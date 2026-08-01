"""
Knowledge repository contract tests.
"""

from athena.knowledge.repositories.knowledge_repository import (
    KnowledgeRepository,
)


def test_repository_contract_exists():

    assert KnowledgeRepository is not None