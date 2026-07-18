from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class Workspace:
    name: str
    path: Path
    version: str
    created: datetime
    modified: datetime
