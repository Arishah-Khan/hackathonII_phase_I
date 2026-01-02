# Research: In-Memory Todo Console Application

**Feature**: 001-todo-console | **Date**: 2026-01-01
**Purpose**: Resolve technical unknowns and document design decisions

## Overview

This document captures research findings for implementing a three-agent architecture in Python for an in-memory todo console application. All technical context was clearly specified in the feature requirements, so minimal research was needed.

## Research Areas

### 1. Three-Agent Architecture Pattern in Python

**Decision**: Use dependency injection pattern with explicit agent interfaces

**Rationale**:
- Python's duck typing allows flexible agent contracts without heavy frameworks
- Explicit interfaces (via Protocol or ABC) document agent boundaries clearly
- Dependency injection enables clean testing and agent isolation
- Aligns with constitutional requirement for architectural separation

**Alternatives Considered**:
- Message bus pattern: Rejected - adds complexity for single-process in-memory application
- Event-driven architecture: Rejected - overkill for synchronous console commands
- Shared state with locks: Rejected - violates agent boundary separation requirements

**Implementation Approach**:
- Define Agent protocols using `typing.Protocol` for structural typing
- State Owner exposes command interface (add_task, list_tasks, complete_task, delete_task)
- Validation Agent exposes validation interface (validate_command) returning ValidationResult
- Interface Agent orchestrates: parse input → validate → execute → format output

### 2. In-Memory Data Structures for Task Storage

**Decision**: Use Python dictionary with integer keys for O(1) task lookup

**Rationale**:
- Dictionary provides fast access by task ID
- Meets performance requirement (< 1 second for 1000 tasks)
- Simple to implement and reason about
- Auto-incrementing integer IDs provide stable references per FR-019

**Alternatives Considered**:
- List with linear search: Rejected - O(n) lookup doesn't scale to 1000 tasks
- OrderedDict: Rejected - insertion order not required for this use case
- Custom data structure: Rejected - unnecessary complexity

**Data Model Design**:
```python
@dataclass(frozen=True)
class TodoTask:
    id: int
    description: str
    is_complete: bool
    created_at: datetime  # For potential future sorting/filtering

# State Owner maintains:
tasks: Dict[int, TodoTask] = {}
next_id: int = 1
```

### 3. Command Parsing Strategy

**Decision**: Simple string-based command parser with argument extraction

**Rationale**:
- Console commands have predictable structure (verb + arguments)
- No need for complex CLI framework (argparse, click) for 4 operations
- Custom parser provides clear error messages for validation
- Aligns with "standard library preferred" constitutional principle

**Alternatives Considered**:
- argparse: Rejected - designed for script arguments, not interactive REPL
- click: Rejected - external dependency, overkill for simple commands
- cmd module: Rejected - adds framework overhead for simple use case

**Command Format**:
```
add <description>      # Add new task
list                   # List all tasks
complete <task_id>     # Mark task complete
delete <task_id>       # Delete task
help                   # Show help
exit                   # Exit application
```

### 4. Validation Rules Implementation

**Decision**: Centralized validation in Validation Agent using composable validator functions

**Rationale**:
- Keeps validation logic out of State Owner (per FR-010)
- Enables reusable validation rules (e.g., non-empty description)
- Clear separation makes rules easy to test and modify
- Validation results carry context for helpful error messages

**Validation Categories**:
- **Command syntax**: Valid command verb and argument count
- **Data validation**: Non-empty description, valid task ID format
- **State validation**: Task ID exists (for complete/delete operations)
- **Business rules**: No additional rules for Phase I (keep simple)

**Validation Result Design**:
```python
@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    error_message: Optional[str] = None
```

### 5. Console I/O and Error Handling

**Decision**: Use standard print/input with structured output formatting

**Rationale**:
- Constitutional requirement: console-only interface
- Standard library functions sufficient for requirements
- Clear error messages improve user experience per SC-005
- Structured output (tables, lists) enhances readability

**Error Handling Strategy**:
- Validation errors: Display to user with guidance, don't crash
- Internal errors: Log to stderr, provide user-friendly message
- Exit handling: Warn user about data loss per FR-023

**Output Format Examples**:
```
# List output
Tasks:
  [1] Buy groceries
  [2] ✓ Write report
  [3] Call dentist

# Error output
Error: Task ID '99' not found
```

### 6. Testing Strategy for Agent Boundaries

**Decision**: Unit tests for each agent in isolation; integration tests for agent interactions

**Rationale**:
- Constitutional requirement: ≥ 80% coverage for domain logic
- Agent isolation crucial for architectural integrity
- Mock dependencies for unit tests (State Owner, Validation Agent)
- Integration tests verify command flow: Interface → Validation → State Owner

**Test Categories**:
- **Unit tests**: Each agent tested independently with mocked dependencies
- **Integration tests**: End-to-end command flows with real agent instances
- **Contract tests**: Verify agent interfaces match expected protocols

**Key Test Scenarios**:
- Agent 1 (State Owner): Task operations without validation or I/O
- Agent 2 (Interface Agent): Command routing without state or validation logic
- Agent 3 (Validation Agent): Validation rules without state changes or I/O
- Integration: Full command flows from user input to console output

### 7. Application Lifecycle Management

**Decision**: Simple REPL (Read-Eval-Print Loop) with graceful shutdown

**Rationale**:
- Console application naturally fits REPL pattern
- Agent initialization at startup (per FR-024)
- Clean shutdown with data loss warning (per FR-023)
- Single-threaded synchronous execution keeps it simple

**Lifecycle Phases**:
1. **Startup**: Initialize agents in order (State Owner → Validation Agent → Interface Agent)
2. **REPL Loop**: Read command → Parse → Validate → Execute → Display → Repeat
3. **Shutdown**: Display warning about data loss, exit cleanly

## Technology Decisions Summary

| Category | Decision | Justification |
|----------|----------|---------------|
| Language | Python 3.11+ | Constitutional mandate; structural pattern matching useful |
| Package Manager | uv | Constitutional mandate; fast, modern dependency management |
| Data Storage | Dictionary (in-memory) | O(1) lookup; meets performance requirements |
| Agent Pattern | Dependency injection | Clear boundaries; testable; flexible |
| Command Parsing | Custom string parser | Simple; no external dependencies; clear errors |
| Validation | Centralized validator functions | Composable; testable; separated from state |
| Testing Framework | pytest | Standard choice; excellent Python support; coverage tools |
| Type Checking | mypy (strict mode) | Constitutional recommendation; catches errors early |
| Data Classes | @dataclass with frozen=True | Immutable value objects; serialization-ready |

## Open Questions Resolved

All questions from specification were answerable through analysis:

1. **Agent communication protocol**: Method calls with typed request/response objects
2. **Task ID stability**: Auto-increment integer IDs never reused within session
3. **Validation timing**: Before state modification, in Validation Agent
4. **Error message format**: Human-readable strings with context
5. **Performance at scale**: Dictionary operations O(1), easily handles 1000+ tasks

## Dependencies

**Production Dependencies**: None (standard library only)

**Development Dependencies**:
- pytest: Testing framework
- pytest-cov: Coverage reporting
- mypy: Type checking
- ruff: Linting and formatting

All managed via `uv` as specified in constitution.

## Next Steps

Phase 1 artifacts ready for generation:
1. `data-model.md`: Detailed entity definitions and relationships
2. `contracts/`: Agent interface specifications
3. `quickstart.md`: Setup and usage guide

No additional research required - all technical decisions resolved.
