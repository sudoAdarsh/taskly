import json
import argparse
from datetime import datetime
from pathlib import Path
from tabulate import tabulate

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tasks.json"

def load_data():
    if not DATA_FILE.exists():
        return {"meta": {"last_id": 0}, "tasks": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open (DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_task(task: dict):
    data = load_data()
    
    data["meta"]["last_id"] += 1
    task["id"] = data["meta"]["last_id"]

    data["tasks"].append(task)
    save_data(data)

    return task


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def sort_key(task):
    due = (datetime.strptime(task["due"], "%Y-%m-%d %H:%M") if task["due"] else datetime.max)
    return (task["priority"], due)

def display_tasks(tasks):
    rows = [
        [
            t["id"],
            t["description"],
            t["status"],
            t["priority"],
            t["due"] or "-",
            t["created_at"],
            t["started_at"] or "-"
        ]
        for t in tasks
    ]
    print(
        tabulate(
            rows,
            headers=["ID", "Description", "Status", "Priority", "Due", "Created at", "Started at"],
            tablefmt="github"
        )
    )

def parse_due_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD HH:MM (e.g. 2025-01-15 13:20)")

def handle_add(args):
    due_date = None
    if args.due:
        due_date = parse_due_date(args.due)
    
    task = {
        "id": None,
        "description": args.description,
        "status": "todo",
        "priority": args.priority,
        "created_at": now(),
        "started_at": None,
        "completed_at": None,
        "due": due_date.strftime("%Y-%m-%d %H:%M") if due_date else None
    }

    saved = add_task(task)
    print(f"Task added with ID {saved['id']}")

def list_tasks():
    data = load_data()
    tasks = data["tasks"]
    active_tasks = [task for task in tasks if task["status"] in ("todo", "in_progress")]
    active_tasks.sort(key=sort_key)
    display_tasks(active_tasks)

def list_task_by_priority():
    data = load_data()
    



parser = argparse.ArgumentParser("to-do app")
subparser = parser.add_subparsers(dest="command")

add = subparser.add_parser("add", help="Add's a new task")
add.add_argument("description", help="Task description")
add.add_argument("--due", help="Setup a due date for the task")
add.add_argument(
    "--priority",
    choices=range(1,5),
    default=3,
    type=int,
    help="Task priority (1=Critical, 2=High, 3=Normal, 4=Low)"
    )


list_ = subparser.add_parser("list", help="list current to-do and in-progress.")
list_.add_argument("--priority", action="store_true", help="list in order of priority")

args = parser.parse_args()

if args.command == "add":
    try:
        handle_add(args)
    except ValueError as e:
        parser.error(str(e))
elif args.command == "list":
    if args.priority:
        list_task_by_priority()
    else:
        list_tasks()
