"""
Public API for the Athena Intent Engine.

The IntentService is the only public entry point into the
Intent Engine. It delegates intent detection to the
IntentDetector.
"""

from __future__ import annotations

from .detector import IntentDetector
from .models import IntentResult


class IntentService:
    """
    Public interface for intent detection.
    """

    def __init__(self) -> None:
        self._detector = IntentDetector()

    def detect(self, query: str) -> IntentResult:
        """
        Detect the user's intent.

        Parameters
        ----------
        query
            Raw user query.

        Returns
        -------
        IntentResult
            Result of intent detection.
        """
        return self._detector.detect(query)