"""
PDF page display widget.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QImage, QPainter
from PySide6.QtWidgets import QWidget


class PDFCanvas(QWidget):
    """
    Widget for displaying rendered PDF pages.

    This widget only displays QImage objects.
    It has no knowledge of PDFs, documents,
    renderers or application services.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._image: QImage | None = None

        self.setMinimumSize(300, 400)

    @property
    def has_image(self) -> bool:
        """Return True if an image is loaded."""

        return self._image is not None

    def set_image(
        self,
        image: QImage | None,
    ) -> None:
        """
        Display a rendered page.
        """

        self._image = image

        self.update()

    def clear(self) -> None:
        """Clear the displayed page."""

        self._image = None

        self.update()

    def paintEvent(self, event) -> None:
        """
        Paint the current page.
        """

        del event

        painter = QPainter(self)

        painter.fillRect(
            self.rect(),
            QColor(240, 240, 240),
        )

        if self._image is None:
            painter.setPen(Qt.GlobalColor.darkGray)

            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                "No document loaded",
            )

            return

        scaled = self._image.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2

        painter.drawImage(
            x,
            y,
            scaled,
        )
