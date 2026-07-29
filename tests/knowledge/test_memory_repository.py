from athena.knowledge.domain import KnowledgeNote
from athena.knowledge.infrastructure.memory_repository import InMemoryKnowledgeNoteRepository


def test_save_and_get_note():
    repository = InMemoryKnowledgeNoteRepository()

    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    repository.save(note)

    loaded = repository.get(note.id)

    assert loaded is note

def test_delete_note():
    repository = InMemoryKnowledgeNoteRepository()

    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    repository.save(note)
    repository.delete(note.id)

    assert repository.get(note.id) is None

def test_list_all_notes():
    repository = InMemoryKnowledgeNoteRepository()

    note1 = KnowledgeNote(
        title="One",
        markdown="A"
    )

    note2 = KnowledgeNote(
        title="Two",
        markdown="B"
    )

    repository.save(note1)
    repository.save(note2)

    notes = repository.list_all()

    assert len(notes) == 2
    assert note1 in notes
    assert note2 in notes
