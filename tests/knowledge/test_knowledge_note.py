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

def test_rename_note():
    note = KnowledgeNote(
        title="Old",
        markdown="Knowledge"
    )

    note.rename("New")

    assert note.title == "New"

import pytest


def test_rename_empty_title_raises():
    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    with pytest.raises(ValueError):
        note.rename("")

def test_update_markdown():
    note = KnowledgeNote(
        title="Athena",
        markdown="# Old"
    )

    note.update_markdown("# New")

    assert note.markdown == "# New"

def test_favorite_note():
    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    note.favorite_note()

    assert note.favorite is True

def test_unfavorite_note():
    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    note.favorite_note()
    note.unfavorite_note()

    assert note.favorite is False

from uuid import UUID


def test_note_has_uuid():
    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    assert isinstance(note.id, UUID)

from datetime import datetime


def test_note_has_timestamps():
    note = KnowledgeNote(
        title="Athena",
        markdown="Knowledge"
    )

    assert isinstance(note.created_at, datetime)
    assert isinstance(note.updated_at, datetime)

from time import sleep


def test_rename_updates_timestamp():
    note = KnowledgeNote(
        title="Old",
        markdown="Knowledge"
    )

    original = note.updated_at

    sleep(0.01)

    note.rename("New")

    assert note.updated_at > original
