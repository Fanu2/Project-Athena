from __future__ import annotations


class ServiceRegistry:
    """Registers and provides application services."""

    def __init__(self):
        self._services: dict[str, object] = {}

    def register(self, name: str, service: object) -> None:
        self._services[name] = service

    def get(self, name: str) -> object:
        return self._services[name]

    def has(self, name: str) -> bool:
        return name in self._services

    def names(self) -> list[str]:
        return sorted(self._services.keys())
