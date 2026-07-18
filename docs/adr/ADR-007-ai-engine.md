# ADR-007: AI Engine

**Status:** Accepted

**Date:** 2026-07-18

---

# Context

Artificial Intelligence enhances research by generating answers from indexed documents.

The AI subsystem must remain independent from storage implementation.

---

# Decision

Athena shall separate retrieval from generation.

```
Question

↓

Search

↓

Retrieved Chunks

↓

Prompt Builder

↓

LLM

↓

Answer
```

The AI engine never accesses:

- SQLite
- files
- repositories

directly.

It communicates only with the Search Service.

---

# Responsibilities

The AI engine:

- builds prompts
- selects context
- communicates with LLM providers
- formats answers
- generates citations

The AI engine does not:

- index documents
- search databases
- manage files

---

# LLM Providers

Providers may include:

- Ollama
- llama.cpp
- OpenAI
- Anthropic
- Gemini

Each provider implements a common interface.

---

# Consequences

Changing LLM providers should require only replacing the provider implementation.

The AI engine remains unchanged.