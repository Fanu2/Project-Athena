from __future__ import annotations

from enum import Enum


class HealthStatus(str, Enum):
    """AI provider health state."""

    ONLINE = "online"
    OFFLINE = "offline"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"