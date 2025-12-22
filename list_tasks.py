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

        if tasks_to_display == "default":
            # Select headers
            columns = COLUMNS[view]
            headers = [label_title for label_title, label in columns]
            # Select rows
            rows = tuple([label for label_title, label in columns])
            # Fetch data from database
            query = f"SELECT {', '.join(rows)} FROM tasks WHERE status='todo' OR status='in-progress'"
            print(query)
            tasks = cursor.execute(query)
            data = (tasks.fetchall())
            data = [[str(cell) if cell is not None and cell != "" else "-" for cell in row] for row in data]
            print(tabulate(data, headers=headers))
            conn.close()
        