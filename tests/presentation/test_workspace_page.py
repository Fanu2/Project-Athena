from athena.presentation.workspace.workspace_page import WorkspacePage


class FakeWorkspace:
    def __init__(self):
        self.workspace = type(
            "Workspace",
            (),
            {
                "name": "Athena Research",
                "project_count": 2,
                "document_count": 3,
                "note_count": 1,
            },
        )()

        self.projects = [
            type("Project", (), {"name": "Project A"})(),
            type("Project", (), {"name": "Project B"})(),
        ]

        self.collections = [
            type("Collection", (), {"name": "Collection A"})(),
        ]

        self.documents = [
            type("Document", (), {"filename": "research.pdf"})(),
            type("Document", (), {"filename": "notes.md"})(),
            type("Document", (), {"filename": "report.docx"})(),
        ]

        self.notes = [
            type("Note", (), {"title": "Research Notes"})(),
        ]


class FakeProvider:
    def build(self, workspace_id, **kwargs):
        assert workspace_id == "workspace-1"
        return FakeWorkspace()


def test_workspace_page_refreshes_from_provider(qtbot):
    page = WorkspacePage()
    qtbot.addWidget(page)

    page.set_workspace_provider(
        FakeProvider(),
        "workspace-1",
    )

    assert page.title_label.text() == "Athena Research"
    assert "Projects: 2" in page.summary_label.text()
    assert "Documents: 3" in page.summary_label.text()
    assert "Notes: 1" in page.summary_label.text()

    assert page.projects_list.count() == 2
    assert page.collections_list.count() == 1
    assert page.documents_list.count() == 3
    assert page.notes_list.count() == 1

    assert page.projects_list.item(0).text() == "Project A"
    assert page.documents_list.item(0).text() == "research.pdf"
    assert page.notes_list.item(0).text() == "Research Notes"


def test_workspace_page_clear(qtbot):
    page = WorkspacePage()
    qtbot.addWidget(page)

    page.set_workspace_provider(
        FakeProvider(),
        "workspace-1",
    )

    page.clear()

    assert page.projects_list.count() == 0
    assert page.collections_list.count() == 0
    assert page.documents_list.count() == 0
    assert page.notes_list.count() == 0
    assert page.summary_label.text() == ""
