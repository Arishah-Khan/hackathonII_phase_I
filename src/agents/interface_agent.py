"""Interface Agent implementation.

Agent 2: Handles console I/O and command orchestration.
"""

from src.agents.state_owner import StateOwner
from src.agents.validation_agent import ValidationAgent
from src.console.formatter import format_error, format_success, format_task_list
from src.console.parser import parse_command


class InterfaceAgent:
    """Interface Agent - handles console I/O and command orchestration.

    Responsibilities:
    - Read user input from stdin
    - Parse commands and arguments
    - Route to Validation Agent
    - Route validated commands to State Owner
    - Format and display output

    Prohibitions:
    - No state modification (delegated to State Owner)
    - No validation logic (delegated to Validation Agent)
    - No business rules
    """

    def __init__(
        self, state_owner: StateOwner, validator: ValidationAgent
    ) -> None:
        """Initialize interface agent.

        Args:
            state_owner: State owner for command execution
            validator: Validation agent for command validation
        """
        self._state_owner = state_owner
        self._validator = validator

    def run(self) -> None:
        """Start the interactive console REPL (Read-Eval-Print Loop)."""
        self.display_welcome()

        while True:
            try:
                user_input = input("\n> ")
                command, args = parse_command(user_input)

                if not command:
                    continue

                if command == "exit":
                    validation = self._validator.validate_exit_command()
                    if validation.is_valid:
                        print("\nExiting... All data will be lost.")
                        break
                elif command == "help":
                    validation = self._validator.validate_help_command()
                    if validation.is_valid:
                        self.display_help()
                elif command == "list":
                    validation = self._validator.validate_list_command()
                    if validation.is_valid:
                        tasks = self._state_owner.list_tasks()
                        print(format_task_list(tasks))
                elif command == "add":
                    # Parse title and description from "Title | Description" format
                    full_input = args[0] if args else None
                    title = None
                    description = None

                    if full_input and "|" in full_input:
                        parts = full_input.split("|", 1)
                        title = parts[0].strip() if len(parts) > 0 else None
                        description = parts[1].strip() if len(parts) > 1 else None
                    elif full_input:
                        # If no separator, treat entire input as error
                        print(
                            format_error(
                                "Please use '|' to separate title and description\n"
                                "Example: add Buy Groceries | Get milk, eggs, and bread"
                            )
                        )
                        continue

                    validation = self._validator.validate_add_command(title, description)
                    if validation.is_valid and title and description:
                        task_id = self._state_owner.add_task(title, description)
                        print("\n" + "=" * 70)
                        print("✓ TASK ADDED SUCCESSFULLY!")
                        print("=" * 70)
                        print(f"Task ID     : {task_id}")
                        print(f"Title       : {title.strip()}")
                        print(f"Description : {description.strip()}")
                        print(f"Status      : Pending")
                        print("=" * 70)
                    else:
                        print(format_error(validation.error_message or "Unknown error"))
                elif command == "complete":
                    task_id = args[0] if args else None
                    validation = self._validator.validate_complete_command(task_id)
                    if validation.is_valid and task_id:
                        # Get task details before marking complete
                        task_data = self._state_owner.get_task(task_id)
                        self._state_owner.complete_task(task_id)
                        if task_data:
                            _, title, description, _, _ = task_data
                            print("\n" + "=" * 70)
                            print("✓ TASK MARKED AS COMPLETE!")
                            print("=" * 70)
                            print(f"Task ID     : {task_id}")
                            print(f"Title       : {title}")
                            print(f"Description : {description}")
                            print(f"Status      : Complete")
                            print("=" * 70)
                    else:
                        print(format_error(validation.error_message or "Unknown error"))
                elif command == "delete":
                    task_id = args[0] if args else None
                    validation = self._validator.validate_delete_command(task_id)
                    if validation.is_valid and task_id:
                        # Get task details before deleting
                        task_data = self._state_owner.get_task(task_id)
                        self._state_owner.delete_task(task_id)
                        if task_data:
                            _, title, description, _, _ = task_data
                            print("\n" + "=" * 70)
                            print("✓ TASK DELETED SUCCESSFULLY!")
                            print("=" * 70)
                            print(f"Task ID     : {task_id}")
                            print(f"Title       : {title}")
                            print(f"Description : {description}")
                            print("=" * 70)
                    else:
                        print(format_error(validation.error_message or "Unknown error"))
                elif command == "update":
                    # Parse task_id, title and description from "task_id | Title | Description" format
                    full_input = args[0] if args else None
                    task_id = None
                    title = None
                    description = None

                    if full_input and "|" in full_input:
                        parts = full_input.split("|")
                        if len(parts) >= 3:
                            task_id = parts[0].strip() if parts[0] else None
                            title = parts[1].strip() if parts[1] else None
                            description = parts[2].strip() if parts[2] else None
                        else:
                            print(
                                format_error(
                                    "Please use '|' to separate task ID, title, and description\n"
                                    "Example: update a1b2c3d4 | Shopping | Buy only milk and eggs"
                                )
                            )
                            continue
                    else:
                        print(
                            format_error(
                                "Please use '|' to separate task ID, title, and description\n"
                                "Example: update a1b2c3d4 | Shopping | Buy only milk and eggs"
                            )
                        )
                        continue

                    validation = self._validator.validate_update_command(
                        task_id, title, description
                    )
                    if validation.is_valid and task_id and title and description:
                        self._state_owner.update_task(task_id, title, description)
                        print("\n" + "=" * 70)
                        print("✓ TASK UPDATED SUCCESSFULLY!")
                        print("=" * 70)
                        print(f"Task ID          : {task_id}")
                        print(f"New Title        : {title.strip()}")
                        print(f"New Description  : {description.strip()}")
                        print("=" * 70)
                    else:
                        print(format_error(validation.error_message or "Unknown error"))
                else:
                    print(
                        format_error(
                            f"Unknown command: '{command}'. Type 'help' for available commands."
                        )
                    )

            except KeyboardInterrupt:
                print("\n\nExiting... All data will be lost.")
                break
            except EOFError:
                print("\n\nExiting... All data will be lost.")
                break
            except Exception as e:
                print(format_error(f"An error occurred: {e}"))

    def display_welcome(self) -> None:
        """Display welcome message and data loss warning."""
        print("=" * 42)
        print("Welcome to Todo Console")
        print("=" * 42)
        print("WARNING: All data is in memory only.")
        print("Data will be lost when you exit.")
        print()
        print("Type 'help' for commands or 'exit' to quit.")

    def display_help(self) -> None:
        """Display help information with available commands."""
        print("\n" + "=" * 70)
        print("Available Commands:")
        print("=" * 70)
        print("\n1. ADD - Add a new task")
        print("   Syntax:  add <title> | <description>")
        print("   Example: add Buy Groceries | Get milk, eggs, and bread from store")
        print("")
        print("2. LIST - List all tasks")
        print("   Syntax:  list")
        print("   Example: list")
        print("")
        print("3. UPDATE - Update task title and description")
        print("   Syntax:  update <task_id> | <title> | <description>")
        print("   Example: update a1b2c3d4 | Shopping | Buy only milk and eggs")
        print("")
        print("4. COMPLETE - Mark task as complete")
        print("   Syntax:  complete <task_id>")
        print("   Example: complete a1b2c3d4")
        print("")
        print("5. DELETE - Delete a task")
        print("   Syntax:  delete <task_id>")
        print("   Example: delete a1b2c3d4")
        print("")
        print("6. HELP - Show this help message")
        print("   Syntax:  help")
        print("")
        print("7. EXIT - Exit the application")
        print("   Syntax:  exit")
        print("=" * 70)
