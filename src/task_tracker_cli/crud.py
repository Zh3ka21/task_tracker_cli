import json
import os
import datetime
import pprint
import uuid

from dotenv import load_dotenv
from task_tracker_cli.const import STATUS_MARK_TODO, STATUS_MARK_DONE, STATUS_MARK_INPROGRESS

load_dotenv()

class TaskTracker:
    def __init__(self):
        """Initialize TaskTracker with data loaded from DB or create a new one."""
        self.db: dict = self._load_db()
        if self.db is None:
            self.db = self._create_db()

    # Internal methods 
    def _build_task(self, task_name: str, id: str, status: str = "todo", description: str = "") -> dict:
        """Builds a task dictionary with metadata."""
        task_schema = {
            f"{task_name}": {
                "id": id,
                "description": description,
                "status": status,
                "created_at": str(datetime.datetime.now()),
                "updated_at": str(datetime.datetime.now()),
            },
        }
        return task_schema

    def _create_db(self):
        """Create the JSON DB file if it doesn't exist."""
        try:
            with open(os.getenv('DB_STRING'), "w") as f:
                json.dump({}, f)
            return self._load_db()
        except Exception:
            return None

    def _load_db(self):
        """Load and return the contents of the DB file."""
        try:
            with open(os.getenv('DB_STRING'), "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def _push_db(self, task_name: str, id: int):
        task = self._build_task(task_name, id)
        self.db = self._load_db()          
        ndata = self.db[task_name] = task
        with open(os.getenv('DB_STRING'), "w") as f:
            json.dump({**self.db, **ndata}, f)
        self.db = ndata

    def _find_tasks_by_partial_id(self, partial_id: str):
        """Search tasks by prefix of ID. Returns exact match or informs of ambiguity."""
        matched = [
            (task_name, task_data)
            for task_name, task_data in self.db.items()
            if task_data["id"].startswith(partial_id)
        ]

        if not matched:
            print(f"No task found starting with ID: {partial_id}")
            return None

        if len(matched) > 1:
            print(f"Multiple tasks match ID '{partial_id}':")
            for task_name, task_data in matched:
                print(f"  - {task_name} → {task_data['id']}")
            return None

        return matched[0]

    def _query(self, status: str = ""):
        """Display tasks filtered by status, if provided."""
        counter = 0
        status = status.lower()
        if status not in ("", STATUS_MARK_TODO, STATUS_MARK_DONE, STATUS_MARK_INPROGRESS):
            print(f"Status is incorrect. Use one of: {(STATUS_MARK_TODO, STATUS_MARK_DONE, STATUS_MARK_INPROGRESS)}")
            return

        for task, details in self.db.items():
            if not status or details.get("status") == status:
                pprint.pprint(f"{task}: {details}")
                counter += 1

        if counter < 1:
            print("Such tasks weren't found")

    # CRUD operations
    def add(self, task: str):
        """Add a new task if it does not already exist."""
        if self.db.get(task, None) is None:
            new_id = str(uuid.uuid4())
            self._push_db(task, new_id)
            print(f"Output: Task added successfully (ID: {new_id})")
        else:
            print("Output: Task with such name already exists.")

    def update(self, partial_id: str, new_task_name: str):
        """Rename an existing task based on ID prefix."""
        self.db = self._load_db()
        match = self._find_tasks_by_partial_id(partial_id)
        if match is None:
            return

        old_name, task_data = match
        self.db[new_task_name] = self.db.pop(old_name)
        self.db[new_task_name]["updated_at"] = str(datetime.datetime.now())
        print(f"Renamed task '{old_name}' to '{new_task_name}'")

        with open(os.getenv('DB_STRING'), "w") as f:
            json.dump(self.db, f)

    def delete(self, partial_id: str):
        """Delete task using ID prefix."""
        self.db = self._load_db()
        match = self._find_tasks_by_partial_id(partial_id)
        if match is None:
            return

        old_name, _ = match
        del self.db[old_name]
        print(f"Deleted task '{old_name}'")

        with open(os.getenv('DB_STRING'), "w") as f:
            json.dump(self.db, f)

    def mark(self, partial_id: str, status: str):
        """Change task status (todo, done, in-progress) using ID prefix."""
        self.db = self._load_db()
        match = self._find_tasks_by_partial_id(partial_id)
        if match is None:
            return

        status = status.lower()
        if status not in (STATUS_MARK_TODO, STATUS_MARK_DONE, STATUS_MARK_INPROGRESS):
            print(f"Status is incorrect. Use one of: {(STATUS_MARK_TODO, STATUS_MARK_DONE, STATUS_MARK_INPROGRESS)}")
            return

        old_name, task_data = match
        self.db[old_name]["status"] = status
        self.db[old_name]["updated_at"] = str(datetime.datetime.now())
        print(f"Marked task '{old_name}' {status}")

        with open(os.getenv('DB_STRING'), "w") as f:
            json.dump(self.db, f)

    def listing(self, status: str):
        """List tasks by given status or all if blank."""
        self.db = self._load_db()
        self._query(status)
