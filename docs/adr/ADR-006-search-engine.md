# ADR-006: Search Engine

**Status:** Accepted

**Date:** 2026-07-18

---

# Context

Users require fast and reliable access to information stored in their document collections.

Search capabilities will evolve over time, but the public API should remain stable.

---

# Decision

Athena shall implement search as an independent subsystem.

```
User Query

↓

Search Service

↓

Repository

↓

Results
```

The Search Service owns:

- query validation
- search execution
- ranking
- result limiting

Repositories provide storage-specific implementations.

---

# Search Evolution

Athena will support multiple search strategies.

Phase 1

- Keyword search

Phase 2

- SQLite Full Text Search (FTS5)

Phase 3

- Vector search

Phase 4

- Hybrid retrieval

The public API shall remain unchanged.

---

# Rules

Search never:

- reads files
- executes SQL directly
- communicates with the UI

Search depends only on repository interfaces.

---

# Consequences

Future ranking algorithms may be introduced without changing the Presentation Layer.

Examples:

- BM25
- cosine similarity
- hybrid ranking
- semantic search