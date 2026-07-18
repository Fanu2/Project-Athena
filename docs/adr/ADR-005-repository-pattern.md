# ADR-005: Repository Pattern

**Status:** Accepted

**Date:** 2026-07-18

---

# Context

Athena stores searchable document chunks.

The underlying storage technology may evolve over time.

Current implementation:

- SQLite

Future implementations may include:

- SQLite FTS5
- ChromaDB
- PostgreSQL
- Elasticsearch
- Other vector databases

Business logic should remain independent of storage implementation.

---

# Decision

Athena shall use the Repository Pattern.

All indexing and search operations communicate only through repository interfaces.

Example:

```
IndexingService

↓

ChunkRepository

↓

Implementation
```

Current implementation:

```
ChunkRepository

▲

SQLiteChunkRepository
```

Future implementations:

```
ChunkRepository

▲

MemoryChunkRepository

SQLiteChunkRepository

SQLiteFTSRepository

ChromaRepository

FutureRepository
```

---

# Rationale

Advantages include:

- Loose coupling
- Easier testing
- Replaceable storage
- Better maintainability
- Simpler dependency injection

Repositories isolate SQL and database-specific code from the rest of the application.

---

# Rules

Repositories:

- communicate only with storage
- contain no UI logic
- contain no business logic
- expose typed interfaces
- return domain models

Services:

- never execute SQL directly
- never depend on SQLite classes

Presentation:

- never accesses repositories directly

---

# Consequences

Changing storage technology should require only a new repository implementation.

The remainder of Athena should continue functioning without modification.

This decision enables future support for:

- SQLite Full Text Search
- Vector databases
- Cloud storage
- Distributed indexing

without changing application services.