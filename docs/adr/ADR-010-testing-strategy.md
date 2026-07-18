# ADR-010: Testing Strategy

**Status:** Accepted

**Date:** 2026-07-18

---

# Decision

Testing is considered part of implementation.

Features are incomplete until tested.

---

# Testing Levels

Unit Tests

- individual classes

Integration Tests

- component interaction

Manual Tests

- user workflows

---

# Requirements

Every public feature requires tests.

Every bug fix should include a regression test whenever practical.

---

# Release Requirements

Before every release:

- pytest passes
- Ruff passes
- Black passes
- mypy passes

Documentation reflects implementation.

---

# Philosophy

Testing provides confidence for future refactoring.

A passing test suite enables long-term maintainability.