from athena.knowledge.domain import KnowledgeNote
from athena.knowledge.infrastructure.sqlite_repository import SQLiteKnowledgeNoteRepository


def test_save_and_get_note(tmp_path):
    db_path = tmp_path / "knowledge.db"

    repository = SQLiteKnowledgeNoteRepository(db_path)

    note = KnowledgeNote(
        title="Athena",
        markdown="# Hello"
    )

    repository.save(note)

    loaded = repository.get(note.id)

    assert loaded is not None
    assert loaded.id == note.id
    assert loaded.title == "Athena"

def test_list_all_notes(tmp_path):
    db_path = tmp_path / "knowledge.db"

    repository = SQLiteKnowledgeNoteRepository(db_path)

    repository.save(
        KnowledgeNote(
            title="One",
            markdown="A"
        )
    )

    repository.save(
        KnowledgeNote(
            title="Two",
            markdown="B"
        )
    )

    notes = repository.list_all()

    assert len(notes) == 2
    assert notes[0].title == "One"
    assert notes[1].title == "Two"

def test_list_all_notes(tmp_path):
    db_path = tmp_path / "knowledge.db"

    repository = SQLiteKnowledgeNoteRepository(db_path)

    repository.save(
        KnowledgeNote(
            title="One",
            markdown="A"
        )
    )

    repository.save(
        KnowledgeNote(
            title="Two",
            markdown="B"
        )
    )

    notes = repository.list_all()

    assert len(notes) == 2
    assert notes[0].title == "One"
    assert notes[1].title == "Two"

def test_delete_note(tmp_path):
    db_path = tmp_path / "knowledge.db"

    repository = SQLiteKnowledgeNoteRepository(db_path)

    note = KnowledgeNote(
        title="Athena",
        markdown="# Hello"
    )

    repository.save(note)

    repository.delete(note.id)

    assert repository.get(note.id) is None

def test_update_existing_note(tmp_path):
    db_path = tmp_path / "knowledge.db"

    repository = SQLiteKnowledgeNoteRepository(db_path)

    note = KnowledgeNote(
        title="Old",
        markdown="Hello"
    )

    repository.save(note)

    note.rename("New")

    repository.save(note)

    loaded = repository.get(note.id)

    assert loaded.title == "New"
