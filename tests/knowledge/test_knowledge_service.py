from athena.knowledge.application.knowledge_note_service import KnowledgeNoteService
from athena.knowledge.infrastructure.memory_repository import InMemoryKnowledgeNoteRepository


def test_create_note():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Athena",
        markdown="# Hello"
    )

    assert note.title == "Athena"
    assert note.markdown == "# Hello"

    loaded = repository.get(note.id)

    assert loaded is note

def test_get_note():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    created = service.create_note(
        title="Athena",
        markdown="# Hello"
    )

    loaded = service.get_note(created.id)

    assert loaded is created

def test_list_notes():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    service.create_note(
        title="One",
        markdown="A"
    )

    service.create_note(
        title="Two",
        markdown="B"
    )

    notes = service.list_notes()

    assert len(notes) == 2
    assert notes[0].title == "One"
    assert notes[1].title == "Two"

def test_rename_note():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Old",
        markdown="Knowledge"
    )

    service.rename_note(
        note.id,
        "New"
    )

    loaded = service.get_note(note.id)

    assert loaded.title == "New"

def test_update_markdown():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Athena",
        markdown="Old"
    )

    service.update_markdown(
        note.id,
        "New Markdown"
    )

    loaded = service.get_note(note.id)

    assert loaded.markdown == "New Markdown"

def test_archive_note():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Athena",
        markdown="Knowledge"
    )

    service.archive_note(note.id)

    loaded = service.get_note(note.id)

    assert loaded.archived is True

def test_restore_note():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Athena",
        markdown="Knowledge"
    )

    service.archive_note(note.id)

    service.restore_note(note.id)

    loaded = service.get_note(note.id)

    assert loaded.archived is False

def test_favorite_note():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Athena",
        markdown="Knowledge"
    )

    service.favorite_note(note.id)

    loaded = service.get_note(note.id)

    assert loaded.favorite is True

def test_unfavorite_note():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Athena",
        markdown="Knowledge"
    )

    service.favorite_note(note.id)
    service.unfavorite_note(note.id)

    loaded = service.get_note(note.id)

    assert loaded.favorite is False

def test_delete_note():
    repository = InMemoryKnowledgeNoteRepository()
    service = KnowledgeNoteService(repository)

    note = service.create_note(
        title="Athena",
        markdown="Knowledge"
    )

    service.delete_note(note.id)

    assert service.get_note(note.id) is None
