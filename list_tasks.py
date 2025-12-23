from tabulate import tabulate
from pathlib import Path
from datetime import datetime
import sqlite3

# makes sure our tasks.db will be in project directory
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR/"task.db"

COLUMNS = {
    "default": [
        ("ID", "id", "int"),
        ("Description", "description", "text"),
        ("Status", "status", "text"),
        ("Priority", "priority", "int"),
        ("Due", "due", "datetime"),
    ],
    "active": [
        ("ID", "id", "int"),
        ("Description", "description", "text"),
        ("Status", "status", "text"),
        ("Priority", "priority", "int"),
        ("Due", "due", "datetime"),
        ("Started at", "started_at", "datetime"),
    ],
    "all": [
        ("ID", "id", "int"),
        ("Description", "description", "text"),
        ("Status", "status", "text"),
        ("Priority", "priority", "int"),
        ("Due", "due", "datetime"),
        ("Created at", "created_at", "datetime"),
        ("Started at", "started_at", "datetime"),
        ("Completed at", "completed_at", "datetime"),
    ],
    "del": [
        ("ID", "id", "int"),
        ("Description", "description", "text"),
        ("Status", "status", "text"),
        ("Priority", "priority", "int"),
        ("Due", "due", "datetime"),
        ("Created at", "created_at", "datetime"),
        ("Started at", "started_at", "datetime"),
        ("Completed at", "completed_at", "datetime"),
        ("Deleted at", "deleted_at", "datetime"),
    ]
}

DEFAULT_ORDER = """
ORDER BY
    CASE status
        WHEN 'in-progress' THEN 1
        WHEN 'todo'        THEN 2
        WHEN 'done'        THEN 3
        WHEN 'deleted'     THEN 4
    END,
    priority ASC,
    due ASC
"""

DISPLAY_DATE_FMT = "%d-%m-%Y %H:%M"

# used to format cells if they are null and make dates more human readable
def format_cell(value, col_type):
    if value is None or value == "":
        return "-"
    if col_type == "datetime":
        return datetime.fromisoformat(value).strftime(DISPLAY_DATE_FMT)
    return str(value)

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
        headers = [label_title for label_title, _, _ in columns]

        # Select rows
        rows = tuple([label for _, label, _ in columns])

        # Fetch data from database
        if tasks_to_display == "default":
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status IN ('todo', 'in-progress') {DEFAULT_ORDER}"

        elif tasks_to_display == "all":  # List all tasks
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status IN ('todo', 'in-progress', 'done') {DEFAULT_ORDER}"

        elif tasks_to_display == "done": # List completed tasks
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='done' {DEFAULT_ORDER}"

        elif tasks_to_display == "active":  # List active tasks
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='in-progress' {DEFAULT_ORDER}"

        elif tasks_to_display == "todo":  # List todo's
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='todo' {DEFAULT_ORDER}"

        elif tasks_to_display == "deleted": # List deleted tasks
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='deleted' {DEFAULT_ORDER}"

        elif tasks_to_display == "priority":  # List by priority
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status IN ('todo', 'in-progress') ORDER BY priority"

        elif tasks_to_display == "due":  # List by due dates
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status IN ('todo', 'in-progress') ORDER BY due"

        # Execute querry
        tasks = cursor.execute(query)

        # produces data so null is replaced by '-' and dates become more readable which then can be tabulated
        data = (tasks.fetchall())

        formatted_data = []
        for row in data:
            formatted_row = []
            for cell, (_, _, col_type) in zip(row, columns):
                formatted_row.append(format_cell(cell, col_type))
            formatted_data.append(formatted_row)

        # Print in tabular form
        print(tabulate(formatted_data, headers=headers, tablefmt="pretty"))
        conn.close()