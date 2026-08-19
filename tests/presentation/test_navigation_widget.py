from athena.presentation.navigation.navigation_widget import (
    NavigationWidget,
)


def test_navigation_contains_a20_workspace(qtbot):
    navigation = NavigationWidget()
    qtbot.addWidget(navigation)

    assert navigation.count() == 11
    assert navigation.item(8).text() == "🗂 A20 Workspace"


def test_navigation_emits_workspace_selected(qtbot):
    navigation = NavigationWidget()
    qtbot.addWidget(navigation)

    emissions = []

    navigation.workspace_selected.connect(
        lambda: emissions.append(True),
    )

    navigation.setCurrentRow(8)

    assert emissions == [True]


def test_navigation_preserves_collections_and_settings(qtbot):
    navigation = NavigationWidget()
    qtbot.addWidget(navigation)

    collections = []
    settings = []

    navigation.collections_selected.connect(
        lambda: collections.append(True),
    )

    navigation.settings_selected.connect(
        lambda: settings.append(True),
    )

    navigation.setCurrentRow(9)
    navigation.setCurrentRow(10)

    assert collections == [True]
    assert settings == [True]
