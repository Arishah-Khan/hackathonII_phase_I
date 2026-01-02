---
description: "Implementation tasks for In-Memory Todo Console Application"
---

# Tasks: In-Memory Todo Console Application

**Input**: Design documents from `/specs/001-todo-console/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are REQUIRED per constitutional mandate (≥80% coverage for domain logic)

**Organization**: Tasks grouped by user story to enable independent implementation and testing

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, or SETUP/FOUND for infrastructure)
- Include exact file paths in descriptions

## Path Conventions

- Single project structure: `src/`, `tests/` at repository root
- Paths follow structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create directory structure: src/agents/, src/domain/, src/console/, tests/unit/, tests/integration/
- [x] T002 Initialize Python project with pyproject.toml using uv (Python 3.11+, pytest, mypy, ruff dependencies)
- [x] T003 [P] Configure mypy.ini for strict type checking
- [x] T004 [P] Configure ruff.toml for linting and formatting
- [x] T005 [P] Create README.md with setup instructions (reference quickstart.md)
- [x] T006 [P] Create .gitignore for Python (.venv/, __pycache__/, *.pyc, .pytest_cache/, .mypy_cache/)

**Checkpoint**: Project structure initialized, ready for foundational code

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Domain Models (Foundation)

- [x] T007 [P] [FOUND] Create src/domain/__init__.py
- [x] T008 [P] [FOUND] Implement TodoTask dataclass in src/domain/models.py (frozen, id, description, is_complete, created_at)
- [x] T009 [P] [FOUND] Implement CommandType enum in src/domain/commands.py (ADD, LIST, COMPLETE, DELETE, HELP, EXIT)
- [x] T010 [P] [FOUND] Implement CommandRequest dataclass in src/domain/commands.py (command_type, task_id, description)
- [x] T011 [P] [FOUND] Implement ValidationResult dataclass in src/domain/validation.py (is_valid, error_message, success/failure factory methods)
- [x] T012 [P] [FOUND] Implement CommandResult dataclass in src/domain/commands.py (success, message, tasks)

### Agent Interfaces (Foundation)

- [x] T013 [P] [FOUND] Create src/agents/__init__.py
- [x] T014 [P] [FOUND] Define StateOwnerInterface Protocol in src/agents/state_owner.py (add_task, list_tasks, complete_task, delete_task, get_task, get_task_count)
- [x] T015 [P] [FOUND] Define ValidationAgentInterface Protocol in src/agents/validation_agent.py (validate_add_command, validate_complete_command, validate_delete_command, validate_list_command, validate_help_command, validate_exit_command)
- [x] T016 [P] [FOUND] Define InterfaceAgentInterface Protocol in src/agents/interface_agent.py (run, display_welcome, parse_input, display_error, display_success, display_tasks, display_help)

### Console Utilities (Foundation)

- [x] T017 [P] [FOUND] Create src/console/__init__.py
- [x] T018 [P] [FOUND] Implement command parser in src/console/parser.py (parse_command function returning tuple[str, list[str]])
- [x] T019 [P] [FOUND] Implement output formatter in src/console/formatter.py (format_task_list, format_error, format_success functions)

### Foundational Tests

- [x] T020 [P] [FOUND] Unit test for TodoTask in tests/unit/test_models.py (creation, immutability, complete method)
- [x] T021 [P] [FOUND] Unit test for ValidationResult in tests/unit/test_validation.py (success/failure factory methods)
- [x] T022 [P] [FOUND] Unit test for command parser in tests/unit/test_parser.py (parse various command formats)
- [x] T023 [P] [FOUND] Unit test for output formatter in tests/unit/test_formatter.py (format task list, errors, success messages)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Todo Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks and view the task list

**Independent Test**: Launch app, add tasks, list them, verify display

### Tests for User Story 1 (Write FIRST, ensure they FAIL)

- [x] T024 [P] [US1] Integration test for add command in tests/integration/test_add_task.py (add task, verify in list)
- [x] T025 [P] [US1] Integration test for list command in tests/integration/test_list_tasks.py (add multiple tasks, list, verify all present)
- [x] T026 [P] [US1] Integration test for empty description validation in tests/integration/test_add_task.py (add empty task, verify error)

### Implementation for User Story 1

- [x] T027 [P] [US1] Implement StateOwner class in src/agents/state_owner.py (add_task, list_tasks methods with dict storage)
- [x] T028 [P] [US1] Implement ValidationAgent class in src/agents/validation_agent.py (validate_add_command, validate_list_command methods)
- [x] T029 [US1] Implement InterfaceAgent class in src/agents/interface_agent.py (run REPL, parse_input, display methods for add/list commands)
- [x] T030 [US1] Create main.py application entry point (initialize agents, start REPL with welcome message per FR-023)
- [x] T031 [US1] Add error handling for invalid commands in InterfaceAgent
- [x] T032 [US1] Add help command display in InterfaceAgent (display_help method)

### Unit Tests for User Story 1

- [x] T033 [P] [US1] Unit test for StateOwner.add_task in tests/unit/test_state_owner.py (task creation, ID allocation, storage)
- [x] T034 [P] [US1] Unit test for StateOwner.list_tasks in tests/unit/test_state_owner.py (empty list, multiple tasks)
- [x] T035 [P] [US1] Unit test for ValidationAgent.validate_add_command in tests/unit/test_validation_agent.py (valid description, empty description, None)
- [x] T036 [P] [US1] Unit test for ValidationAgent.validate_list_command in tests/unit/test_validation_agent.py (always succeeds)
- [x] T037 [P] [US1] Unit test for InterfaceAgent command parsing in tests/unit/test_interface_agent.py (parse add, parse list)

**Checkpoint**: User Story 1 complete - MVP functional with add/list commands

---

## Phase 4: User Story 2 - Mark Tasks as Complete (Priority: P2)

**Goal**: Users can mark tasks as complete and see completion status

**Independent Test**: Create tasks, mark specific ones complete, verify checkmarks in list

### Tests for User Story 2 (Write FIRST, ensure they FAIL)

- [x] T038 [P] [US2] Integration test for complete command in tests/integration/test_complete_task.py (add task, complete it, verify ✓ in list)
- [x] T039 [P] [US2] Integration test for idempotent complete in tests/integration/test_complete_task.py (complete task twice, verify no error)
- [x] T040 [P] [US2] Integration test for complete non-existent task in tests/integration/test_complete_task.py (complete invalid ID, verify error)

### Implementation for User Story 2

- [x] T041 [US2] Implement StateOwner.complete_task method in src/agents/state_owner.py (update task completion status)
- [x] T042 [US2] Implement ValidationAgent.validate_complete_command in src/agents/validation_agent.py (validate task ID format, existence check)
- [x] T043 [US2] Add complete command handling to InterfaceAgent in src/agents/interface_agent.py (parse complete, call validator, call state owner)
- [x] T044 [US2] Update display_tasks in src/console/formatter.py to show ✓ for completed tasks

### Unit Tests for User Story 2

- [x] T045 [P] [US2] Unit test for StateOwner.complete_task in tests/unit/test_state_owner.py (complete pending task, complete already complete task)
- [x] T046 [P] [US2] Unit test for ValidationAgent.validate_complete_command in tests/unit/test_validation_agent.py (valid ID, invalid format, non-existent ID, None)
- [x] T047 [P] [US2] Unit test for InterfaceAgent complete command in tests/unit/test_interface_agent.py (parse complete with ID)

**Checkpoint**: User Story 2 complete - users can mark tasks complete

---

## Phase 5: User Story 3 - Remove Tasks (Priority: P3)

**Goal**: Users can delete tasks from the list

**Independent Test**: Create tasks, delete specific ones, verify removed from list

### Tests for User Story 3 (Write FIRST, ensure they FAIL)

- [x] T048 [P] [US3] Integration test for delete command in tests/integration/test_delete_task.py (add task, delete it, verify not in list)
- [x] T049 [P] [US3] Integration test for delete non-existent task in tests/integration/test_delete_task.py (delete invalid ID, verify error)
- [x] T050 [P] [US3] Integration test for empty list display in tests/integration/test_list_tasks.py (delete all tasks, list, verify "No tasks" message)

### Implementation for User Story 3

- [x] T051 [US3] Implement StateOwner.delete_task method in src/agents/state_owner.py (remove task from dict, maintain ID stability per FR-019)
- [x] T052 [US3] Implement ValidationAgent.validate_delete_command in src/agents/validation_agent.py (validate task ID format, existence check)
- [x] T053 [US3] Add delete command handling to InterfaceAgent in src/agents/interface_agent.py (parse delete, call validator, call state owner)
- [x] T054 [US3] Update display_tasks in src/console/formatter.py to show "No tasks found" when list is empty

### Unit Tests for User Story 3

- [x] T055 [P] [US3] Unit test for StateOwner.delete_task in tests/unit/test_state_owner.py (delete existing task, delete non-existent task, verify ID stability)
- [x] T056 [P] [US3] Unit test for ValidationAgent.validate_delete_command in tests/unit/test_validation_agent.py (valid ID, invalid format, non-existent ID, None)
- [x] T057 [P] [US3] Unit test for InterfaceAgent delete command in tests/unit/test_interface_agent.py (parse delete with ID)

**Checkpoint**: All user stories complete - full CRUD functionality operational

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Quality improvements and cross-cutting concerns

### Edge Cases & Validation

- [ ] T058 [P] Add validation for description length (max 500 chars per research.md) in src/agents/validation_agent.py
- [ ] T059 [P] Add integration test for special characters in description in tests/integration/test_add_task.py
- [ ] T060 [P] Add integration test for extremely long description in tests/integration/test_add_task.py (should reject)
- [ ] T061 [P] Add integration test for rapid consecutive commands in tests/integration/test_command_flows.py

### Help & Exit Commands

- [ ] T062 [P] Implement ValidationAgent.validate_help_command in src/agents/validation_agent.py (always succeeds)
- [ ] T063 [P] Implement ValidationAgent.validate_exit_command in src/agents/validation_agent.py (always succeeds)
- [ ] T064 Add exit command handling to InterfaceAgent with data loss warning per FR-023
- [ ] T065 [P] Add integration test for help command in tests/integration/test_help_exit.py
- [ ] T066 [P] Add integration test for exit command in tests/integration/test_help_exit.py

### Documentation & Quality

- [ ] T067 [P] Add docstrings to all public methods in src/agents/ per constitutional requirement
- [ ] T068 [P] Add docstrings to all public functions in src/console/ per constitutional requirement
- [ ] T069 [P] Run mypy --strict on src/ and fix all type errors
- [ ] T070 [P] Run ruff check src/ and fix all linting issues
- [ ] T071 [P] Run pytest --cov=src --cov-report=term-missing and verify ≥80% coverage
- [ ] T072 Update README.md with actual usage examples and screenshots (console output)
- [ ] T073 [P] Validate quickstart.md instructions work end-to-end (fresh install test)

### Performance & Scale

- [ ] T074 [P] Performance test: verify add/list/complete/delete operations complete in <1 second for 1000 tasks in tests/integration/test_performance.py
- [ ] T075 [P] Performance test: verify startup time <3 seconds in tests/integration/test_performance.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP implementation
- **User Story 2 (Phase 4)**: Depends on Foundational - can run parallel with US1/US3 if desired
- **User Story 3 (Phase 5)**: Depends on Foundational - can run parallel with US1/US2 if desired
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories - **MVP PRIORITY**
- **User Story 2 (P2)**: Can start after Foundational - Integrates with US1 (uses StateOwner.list_tasks) but independently testable
- **User Story 3 (P3)**: Can start after Foundational - Integrates with US1 (uses StateOwner.list_tasks) but independently testable

### Within Each User Story

1. **Tests FIRST**: Write integration tests, verify they FAIL
2. **Implementation**: Implement features to make tests PASS
3. **Unit Tests**: Add unit tests for isolation and edge cases
4. **Checkpoint**: Verify story works independently before moving to next

### Parallel Opportunities

**Phase 1 (Setup)**: T001-T006 all marked [P] can run in parallel

**Phase 2 (Foundational)**:
- T007-T012 (Domain models) can run in parallel
- T013-T016 (Agent interfaces) can run in parallel after domain models
- T017-T019 (Console utilities) can run in parallel with agent interfaces
- T020-T023 (Foundational tests) can run in parallel after implementations

**User Stories** (after Foundational complete):
- US1, US2, US3 can all be worked on in parallel by different developers
- Within each story: Tests can run in parallel, models can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T023) - **CRITICAL**
3. Complete Phase 3: User Story 1 (T024-T037)
4. **STOP and VALIDATE**: Test independently - can add and list tasks
5. Deploy/demo MVP

### Incremental Delivery (Recommended)

1. **Foundation**: Complete Setup + Foundational → Ready for stories
2. **MVP (US1)**: Add/List tasks → Test independently → **Deploy/Demo**
3. **US2**: Complete tasks → Test independently → **Deploy/Demo**
4. **US3**: Delete tasks → Test independently → **Deploy/Demo**
5. **Polish**: Edge cases, help, exit, documentation → Final release

### Parallel Team Strategy

With multiple developers (after Foundational complete):

- **Developer A**: User Story 1 (T024-T037) - MVP priority
- **Developer B**: User Story 2 (T038-T047) - parallel work
- **Developer C**: User Story 3 (T048-T057) - parallel work
- **Team**: Polish together (T058-T075) after stories complete

### TDD Approach (Constitutional Requirement)

For each user story:

1. **RED**: Write integration tests first (verify FAIL)
2. **GREEN**: Implement minimum code to pass tests
3. **REFACTOR**: Add unit tests, improve code quality
4. **VERIFY**: Run full test suite, check coverage ≥80%

---

## Testing Requirements

### Coverage Targets (Constitutional Mandate)

- **Domain logic**: ≥80% coverage REQUIRED
- **Agent implementations**: ≥80% coverage REQUIRED
- **Integration tests**: All critical user flows

### Test Categories

**Unit Tests** (`tests/unit/`):
- Isolated component tests
- Mock dependencies
- Fast execution (<1s total)
- Focus on domain logic and agent methods

**Integration Tests** (`tests/integration/`):
- End-to-end command flows
- Real agent instances (no mocks)
- User scenario validation
- Acceptance criteria verification

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific category
pytest tests/unit/
pytest tests/integration/

# Run for specific user story
pytest -k "test_add" -k "test_list"  # US1
pytest -k "test_complete"            # US2
pytest -k "test_delete"              # US3
```

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to user story for traceability
- **Tests FIRST**: Red-Green-Refactor cycle (TDD)
- **Checkpoints**: Stop and validate after each user story
- **Coverage**: Must achieve ≥80% for domain logic (constitutional requirement)
- **Type hints**: All functions must have type annotations (mypy strict)
- **Docstrings**: All public APIs must be documented (Google/NumPy style)
- **Commits**: Commit after each task or logical group
- **Independence**: Each user story should work independently

### Success Criteria Mapping

Tasks map to Success Criteria from spec.md:

- **SC-001** (add/list in <2s): T074 performance test
- **SC-002** (agent boundaries): T027-T029 implementation + architectural testing
- **SC-003** (all operations work): T024-T057 integration tests
- **SC-004** (1000 tasks, <1s): T074 performance test
- **SC-005** (clear errors): T026, T040, T049 error message tests
- **SC-006** (startup <3s): T075 performance test
- **SC-007** (uv setup): T002, T073 setup validation
- **SC-008** (agent boundaries): Architecture enforced by T014-T016 protocols
- **SC-009** (data destroyed): T066 exit command test
- **SC-010** (clear feedback): T031 error handling + formatter tests

---

## Task Count Summary

- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Foundational)**: 17 tasks (CRITICAL - blocks all stories)
- **Phase 3 (User Story 1 - MVP)**: 14 tasks
- **Phase 4 (User Story 2)**: 10 tasks

- **Phase 5 (User Story 3)**: 10 tasks
- **Phase 6 (Polish)**: 18 tasks

**Total**: 75 tasks

**Estimated Effort**:
- MVP (Phases 1-3): ~2-3 days solo developer
- Full implementation (Phases 1-6): ~4-5 days solo developer
- With parallel team: ~2-3 days total (after Foundation complete)
