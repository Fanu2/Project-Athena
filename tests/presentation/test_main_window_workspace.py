from athena.core.application_context import ApplicationContext
from athena.presentation.windows.main_window import MainWindow


def test_main_window_contains_workspace_page(qtbot):
    context = ApplicationContext()
    window = MainWindow(context)

    qtbot.addWidget(window)

    assert window.workspace_page is not None
    assert window.page_stack.indexOf(window.workspace_page) >= 0


def test_main_window_navigation_opens_workspace_page(qtbot):
    context = ApplicationContext()
    window = MainWindow(context)

    qtbot.addWidget(window)

    window.navigation.setCurrentRow(8)

    assert window.page_stack.currentWidget() is window.workspace_page
