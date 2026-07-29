from athena.knowledge.application.knowledge_note_service import KnowledgeNoteService
from athena.knowledge.infrastructure.sqlite_repository import SQLiteKnowledgeNoteRepository


def test_service_with_sqlite_repository(tmp_path):
    db_path = tmp_path / "knowledge.db"

    repository = SQLiteKnowledgeNoteRepository(db_path)
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Athena",
        markdown="# Hello"
    )

    service.rename_note(note.id, "Athena v2")
    service.favorite_note(note.id)
    service.archive_note(note.id)

    loaded = service.get_note(note.id)

    assert loaded.title == "Athena v2"
    assert loaded.favorite is True
    assert loaded.archived is True
