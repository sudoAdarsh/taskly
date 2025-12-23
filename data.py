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
        due_date = parse_due_date(args.due)
        created_at = datetime.now()

        # Create querry to add task
        query = "INSERT INTO TASKS(description, priority, created_at, due) VALUES(?, ?, ?, ?)"
        cursor.execute(query, (args.description, args.priority, created_at, due_date))

        id_ = cursor.lastrowid
        print(f"New task with id {id_} created.")
        conn.commit()
        conn.close()
        

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
            started_at = datetime.now()
            status = "in-progress"
            query = "UPDATE tasks SET started_at = ?, status = ? WHERE id = ?"
            val = (started_at, status, id_)
            cursor.execute(query, val)
            conn.commit()
            print(f"Task {id_} started at {started_at.strftime("%d-%m-%Y %H:%M")}.")
        
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
            completed_at = datetime.now()
            status = "done"
            query = "UPDATE tasks SET completed_at = ?, status = ? WHERE id = ?"
            val = (completed_at, status, id_)
            cursor.execute(query, val)
            conn.commit()
            print(f"Task {id_} done at {completed_at.strftime("%d-%m-%Y %H:%M")}.")
        
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

        # Check current status
        cursor.execute("SELECT status FROM tasks WHERE id=?",(id_,))
        details = cursor.fetchone()

        # Check if task for that id exists or is already deleted
        if details is None or details[0] =="deleted":
            conn.close()
            raise ValueError(f"No details found for Task id {id_}")

        # Check if task is already completed
        if details[0] =="done":
            conn.close()
            raise ValueError(f"Task {id_} is already marked completed, you can't update it now.")
        
        # Save changes that are made
        changes = []

        # Update description if given
        if desc is not None:
            cursor.execute("UPDATE tasks SET description=? WHERE id=?", (desc,id_))
            conn.commit()
            changes.append(f"Description: {desc}")

        # Update priority if given
        if priority is not None:
            cursor.execute("UPDATE tasks SET priority=? WHERE id=?", (priority,id_))
            conn.commit()
            changes.append(f"Priority: {priority}")

        # Update due if given
        if due is not None:
            due_date = parse_due_date(due)
            cursor.execute("UPDATE tasks SET due=? WHERE id=?", (due_date,id_))
            conn.commit()
            changes.append(f"Due: {due_date.strftime("%d-%m-%Y")}")
        
        print(f"Successfully updated Task {id_}: \n{', '.join(changes)}")
        conn.close()

    # Delete a task
    def delete_task(self, id_):
        # Connect to database
        conn = sqlite3.connect(DATA_FILE)
        cursor = conn.cursor()

        # Check current status
        cursor.execute("SELECT status from tasks WHERE id=?", (id_,))
        status = cursor.fetchone()

        # Check if task exists or is already deleted
        if status is None or status[0] == "deleted":
            conn.close()
            raise ValueError(f"No task with id {id_} found.")
        
        # Ask for confirmation to delete task
        confirm = input(f"Delete Task {id_}? [y/N]: ").strip().lower()
        if not confirm.startswith("y"):
            print("Cancelled")
            conn.close()
            return
        
        # Delete task and update deleted at time
        deleted_at = datetime.now()#.strftime("%d-%m-%Y %H:%M")
        new_status = "deleted"
        cursor.execute("UPDATE tasks SET status=?, deleted_at=? WHERE id=?", (new_status, deleted_at, id_))
        print(f"Task {id_} successfully deleted.")
        conn.commit()
        conn.close()