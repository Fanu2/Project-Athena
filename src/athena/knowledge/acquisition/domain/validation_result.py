"""
Athena Validation Result
"""

from dataclasses import dataclass, field
from typing import List, Any


@dataclass
class ValidationResult:
    """
    Result of candidate validation.
    """

    accepted: bool = False

    reasons: List[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )