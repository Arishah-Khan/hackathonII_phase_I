# Agent Interface Contracts

**Feature**: 001-todo-console | **Date**: 2026-01-01
**Purpose**: Define formal interfaces for three-agent architecture

## Overview

This directory contains interface contracts for the three agents in the todo console application. Each agent has a clearly defined responsibility and communicates through typed interfaces.

## Agent Responsibilities

### Agent 1: State Owner (`state_owner_interface.py`)
**Role**: In-memory state management

**Responsibilities**:
- Create new tasks with auto-incrementing IDs
- Store tasks in memory (dictionary-based)
- Retrieve task information
- Update task completion status
- Delete tasks from memory
- Maintain task ID allocation

**Prohibited**:
- ❌ No validation logic (delegated to Validation Agent)
- ❌ No user interaction (delegated to Interface Agent)
- ❌ No I/O operations (print/input)

**Interface Methods**:
- `add_task(description: str) -> int`
- `list_tasks() -> List[tuple[int, str, bool, datetime]]`
- `complete_task(task_id: int) -> bool`
- `delete_task(task_id: int) -> bool`
- `get_task(task_id: int) -> tuple[...] | None`
- `get_task_count() -> int`

---

### Agent 2: Interface Agent (`interface_agent_interface.py`)
**Role**: Console I/O and command orchestration

**Responsibilities**:
- Read user input from stdin
- Parse commands and arguments
- Route commands to Validation Agent
- Route validated commands to State Owner
- Format and display output to stdout/stderr
- Display welcome message and data loss warning

**Prohibited**:
- ❌ No state modification (delegated to State Owner)
- ❌ No validation logic (delegated to Validation Agent)
- ❌ No business rules (pure I/O and orchestration)

**Interface Methods**:
- `run() -> None` - Main REPL loop
- `display_welcome() -> None`
- `parse_input(user_input: str) -> tuple[str, list[str]]`
- `display_error(message: str) -> None`
- `display_success(message: str) -> None`
- `display_tasks(tasks: List[tuple]) -> None`
- `display_help() -> None`

---

### Agent 3: Validation Agent (`validation_agent_interface.py`)
**Role**: Command and input validation

**Responsibilities**:
- Validate command syntax and format
- Validate command parameters (non-empty descriptions, valid task IDs)
- Check state prerequisites (task existence via State Owner query)
- Return structured validation results with error messages

**Prohibited**:
- ❌ No state modification (read-only queries only)
- ❌ No user interaction (returns ValidationResult to Interface Agent)
- ❌ No command execution (only validates)

**Interface Methods**:
- `validate_add_command(description: str | None) -> ValidationResult`
- `validate_complete_command(task_id: str | None) -> ValidationResult`
- `validate_delete_command(task_id: str | None) -> ValidationResult`
- `validate_list_command() -> ValidationResult`
- `validate_help_command() -> ValidationResult`
- `validate_exit_command() -> ValidationResult`

**ValidationResult**:
```python
@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    error_message: str | None = None
```

---

## Command Flow

```
User Input (stdin)
        │
        ▼
┌───────────────────────┐
│   Interface Agent     │  Parse input string
│   (Agent 2)           │  → (command, args)
└──────────┬────────────┘
           │
           ▼
┌───────────────────────┐
│   Validation Agent    │  Validate command
│   (Agent 3)           │  → ValidationResult
└──────────┬────────────┘
           │
    ┌──────┴──────┐
    │ is_valid?   │
    └──────┬──────┘
      Yes  │  No
           │  │
           │  └─────────────────────┐
           ▼                        │
┌───────────────────────┐           │
│   State Owner         │           │
│   (Agent 1)           │           │
│   Execute command     │           │
│   Return result       │           │
└──────────┬────────────┘           │
           │                        │
           ▼                        ▼
┌───────────────────────────────────────┐
│   Interface Agent (Agent 2)           │
│   Format and display result           │
└───────────────────────────────────────┘
           │
           ▼
    Console Output (stdout/stderr)
```

## Design Principles

### 1. Separation of Concerns
Each agent has a single, well-defined responsibility:
- **State Owner**: What data exists
- **Validation Agent**: Whether operations are valid
- **Interface Agent**: How users interact

### 2. Type Safety
All interfaces use Python type hints for:
- Parameter types
- Return types
- Optional values (using `| None`)

### 3. Immutability
Data passed between agents is immutable:
- ValidationResult is a frozen dataclass
- Task data returned as tuples (immutable)
- No shared mutable state

### 4. Protocol-Based Design
Interfaces defined as `Protocol` classes:
- Structural typing (duck typing with type checks)
- No inheritance required
- Easy to mock for testing
- Clear contract definition

### 5. Constitutional Alignment
All interfaces enforce constitutional requirements:
- ✅ In-memory only (no persistence methods)
- ✅ Console-only I/O (Interface Agent only)
- ✅ Domain decoupled from I/O
- ✅ Type hints on all methods
- ✅ Serialization-ready structures

## Testing Strategy

### Unit Testing
Each agent tested independently with mocked dependencies:

**State Owner Tests**:
- Mock: None (pure state management)
- Test: Task CRUD operations, ID allocation, edge cases

**Interface Agent Tests**:
- Mock: State Owner, Validation Agent
- Test: Command parsing, output formatting, orchestration

**Validation Agent Tests**:
- Mock: State Owner (for existence checks)
- Test: Validation rules, error messages, edge cases

### Integration Testing
Test agent interactions with real instances:
- Full command flows from input to output
- Agent communication protocols
- End-to-end user scenarios

### Contract Testing
Verify implementations satisfy interface protocols:
- Protocol compliance checks
- Type hint validation (mypy)
- Method signature matching

## Implementation Notes

### Dependency Injection
Agents receive dependencies via constructor:

```python
class InterfaceAgent:
    def __init__(
        self,
        state_owner: StateOwnerInterface,
        validator: ValidationAgentInterface
    ):
        self._state_owner = state_owner
        self._validator = validator
```

### Error Handling
- Validation errors: Returned as ValidationResult with error_message
- State errors: Returned as bool (False indicates failure)
- System errors: Raised as exceptions (caught by Interface Agent)

### Initialization Order
1. State Owner (no dependencies)
2. Validation Agent (depends on State Owner for existence checks)
3. Interface Agent (depends on both State Owner and Validation Agent)

## Contract Versioning

All contracts versioned independently:
- Current version: 1.0.0
- Breaking changes increment major version
- Backward-compatible additions increment minor version

## References

- [Specification](../spec.md): Feature requirements
- [Data Model](../data-model.md): Entity definitions
- [Research](../research.md): Design decisions and rationale
