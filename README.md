# task_tracker_cli# Task Tracker CLI

A simple and efficient command-line task management tool built with Python. Manage your tasks directly from the terminal with easy-to-use commands.

## Features

- ✅ **Add tasks** - Quickly add new tasks to your list
- ✏️ **Update tasks** - Modify existing task descriptions
- 🗑️ **Delete tasks** - Remove tasks you no longer need
- 📋 **List tasks** - View all tasks or filter by status
- 🏷️ **Mark task status** - Set tasks as todo, in-progress, or done

## Installation

This project uses Poetry for dependency management. Make sure you have Poetry installed on your system.

### Prerequisites

- Python 3.10.12+
- Poetry

### Install Poetry (if not already installed)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Clone and Install

```bash
git clone https://github.com/Zh3ka21/task_tracker_cli
cd task-tracker-cli
poetry install
```

## Usage

After installation, you can use the task tracker with the following commands:

### Add a Task

```bash
poetry run task-tracker add "Buy groceries"
```

### List Tasks

```bash
# List all tasks
poetry run task-tracker list

# List tasks by status
poetry run task-tracker list todo
poetry run task-tracker list in-progress
poetry run task-tracker list done
```

### Update a Task

```bash
poetry run task-tracker update <task_id> "Updated task description"
```

### Mark Task Status

```bash
# Mark as done
poetry run task-tracker mark <task_id> done

# Mark as in-progress
poetry run task-tracker mark <task_id> in-progress

# Mark as todo
poetry run task-tracker mark <task_id> todo
```

### Delete a Task

```bash
poetry run task-tracker delete <task_id>
```

### Get Help

```bash
poetry run task-tracker --help
```

## Project Structure

```
task-tracker-cli/
├── task_tracker_cli/
│   ├── __init__.py
│   ├── cli.py          # CLI interface and argument parsing
│   ├── cli.py
│   └── crud.py         # TaskTracker class with CRUD operations
├── pyproject.toml      # Poetry configuration and dependencies
└── README.md          # This file
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/Zh3ka21/task_tracker_cli
cd task-tracker-cli

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Running Tests

```bash
poetry run pytest
```

## Configuration

The project uses `pyproject.toml` for configuration. Make sure your `pyproject.toml` includes the CLI script entry point:

```toml
[tool.poetry.scripts]
task-tracker = "task_tracker_cli.cli:cli"
```

## Task Status Options

- **todo** - Task is pending and not started
- **in-progress** - Task is currently being worked on
- **done** - Task is completed

## Examples

```bash
# Add some tasks
poetry run task-tracker add "Learn Python"
poetry run task-tracker add "Build CLI app"
poetry run task-tracker add "Write documentation"

# Check all tasks
poetry run task-tracker list

# Mark a task as in-progress
poetry run task-tracker mark <task_id> in-progress

# Update task description
poetry run task-tracker update <task_id> "Build awesome CLI app"

# Mark task as done
poetry run task-tracker mark <task_id> done

# List only completed tasks
poetry run task-tracker list done

# Delete a task
poetry run task-tracker delete <task_id>
```

## Idea taken from

<https://roadmap.sh/projects/task-tracker>

---

**Happy task tracking! 🚀**
