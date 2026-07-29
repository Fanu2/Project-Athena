from abc import ABC, abstractmethod
from uuid import UUID

from .knowledge_note import KnowledgeNote


class KnowledgeNoteRepository(ABC):

    @abstractmethod
    def save(self, note: KnowledgeNote) -> None:
        pass

    @abstractmethod
    def get(self, note_id: UUID) -> KnowledgeNote | None:
        pass

    @abstractmethod
    def delete(self, note_id: UUID) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[KnowledgeNote]:
        pass
