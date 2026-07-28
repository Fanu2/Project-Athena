from __future__ import annotations

from athena.kernel.service_registry import ServiceRegistry


class AthenaKernel:
    """Application composition root for Athena."""

    VERSION = "A7.5"

    def __init__(self):
        self.services = ServiceRegistry()

    def register(self, name: str, service: object) -> None:
        self.services.register(name, service)

    def get(self, name: str) -> object:
        return self.services.get(name)

    def health(self) -> dict:
        return {
            "status": "ok",
            "version": self.VERSION,
            "services": self.services.names(),
        }

