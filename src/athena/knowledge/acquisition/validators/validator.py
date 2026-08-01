"""
Athena Validator Contract

Defines validation behaviour for
knowledge candidates.
"""

from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    """
    Base validator interface.
    """

    @abstractmethod
    def validate(
        self,
        candidate: Any,
    ) -> bool:
        """
        Validate candidate.

        Returns:
            True if accepted.
        """
        raise NotImplementedError