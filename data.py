import sqlite3
from pathlib import Path
from support import parse_due_date, datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR/"task.db"

class Data:
    def __init__(self):
        conection = sqlite3.connect(DATA_FILE)
        cur = conection.cursor()
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
    def add_task(self, args):
        due_date = parse_due_date(args.due).strftime("%d-%m-%Y")
        created_at = datetime.now().strftime("%d-%m-%Y")
        conn = sqlite3.connect(DATA_FILE)
        cursor = conn.cursor()
        query = "INSERT INTO TASKS(description, priority, created_at, due) VALUES(?, ?, ?, ?)"
        cursor.execute(query, (args.description, args.priority, created_at, due_date))
        new_id = cursor.lastrowid
        a = cursor.execute("SELECT * FROM tasks")
        print(a.fetchall())
        conn.commit()
        conn.close()
        return new_id