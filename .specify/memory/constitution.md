<!--
Sync Impact Report:
- Version change: initial → 1.0.0
- Modified principles: N/A (initial ratification)
- Added sections: All (initial creation)
- Removed sections: N/A
- Templates requiring updates:
  ✅ .specify/templates/plan-template.md - Constitution Check section aligned
  ✅ .specify/templates/spec-template.md - Scope alignment verified
  ✅ .specify/templates/tasks-template.md - Task categorization aligned
- Follow-up TODOs: None
-->

# Hackathon Phase I Constitution

**Project**: In-Memory Python Console Application
**Phase**: Phase I (Foundational Development)
**Governing Framework**: Spec-Kit Plus

---

## I. Project Purpose and Scope

### Mission

Deliver a **console-based Python application** operating entirely in memory for Hackathon Phase I. This phase establishes foundational architecture, core domain logic, and operational patterns without external persistence or infrastructure dependencies.

### Phase I Boundaries

**In Scope:**
- Interactive command-line interface via stdin/stdout/stderr
- In-memory data structures and business logic
- Runtime-only data lifecycle (session-bound state)
- Core feature implementation with testing
- Design documentation and architectural decisions

**Out of Scope:**
- Persistent storage (databases, files, external state)
- Network communication or external API integrations
- Graphical interfaces (GUI, web, mobile)
- Multi-process or distributed system concerns
- Production deployment infrastructure

**Future Phases:**
- Phases beyond Phase I may introduce persistence, APIs, and deployment infrastructure
- Scope expansion requires constitutional amendment

---

## Core Principles

### I. Technology Mandate

**Python 3.11+ is the exclusive implementation language.**

- Modern features (structural pattern matching, improved error messages, performance gains) are required
- Type hints MUST be used for all public functions and class methods
- Standard library features MUST be preferred over third-party dependencies where feasible

**uv is the mandatory project manager.**

- All dependencies declared in `pyproject.toml`
- Virtual environments created via `uv venv`
- Dependency installation via `uv init`
- pip, poetry, conda, and other managers are prohibited as primary tools

**Console interface is the only permitted user interaction layer.**

- All I/O via stdin/stdout/stderr
- No GUI frameworks (tkinter, Qt, web frameworks) allowed
- Terminal-based interaction patterns enforced

**Rationale**: Python 3.11+ provides structural pattern matching and performance critical for rapid development. uv ensures reproducible builds and fast dependency resolution. Console-only interaction minimizes complexity and focuses effort on core logic.

---

### II. In-Memory Constraint (NON-NEGOTIABLE)

**All application state MUST reside in RAM during execution.**

- Data lifetime bounded by process runtime
- No writes to filesystem for state persistence
- No database connections or external storage systems
- State discarded on process exit

**Permitted exceptions:**
- Logging to stdout/stderr (ephemeral console output)
- Reading static configuration files at startup (read-only, non-state data)
- Writing diagnostic logs to files (explicitly marked as debug output, not application state)

**Prohibited:**
- Serialization to disk (pickle, JSON files, CSV, shelve)
- Database connections (SQLite, PostgreSQL, Redis, etc.)
- File-based caching or state recovery mechanisms

**Rationale**: In-memory constraint simplifies Phase I implementation, eliminates persistence complexity, and prepares clean architecture for future persistence layers.

---

### III. Architectural Separation

**Domain logic MUST be decoupled from I/O.**

- **Domain Layer**: Core business logic with no I/O dependencies; pure functions and data transformations; type-annotated interfaces
- **Interface Layer**: Console I/O adapters; command parsing and validation; output formatting
- **Separation Rule**: Domain logic MUST NOT directly call `print()` or `input()`; interface layer MUST NOT contain business rules

**Data structures MUST be serialization-ready.**

- Use `dataclasses` or typed dictionaries
- Avoid hard-coded assumptions about persistence format
- Forward compatibility for future persistence layer integration

**Rationale**: Separation ensures domain logic remains testable, reusable, and portable when persistence is added in future phases.

---

### IV. Runtime-Only Data Lifecycle

**Data exists only during process execution.**

1. **Initialization**: Data structures populated at application start or via console commands
2. **Mutation**: State changes occur only through well-defined operations
3. **Termination**: All data discarded on process exit (no cleanup persistence)

**Session isolation:**
- Each execution run is an isolated session
- No state carries over between runs
- Users MUST be explicitly informed that exiting the application loses all data

**Immutability preference:**
- Favor immutable data structures where practical
- Use `dataclasses` with `frozen=True` for value objects
- Document mutable state explicitly with justification

**Rationale**: Runtime-only lifecycle simplifies testing, eliminates data corruption risks, and enforces explicit state management.

---

### V. Quality Standards

**Code quality:**
- Type hints on all public functions and class methods
- Docstrings (Google or NumPy style) for public APIs
- Maximum cyclomatic complexity ≤ 10 per function
- Test coverage ≥ 80% for domain logic

**Testing:**
- Unit tests: Isolated domain logic tests; fast execution (< 1s total suite); no I/O dependencies (mock console interactions)
- Integration tests: End-to-end command flows; realistic user scenarios; console output validation

**Tooling (SHOULD enforce):**
- Linting: `ruff` or equivalent
- Formatting: `black` or `ruff format`
- Type checking: `mypy` (strict mode encouraged)

**Rationale**: Quality gates ensure maintainability, catch errors early, and prepare codebase for future expansion.

---

### VI. Documentation Discipline

**Required artifacts:**
- `README.md`: Setup instructions, usage guide, architecture overview
- `specs/<feature>/spec.md`: Feature requirements and user scenarios
- `specs/<feature>/plan.md`: Design decisions and technical approach
- `specs/<feature>/tasks.md`: Implementation task breakdown
- `history/adr/`: Architectural Decision Records for significant choices

**Code documentation:**
- Module-level docstrings explaining purpose and responsibilities
- Complex algorithms annotated with rationale and tradeoffs
- Public API fully documented with parameters, return types, and exceptions

**Rationale**: Documentation captures design intent, facilitates onboarding, and provides context for future maintainers and phases.

---

## Explicitly Forbidden Practices

### Prohibited Technologies

❌ **MUST NOT use:**
- Databases: SQLite, PostgreSQL, MySQL, MongoDB, Redis, etc.
- File persistence: JSON files, CSV, pickle, shelve, HDF5, etc.
- Network libraries: requests, httpx, aiohttp, websockets, etc.
- ORM frameworks: SQLAlchemy, Django ORM, Peewee, etc.
- Message queues: RabbitMQ, Kafka, Redis pub/sub, etc.
- GUI frameworks: tkinter, PyQt, Kivy, web frameworks (Flask, Django, FastAPI), etc.

### Prohibited Patterns

❌ **MUST NOT implement:**
- Serialization of state to disk for recovery
- Background daemon processes or worker pools
- Caching to filesystem or external services
- "Save/Load" features persisting beyond process lifetime
- Integration with external services or APIs
- Multi-process shared memory or IPC mechanisms

### Rationale

Restrictions enforce in-memory constraint, prevent scope creep, and ensure Phase I remains focused. Persistence and external integration are deferred to future phases with proper architectural planning.

---

## Phase Boundaries and Transition

### Phase I Completion Criteria

**Phase I is complete when:**
- All specified features implemented and tested
- Documentation current and comprehensive
- No technical debt blocks future persistence layer
- Data structures serialization-ready
- Test coverage ≥ 80% for domain logic

### Transition to Phase II

**Phase II may begin only after:**
- Phase I acceptance criteria met
- Constitutional amendment approved for new scope
- Persistence strategy documented in an ADR
- Migration plan defined for existing data structures

**Phase II scope (requires amendment):**
- Persistent storage solutions
- API development (REST, GraphQL, etc.)
- Deployment automation
- Performance optimization for scale
- External integrations

### Rationale

Clear phase boundaries prevent premature optimization, ensure Phase I delivers value independently, and prepare clean foundation for future expansion.

---

## Governance

### Constitutional Authority

This constitution supersedes all other development practices, conventions, or informal agreements for Hackathon Phase I.

### Amendment Process

**Minor Amendments (Patch/Minor version):**
- Scope: Clarifications, tooling updates, wording improvements
- Approval: Project maintainer
- Documentation: Version increment, changelog entry

**Major Amendments (Major version):**
- Scope: Expanding Phase I boundaries, removing core constraints, changing technology mandates
- Approval: Explicit stakeholder review
- Documentation: ADR required, migration plan for impacted code

### Compliance Review

**Pre-commit gates:**
- Linting passes (ruff or equivalent)
- Type checking passes (mypy strict mode)
- Formatting applied (black or ruff format)

**Pre-merge gates:**
- Test coverage ≥ 80% for domain logic
- Documentation updated for new features
- Constitution compliance verified (no prohibited technologies/patterns)

**Post-feature review:**
- Architectural alignment verified
- Technical debt documented
- ADR created for significant decisions

### Violation Handling

**Hard Violations (immediate rejection):**
- Use of databases or file persistence for application state
- External network calls or API integrations
- Non-console UI frameworks

**Soft Violations (requires justification):**
- Mutable global state (MUST document rationale)
- Complex interdependencies (MUST refactor or justify with ADR)
- Skipping tests (MUST justify and plan remediation)

---

## Definitions

**In-Memory**: Data structures allocated in RAM with no serialization to non-volatile storage during normal operation.

**Console Application**: Program interacting exclusively through stdin/stdout/stderr; no graphical windowing systems.

**Persistence**: Any mechanism retaining state beyond process termination (files, databases, external services).

**Phase I**: Current development stage as defined in Section I; distinct from future phases requiring constitutional amendment.

**Application State**: Runtime data representing user-created or user-modified information (distinct from static configuration or diagnostic logs).

**MUST/SHOULD/MAY**: RFC 2119 interpretation (MUST = mandatory requirement, SHOULD = strong recommendation, MAY = optional).

---

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
