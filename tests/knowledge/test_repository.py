from athena.knowledge.domain import KnowledgeNote
from athena.knowledge.domain.repository import KnowledgeNoteRepository


def test_repository_is_abstract():
    assert hasattr(KnowledgeNoteRepository, "save")
    assert hasattr(KnowledgeNoteRepository, "get")
    assert hasattr(KnowledgeNoteRepository, "delete")
    assert hasattr(KnowledgeNoteRepository, "list_all")
