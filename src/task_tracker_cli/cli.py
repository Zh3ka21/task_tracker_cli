import argparse
from task_tracker_cli.crud import TaskTracker

def cli():
    parser = argparse.ArgumentParser(description="Task CLI Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- add ---
    add_parser = subparsers.add_parser("add", help="Add a task to the list")
    add_parser.add_argument("task", type=str, help="The task to add")
    add_parser.set_defaults(func=lambda args: TaskTracker().add(args.task))

    # --- update ---
    update_parser = subparsers.add_parser("update", help="Update a task's description")
    update_parser.add_argument("task_id", type=str, help="The task ID to identify the task")
    update_parser.add_argument("task_name", type=str, help="The new task name")
    update_parser.set_defaults(func=lambda args: TaskTracker().update(args.task_id, args.task_name))
    
    # --- delete ---
    delete_parser = subparsers.add_parser("delete", help="Delete task")
    delete_parser.add_argument("task_id", type=str, help="The task ID to identify the task")
    delete_parser.set_defaults(func=lambda args: TaskTracker().delete(args.task_id))
    
    # --- mark ---
    mark_done = subparsers.add_parser("mark", help="Mark task")
    mark_done.add_argument("task_id", type=str, help="The task ID to identify the task")
    mark_done.add_argument("status", type=str, help="Mark task done, in-progress, todo")
    
    mark_done.set_defaults(func=lambda args: TaskTracker().mark(args.task_id, args.status))
        
    # --- list (with subcommands) ---
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument(
        "status",
        type=str,
        nargs="?",
        default="",
        help="Choose: done, in-progress, todo. Leave empty to list all tasks."
    )
    list_parser.set_defaults(func=lambda args: TaskTracker().listing(args.status))

    # Parse args and run associated function
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
