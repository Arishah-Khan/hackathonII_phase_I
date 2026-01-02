# Data Model: In-Memory Todo Console Application

**Feature**: 001-todo-console | **Date**: 2026-01-01
**Purpose**: Define entity structure and relationships for three-agent architecture

## Overview

This document specifies the data model for the in-memory todo console application. All entities are designed to be immutable value objects using Python dataclasses, supporting the constitutional requirement for serialization-ready structures.

## Core Entities

### TodoTask

**Purpose**: Represents a single task item to be completed

**Attributes**:
| Name | Type | Required | Constraints | Description |
|------|------|----------|-------------|-------------|
| id | int | Yes | > 0, unique within session | Stable task identifier assigned by State Owner |
| description | str | Yes | Non-empty, trimmed | User-provided task description |
| is_complete | bool | Yes | True or False | Completion status (pending or complete) |
| created_at | datetime | Yes | ISO 8601 timestamp | Task creation timestamp (for future sorting) |

**Invariants**:
- ID assigned by State Owner, never changed after creation
- Description cannot be empty or whitespace-only
- Completion status can transition from False → True (idempotent if already True)
- Created timestamp immutable after task creation

**Python Implementation**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TodoTask:
    """Immutable representation of a todo task.

    Attributes:
        id: Unique task identifier (within session)
        description: Task description text
        is_complete: Whether task has been marked complete
        created_at: Timestamp when task was created
    """
    id: int
    description: str
    is_complete: bool
    created_at: datetime

    def complete(self) -> 'TodoTask':
        """Return new task with is_complete=True.

        Returns:
            New TodoTask instance with completion status updated
        """
        return TodoTask(
            id=self.id,
            description=self.description,
            is_complete=True,
            created_at=self.created_at
        )
```

---

### CommandRequest

**Purpose**: Represents a validated user command flowing from Interface Agent to State Owner

**Attributes**:
| Name | Type | Required | Constraints | Description |
|------|------|----------|-------------|-------------|
| command_type | CommandType (enum) | Yes | One of: ADD, LIST, COMPLETE, DELETE, HELP, EXIT | Command operation type |
| task_id | Optional[int] | Conditional | Required for COMPLETE, DELETE | Target task identifier |
| description | Optional[str] | Conditional | Required for ADD | Task description for new tasks |

**Command Type Enumeration**:
```python
from enum import Enum

class CommandType(Enum):
    """Supported command operations."""
    ADD = "add"
    LIST = "list"
    COMPLETE = "complete"
    DELETE = "delete"
    HELP = "help"
    EXIT = "exit"
```

**Python Implementation**:
```python
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CommandRequest:
    """Represents a parsed and validated user command.

    Attributes:
        command_type: The type of command operation
        task_id: Task identifier (for COMPLETE/DELETE commands)
        description: Task description (for ADD commands)
    """
    command_type: CommandType
    task_id: Optional[int] = None
    description: Optional[str] = None
```

**Validation Rules**:
- ADD command: description must be present and non-empty
- COMPLETE/DELETE commands: task_id must be present and positive integer
- LIST/HELP/EXIT commands: no additional parameters required

---

### ValidationResult

**Purpose**: Represents the outcome of command validation by Validation Agent

**Attributes**:
| Name | Type | Required | Constraints | Description |
|------|------|----------|-------------|-------------|
| is_valid | bool | Yes | True or False | Whether validation passed |
| error_message | Optional[str] | Conditional | Present if is_valid=False | Human-readable error description |

**Python Implementation**:
```python
@dataclass(frozen=True)
class ValidationResult:
    """Result of command validation.

    Attributes:
        is_valid: Whether the command passed validation
        error_message: Error description if validation failed
    """
    is_valid: bool
    error_message: Optional[str] = None

    @staticmethod
    def success() -> 'ValidationResult':
        """Create a successful validation result."""
        return ValidationResult(is_valid=True)

    @staticmethod
    def failure(message: str) -> 'ValidationResult':
        """Create a failed validation result with error message.

        Args:
            message: Human-readable error description

        Returns:
            ValidationResult with is_valid=False and error message
        """
        return ValidationResult(is_valid=False, error_message=message)
```

---

### CommandResult

**Purpose**: Represents the outcome of command execution by State Owner

**Attributes**:
| Name | Type | Required | Constraints | Description |
|------|------|----------|-------------|-------------|
| success | bool | Yes | True or False | Whether command executed successfully |
| message | Optional[str] | Optional | Present for user feedback | Success or error message for user |
| tasks | Optional[List[TodoTask]] | Conditional | Present for LIST command | Task list result |

**Python Implementation**:
```python
from typing import List

@dataclass(frozen=True)
class CommandResult:
    """Result of command execution.

    Attributes:
        success: Whether command executed successfully
        message: User-facing success or error message
        tasks: List of tasks (for LIST command)
    """
    success: bool
    message: Optional[str] = None
    tasks: Optional[List[TodoTask]] = None
```

---

## State Management

### State Owner Internal State

The State Owner (Agent 1) maintains the following in-memory state:

**State Structure**:
```python
class StateOwner:
    _tasks: Dict[int, TodoTask]  # Task storage: ID → Task
    _next_id: int                # Auto-increment counter for task IDs
```

**State Invariants**:
- `_tasks` dictionary always contains valid TodoTask instances
- `_next_id` always greater than any existing task ID
- Task IDs never reused within a session (monotonically increasing)
- All state private to State Owner; accessed only via command methods

**State Operations**:
| Operation | Effect | Returns |
|-----------|--------|---------|
| add_task(description) | Creates new task with next_id, increments counter | CommandResult with success=True |
| list_tasks() | Returns all tasks as list | CommandResult with tasks populated |
| complete_task(task_id) | Updates task completion status | CommandResult with success status |
| delete_task(task_id) | Removes task from dictionary | CommandResult with success status |

---

## Entity Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                        Console User Input                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Interface Agent (Agent 2)                      │
│  - Parses input string                                           │
│  - Creates CommandRequest                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Validation Agent (Agent 3)                       │
│  - Receives CommandRequest                                       │
│  - Returns ValidationResult                                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                   ┌─────────┴─────────┐
                   │ Valid?            │
                   └─────────┬─────────┘
                   Yes       │       No
                   │         │         │
                   ▼         │         ▼
         ┌─────────────────┐ │ ┌──────────────────┐
         │ State Owner     │ │ │ Return error to  │
         │ (Agent 1)       │ │ │ Interface Agent  │
         │ - Execute cmd   │ │ └──────────────────┘
         │ - Update state  │ │
         │ - Return result │ │
         └────────┬────────┘ │
                  │          │
                  ▼          │
         ┌─────────────────┐ │
         │ CommandResult   │ │
         └────────┬────────┘ │
                  │          │
                  └──────────┴───────────────────┐
                                                 ▼
                             ┌─────────────────────────────────────┐
                             │   Interface Agent (Agent 2)         │
                             │   - Format output                   │
                             │   - Display to console              │
                             └─────────────────────────────────────┘
```

**Data Flow**:
1. User enters command text
2. Interface Agent parses to CommandRequest
3. Validation Agent validates CommandRequest → ValidationResult
4. If valid: State Owner executes → CommandResult
5. If invalid: Interface Agent displays ValidationResult error
6. Interface Agent formats and displays result to user

---

## Validation Rules by Entity

### TodoTask Validation
- **ID**: Must be positive integer (assigned by State Owner)
- **Description**: Must be non-empty after trimming whitespace
- **is_complete**: Boolean only (no null/undefined)
- **created_at**: Must be valid datetime (assigned by State Owner)

### CommandRequest Validation
- **ADD command**: description present and non-empty
- **COMPLETE command**: task_id present and positive integer
- **DELETE command**: task_id present and positive integer
- **LIST/HELP/EXIT**: No additional validation required

### State Validation
- **COMPLETE/DELETE operations**: Task with given ID must exist in State Owner
- **ADD operation**: No duplicate description check (users can have duplicate tasks)

---

## Serialization Readiness

All entities use `@dataclass(frozen=True)` making them:
- **Immutable**: Thread-safe and cacheable
- **Hashable**: Can be used as dictionary keys or set members
- **JSON-serializable**: Easy conversion via dataclasses.asdict()
- **Type-safe**: Full type hint support for mypy validation

**Future Persistence Integration**:
When persistence is added in future phases, these entities can be directly:
- Serialized to JSON/YAML without modification
- Mapped to database tables (ORM-ready structure)
- Transmitted over network APIs (already defined schemas)

No changes to entity structure will be required for persistence layer integration.

---

## Summary

**Total Entities**: 5 core data classes
- TodoTask: Domain entity
- CommandRequest: Command pattern request
- CommandType: Enumeration of operations
- ValidationResult: Validation outcome
- CommandResult: Execution outcome

**Key Design Principles**:
- Immutability via `frozen=True` dataclasses
- Clear type annotations for all fields
- Validation rules enforced by Validation Agent
- State encapsulated in State Owner
- Agent boundaries enforced through typed interfaces

All entities align with constitutional requirements:
- ✅ Serialization-ready structures
- ✅ Domain decoupled from I/O
- ✅ Type hints on all public APIs
- ✅ Immutability preferred
