from uuid import UUID

from athena.knowledge.domain import (
    KnowledgeNote,
    KnowledgeNoteRepository,
)


class InMemoryKnowledgeNoteRepository(KnowledgeNoteRepository):

    def __init__(self) -> None:
        self._notes: dict[UUID, KnowledgeNote] = {}

    def save(self, note: KnowledgeNote) -> None:
        self._notes[note.id] = note

    def get(self, note_id: UUID) -> KnowledgeNote | None:
        return self._notes.get(note_id)

    def delete(self, note_id: UUID) -> None:
        self._notes.pop(note_id, None)

    def list_all(self) -> list[KnowledgeNote]:
        return list(self._notes.values())
