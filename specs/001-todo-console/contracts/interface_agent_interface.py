"""
Interface Agent Interface Contract

This module defines the interface contract for Agent 2 (Interface Agent).
The Interface Agent is responsible for:
- Reading user input from console (stdin)
- Parsing input into commands
- Routing commands to Validation Agent and State Owner
- Formatting output for console display (stdout/stderr)

The Interface Agent MUST NOT:
- Modify state directly (must go through State Owner)
- Perform validation logic (delegated to Validation Agent)
- Contain business rules (delegated to domain layer)

The Interface Agent is the only component that performs I/O operations.
"""

from typing import Protocol


class InterfaceAgentInterface(Protocol):
    """Protocol defining the Interface Agent's public interface.

    The Interface Agent orchestrates the command flow:
    1. Read and parse user input
    2. Route to Validation Agent for validation
    3. If valid, route to State Owner for execution
    4. Format and display result to user
    """

    def run(self) -> None:
        """Start the interactive console REPL (Read-Eval-Print Loop).

        Lifecycle:
            1. Display welcome message and data loss warning (FR-023)
            2. Enter REPL loop:
               - Read user input
               - Parse into command
               - Validate via Validation Agent
               - Execute via State Owner (if valid)
               - Display result
            3. Exit on 'exit' command or EOF

        Side Effects:
            - Reads from stdin
            - Writes to stdout/stderr
            - Blocks until user exits

        Example:
            >>> interface_agent = InterfaceAgent(state_owner, validator)
            >>> interface_agent.run()
            Welcome to Todo Console
            WARNING: All data is stored in memory and will be lost on exit.

            > add Buy groceries
            Task added: [1] Buy groceries

            > list
            Tasks:
              [1] Buy groceries

            > exit
            Exiting... All data will be lost.
        """
        ...

    def display_welcome(self) -> None:
        """Display welcome message and data loss warning.

        Outputs:
            - Application title
            - Warning about in-memory storage (constitutional requirement FR-023)
            - Brief usage instructions or 'help' command reference

        Side Effects:
            - Writes to stdout

        Example:
            >>> interface_agent.display_welcome()
            ==========================================
            Welcome to Todo Console
            ==========================================
            WARNING: All data is in memory only.
            Data will be lost when you exit.

            Type 'help' for commands or 'exit' to quit.
        """
        ...

    def parse_input(self, user_input: str) -> tuple[str, list[str]]:
        """Parse user input string into command and arguments.

        Args:
            user_input: Raw input string from user

        Returns:
            Tuple of (command_verb, arguments_list)
            - command_verb: First word (lowercased)
            - arguments_list: Remaining words/text

        Example:
            >>> verb, args = interface_agent.parse_input("add Buy groceries")
            >>> verb
            "add"
            >>> args
            ["Buy", "groceries"]

            >>> verb, args = interface_agent.parse_input("list")
            >>> verb
            "list"
            >>> args
            []
        """
        ...

    def display_error(self, message: str) -> None:
        """Display error message to user.

        Args:
            message: Error message text

        Side Effects:
            - Writes to stderr (preferred for errors) or stdout

        Example:
            >>> interface_agent.display_error("Task ID '99' not found")
            Error: Task ID '99' not found
        """
        ...

    def display_success(self, message: str) -> None:
        """Display success message to user.

        Args:
            message: Success message text

        Side Effects:
            - Writes to stdout

        Example:
            >>> interface_agent.display_success("Task added successfully")
            Task added successfully
        """
        ...

    def display_tasks(self, tasks: list[tuple[int, str, bool, object]]) -> None:
        """Display task list in formatted console output.

        Args:
            tasks: List of task tuples (id, description, is_complete, created_at)

        Side Effects:
            - Writes formatted task list to stdout
            - Displays "No tasks" message if list empty

        Example:
            >>> tasks = [(1, "Buy groceries", False, datetime.now()),
            ...          (2, "Write report", True, datetime.now())]
            >>> interface_agent.display_tasks(tasks)
            Tasks:
              [1] Buy groceries
              [2] ✓ Write report

            >>> interface_agent.display_tasks([])
            No tasks found.
        """
        ...

    def display_help(self) -> None:
        """Display help information with available commands.

        Side Effects:
            - Writes command usage information to stdout

        Example:
            >>> interface_agent.display_help()
            Available Commands:
              add <description>    - Add a new task
              list                 - List all tasks
              complete <task_id>   - Mark task as complete
              delete <task_id>     - Delete a task
              help                 - Show this help message
              exit                 - Exit the application
        """
        ...


# Interface contract specification
CONTRACT_VERSION = "1.0.0"
CONTRACT_DESCRIPTION = "Interface Agent interface for console I/O and command orchestration"

# Display formatting constants
WELCOME_BANNER = "=" * 42
TASK_COMPLETE_SYMBOL = "✓"
TASK_INCOMPLETE_SYMBOL = " "

# Command syntax patterns
COMMAND_ADD = "add <description>"
COMMAND_LIST = "list"
COMMAND_COMPLETE = "complete <task_id>"
COMMAND_DELETE = "delete <task_id>"
COMMAND_HELP = "help"
COMMAND_EXIT = "exit"

# Constitutional compliance notes:
# - Only component that performs I/O (print/input)
# - No state modification logic (delegates to State Owner)
# - No validation logic (delegates to Validation Agent)
# - Type hints on all methods (constitutional requirement)
# - Console-only interface (no GUI/web frameworks)
