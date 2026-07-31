"""
Athena Import Artifact

Represents normalized content produced by
an importer before knowledge compilation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from uuid import UUID, uuid4


@dataclass
class ImportArtifact:
    """
    Imported representation of a KnowledgeSource.

    Examples:
        PDF bytes
        extracted markdown
        image data
        repository snapshot
    """

    artifact_id: UUID = field(default_factory=uuid4)

    source_id: Optional[UUID] = None

    artifact_type: str = "unknown"

    content_reference: Optional[str] = None

    checksum: Optional[str] = None

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Add artifact metadata.
        """
        self.metadata[key] = value