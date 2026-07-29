from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(slots=True)
class KnowledgeNote:
    title: str
    markdown: str

    id: UUID = field(default_factory=uuid4)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    favorite: bool = False
    archived: bool = False

    def _touch(self) -> None:
        self.updated_at = datetime.now(UTC)

    def archive(self) -> None:
        self.archived = True
        self._touch()

    def restore(self) -> None:
        self.archived = False
        self._touch()

    def rename(self, title: str) -> None:
        title = title.strip()

        if not title:
            raise ValueError("Title cannot be empty.")

        self.title = title
        self._touch()

    def update_markdown(self, markdown: str) -> None:
        self.markdown = markdown
        self._touch()

    def favorite_note(self) -> None:
        self.favorite = True
        self._touch()

    def unfavorite_note(self) -> None:
        self.favorite = False
        self._touch()
