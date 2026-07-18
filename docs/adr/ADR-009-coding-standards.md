# ADR-009: Coding Standards

**Status:** Accepted

**Date:** 2026-07-18

---

# Decision

Athena follows a consistent coding style.

---

# Requirements

All code shall include:

- type hints
- descriptive names
- docstrings for public APIs
- dependency injection
- unit tests

Models should prefer:

- dataclasses
- immutability
- slots

---

# Quality Gates

Every contribution must satisfy:

- pytest
- Ruff
- Black
- mypy

---

# Design Principles

Prefer:

- explicit behavior
- small classes
- single responsibility
- composition
- interfaces

Avoid:

- global state
- circular imports
- hidden dependencies
- duplicated logic