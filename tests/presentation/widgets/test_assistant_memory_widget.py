"""
Tests for assistant memory widget.
"""

from datetime import datetime

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)

from athena.presentation.widgets.assistant_memory import (
    AssistantMemoryWidget,
)


def test_memory_widget_displays_memory(
    qtbot,
):

    widget = AssistantMemoryWidget()

    qtbot.addWidget(
        widget,
    )

    memory = AssistantMemoryItem(
        key="style",
        value="concise answers",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    widget.set_memories(
        (
            memory,
        )
    )

    assert (
        "style"
        in widget.content.text()
    )

    assert (
        "concise answers"
        in widget.content.text()
    )
