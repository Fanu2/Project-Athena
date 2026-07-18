# ADR-002: Workspace Layout

**Status:** Accepted

**Date:** 2026-07-18

---

# Context

Athena stores documents, indexes, notes, and future research artifacts.

A predictable workspace layout simplifies portability, backup, and future extensions.

---

# Decision

Each workspace shall contain all project-specific data.

Recommended layout:

```text
Workspace/
│
├── documents/
│
├── .athena/
│   ├── index.db
│   └── settings.json
│
├── notes/
│
└── exports/
```

---

# Rationale

This layout ensures:

- Complete portability
- Simple backup
- No hidden dependencies
- Isolation between workspaces

Users can copy or archive a workspace without additional export steps.

---

# Consequences

Future features such as bookmarks, annotations, AI conversations, and embeddings should remain inside the workspace.

No user-generated project data should be stored outside the workspace unless explicitly configured.