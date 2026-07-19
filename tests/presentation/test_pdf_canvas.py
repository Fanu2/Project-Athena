"""
Tests for PDFCanvas.
"""

from __future__ import annotations

from PySide6.QtGui import QImage

from athena.presentation.viewer import PDFCanvas


def test_canvas_initial_state(qtbot) -> None:
    """Canvas starts without an image."""

    canvas = PDFCanvas()

    qtbot.addWidget(canvas)

    assert not canvas.has_image


def test_set_image(qtbot) -> None:
    """Setting an image updates the canvas."""

    canvas = PDFCanvas()

    qtbot.addWidget(canvas)

    image = QImage(200, 300, QImage.Format.Format_RGB888)

    canvas.set_image(image)

    assert canvas.has_image


def test_clear(qtbot) -> None:
    """Clearing removes the image."""

    canvas = PDFCanvas()

    qtbot.addWidget(canvas)

    image = QImage(100, 100, QImage.Format.Format_RGB888)

    canvas.set_image(image)

    assert canvas.has_image

    canvas.clear()

    assert not canvas.has_image


def test_set_none(qtbot) -> None:
    """Setting None clears the image."""

    canvas = PDFCanvas()

    qtbot.addWidget(canvas)

    canvas.set_image(None)

    assert not canvas.has_image