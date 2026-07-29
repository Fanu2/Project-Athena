from dataclasses import dataclass


@dataclass(slots=True)
class KnowledgeNote:
    title: str
    markdown: str

    favorite: bool = False
    archived: bool = False

    def archive(self) -> None:
        self.archived = True

    def restore(self) -> None:
        self.archived = False
