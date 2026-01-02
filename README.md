# In-Memory Todo Console Application

**Hackathon Phase I** - A console-based todo task manager with strict three-agent architecture

## Overview

This is a Python console application for managing todo tasks entirely in memory. It features a three-agent architecture with clear separation of concerns:

- **Agent 1 (State Owner)**: Manages in-memory task state
- **Agent 2 (Interface Agent)**: Handles console I/O and command orchestration
- **Agent 3 (Validation Agent)**: Validates commands and inputs

**⚠️ Important**: All data is stored in memory only and will be lost when the application exits.

## Prerequisites

- Python 3.11 or higher
- `uv` package manager ([installation guide](https://github.com/astral-sh/uv))

## Quick Start

### Installation

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -e ".[dev]"
```

### Running the Application

```bash
python -m src.main
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `add <description>` | Create a new task | `add Buy groceries` |
| `list` | Display all tasks | `list` |
| `complete <task_id>` | Mark task as complete | `complete 1` |
| `delete <task_id>` | Remove a task | `delete 2` |
| `help` | Show help message | `help` |
| `exit` | Exit application | `exit` |

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test category
pytest tests/unit/
pytest tests/integration/
```

### Code Quality

```bash
# Type checking
mypy src/

# Linting
ruff check src/

# Formatting
ruff format src/
```

## Architecture

See [specs/001-todo-console/](specs/001-todo-console/) for detailed documentation:

- [spec.md](specs/001-todo-console/spec.md) - Feature specification
- [plan.md](specs/001-todo-console/plan.md) - Implementation plan
- [data-model.md](specs/001-todo-console/data-model.md) - Data models
- [contracts/](specs/001-todo-console/contracts/) - Agent interfaces
- [quickstart.md](specs/001-todo-console/quickstart.md) - Detailed setup guide

## License

Hackathon Phase I Project
