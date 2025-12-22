from tabulate import tabulate
from pathlib import Path
import sqlite3

# makes sure our tasks.db will be in project directory
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR/"task.db"

COLUMNS = {
    "default": [
        ("ID", "id"),
        ("Description", "description"),
        ("Status", "status"),
        ("Priority", "priority"),
        ("Due", "due"),
    ],
    "active": [
        ("ID", "id"),
        ("Description", "description"),
        ("Status", "status"),
        ("Priority", "priority"),
        ("Due", "due"),
        ("Started at", "started_at"),
    ],
    "all": [
        ("ID", "id"),
        ("Description", "description"),
        ("Status", "status"),
        ("Priority", "priority"),
        ("Due", "due"),
        ("Created at", "created_at"),
        ("Started at", "started_at"),
        ("Completed at", "completed_at"),
    ],
    "del": [
        ("ID", "id"),
        ("Description", "description"),
        ("Status", "status"),
        ("Priority", "priority"),
        ("Due", "due"),
        ("Created at", "created_at"),
        ("Started at", "started_at"),
        ("Completed at", "completed_at"),
        ("Deleted at", "deleted_at"),
    ]
}

class List:
    def __init__(self):
        pass
    # list tasks
    def list_task(self, tasks_to_display="default", view="default"):
        # build connection
        conn = sqlite3.connect(DATA_FILE)
        cursor = conn.cursor()

        # Select headers
        columns = COLUMNS[view]
        headers = [label_title for label_title, label in columns]

        # Select rows
        rows = tuple([label for label_title, label in columns])

        # Fetch data from database
        if tasks_to_display == "default":
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='todo' OR status='in-progress'"

        elif tasks_to_display == "all":  # List all tasks
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='todo' OR status='in-progress' OR status='done'"
        elif tasks_to_display == "done":
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='done'"
        elif tasks_to_display == "active":
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='in-progress'"
        elif tasks_to_display == "todo":
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='todo'"
        elif tasks_to_display == "deleted":
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='deleted'"
        elif tasks_to_display == "priority":
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='todo' OR status='in-progress' ORDER BY priority"

        # Execute querry
        tasks = cursor.execute(query)

        # Format data so null is replaced by '-'
        data = (tasks.fetchall())
        data = [[str(cell) if cell is not None and cell != "" else "-" for cell in row] for row in data]

        # Print in tabular form
        print(tabulate(data, headers=headers, tablefmt="pretty"))
        conn.close()