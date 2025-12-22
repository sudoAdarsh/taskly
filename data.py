import sqlite3
from pathlib import Path
from support import parse_due_date, datetime

# makes sure our tasks.db will be in project directory
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR/"task.db"

class Data:
    def __init__(self):
        conection = sqlite3.connect(DATA_FILE)
        cur = conection.cursor()

        # Create table is not laready present
        cur.execute(
            "CREATE TABLE IF NOT EXISTS tasks (" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "description TEXT," \
            "status TEXT DEFAULT 'todo'," \
            "priority INTEGER," \
            "created_at TEXT," \
            "started_at TEXT," \
            "completed_at TEXT," \
            "due TEXT," \
            "deleted_at TEXT)"
        )
        conection.commit()
        conection.close()

    # Add a new task 
    def add_task(self, args):
        # Connect to database
        conn = sqlite3.connect(DATA_FILE)
        cursor = conn.cursor()

        # Format due date and creation date
        due_date = parse_due_date(args.due).strftime("%d-%m-%Y %H:%M")
        created_at = datetime.now().strftime("%d-%m-%Y %H:%M")

        # Create querry to add task
        query = "INSERT INTO TASKS(description, priority, created_at, due) VALUES(?, ?, ?, ?)"
        cursor.execute(query, (args.description, args.priority, created_at, due_date))

        # new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        # return new_id

    # Start a new task
    def start_task(self, id_):
        # Connect to database
        conn = sqlite3.connect(DATA_FILE)
        cursor = conn.cursor()

        # Check current status
        cursor.execute("SELECT status FROM tasks WHERE id = ?", (id_,))
        current_status = cursor.fetchone()
        if current_status is None:
            conn.close()
            raise ValueError(f"No task with id {id_} found.")

        # Extract status from current status tuple
        current_status = current_status[0]
        
        # if task is todo
        if current_status == "todo":
            # format start date and change status from todo to in-progress
            started_at = datetime.now().strftime("%d-%m-%Y %H:%M")
            status = "in-progress"
            query = "UPDATE tasks SET started_at = ?, status = ? WHERE id = ?"
            val = (started_at, status, id_)
            cursor.execute(query, val)
            conn.commit()
            print(f"Task {id_} has been started at {started_at}.")
        
        # if task is already in-progress
        elif current_status == "in-progress":
            raise ValueError("Task is already in progress.")
        
        # if task is already completed
        elif current_status == "done":
            raise ValueError("Task is already completed.")
        
        else:
            raise ValueError(f"No active task with ID {id_}.")
        conn.close()

    # mark a task completed.
    def done_task(self, id_):
        # Connect to database
        conn = sqlite3.connect(DATA_FILE)
        cursor = conn.cursor()

        # Check current status
        cursor.execute("SELECT status FROM tasks WHERE id = ?", (id_,))
        current_status = cursor.fetchone()
        if current_status is None:
            conn.close()
            raise ValueError(f"No task with id {id_} found.")

        # Extract status from current status tuple
        current_status = current_status[0]
        
        # if current status is todo or in-progress mark task is complete
        if current_status == "todo" or current_status == "in-progress":
            # format completed date and change status to done
            completed_at = datetime.now().strftime("%d-%m-%Y %H:%M")
            status = "done"
            query = "UPDATE tasks SET completed_at = ?, status = ? WHERE id = ?"
            val = (completed_at, status, id_)
            cursor.execute(query, val)
            conn.commit()
            print(f"Task {id_} has been marked done at {completed_at}.")
        
        # if task is already completed
        elif current_status == "done":
            raise ValueError("Task is already completed.")
        
        else:
            raise ValueError(f"No active task with ID {id_}.")
        conn.close()
    
    # Update a task
    def update_task(self, id_:int, desc=None, priority=None, due=None):
        # Connect to database
        conn = sqlite3.connect(DATA_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT description, priority, due FROM tasks WHERE id=?",(id_,))
        details = cursor.fetchone()
        if details is None:
            conn.close()
            raise ValueError("No details found")
        print(details)
