from uuid import UUID

from athena.knowledge.domain import (
    KnowledgeNote,
    KnowledgeNoteRepository,
)


class KnowledgeNoteService:

    def __init__(
        self,
        repository: KnowledgeNoteRepository,
    ) -> None:
        self._repository = repository

    def create_note(
        self,
        title: str,
        markdown: str,
    ) -> KnowledgeNote:

        note = KnowledgeNote(
            title=title,
            markdown=markdown,
        )

        self._repository.save(note)

        return note

    def get_note(
        self,
        note_id: UUID,
    ) -> KnowledgeNote | None:
        return self._repository.get(note_id)

    def list_notes(self) -> list[KnowledgeNote]:
        return self._repository.list_all()

    def rename_note(
        self,
        note_id: UUID,
        title: str,
    ) -> None:

        note = self._repository.get(note_id)

        if note is None:
            raise ValueError("Knowledge note not found.")

        note.rename(title)

        self._repository.save(note)

    def update_markdown(
        self,
        note_id: UUID,
        markdown: str,
    ) -> None:

        note = self._repository.get(note_id)

        if note is None:
            raise ValueError("Knowledge note not found.")

        note.update_markdown(markdown)

        self._repository.save(note)

    def archive_note(
        self,
        note_id: UUID,
    ) -> None:

        note = self._repository.get(note_id)

        if note is None:
            raise ValueError("Knowledge note not found.")

        note.archive()

        self._repository.save(note)

    def restore_note(
        self,
        note_id: UUID,
    ) -> None:

        note = self._repository.get(note_id)

        if note is None:
            raise ValueError("Knowledge note not found.")

        note.restore()

        self._repository.save(note)

    def favorite_note(
        self,
        note_id: UUID,
    ) -> None:

        note = self._repository.get(note_id)

        if note is None:
            raise ValueError("Knowledge note not found.")

        note.favorite_note()

        self._repository.save(note)

    def unfavorite_note(
        self,
        note_id: UUID,
    ) -> None:

        note = self._repository.get(note_id)

        if note is None:
            raise ValueError("Knowledge note not found.")

        note.unfavorite_note()

        self._repository.save(note)

    def delete_note(
        self,
        note_id: UUID,
    ) -> None:

        self._repository.delete(note_id)
