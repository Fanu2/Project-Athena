from athena.knowledge.domain import KnowledgeNote


def test_create_note():
    note = KnowledgeNote(
        title="Athena",
        markdown="# Hello Athena",
    )

    assert note.title == "Athena"
    assert note.markdown == "# Hello Athena"
    assert note.favorite is False
    assert note.archived is False

def test_archive_note():
    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    note.archive()

    assert note.archived is True

def test_restore_note():
    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    note.archive()
    note.restore()

    assert note.archived is False
