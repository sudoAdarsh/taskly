import json
import argparse
from datetime import datetime
from pathlib import Path
from tabulate import tabulate

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "tasks.json"

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

def get_task_by_id(tasks, id_):
    for task in tasks:
        if task["id"] == id_:
            return task
    return None

def start_task(id_: int):
    data = load_data()
    tasks = data["tasks"]
    task = get_task_by_id(tasks, id_)
    if not task or task["status"] == "deleted":
        raise IndexError(f"No task with id {id_}")
    if task["status"] == "todo":
        task["started_at"] = now()
        task["status"] = "in_progress"
        save_data(data)
        print(f"Task {id_}. {task["description"]} is now in progress.")
        return 
    elif task["status"] == "in_progress":
        raise Exception(f"Task {id_}. {task["description"]} is already in progress.")
    elif task["status"] == "done":
        raise Exception(f"Task {id_}. {task["description"]} is completed.")

def done_task(id_: int):
    data = load_data()
    tasks = data["tasks"]
    task = get_task_by_id(tasks, id_)
    if not task or task["status"] == "deleted":
        raise IndexError(f"No task with id {id_}")
    if task["status"] != "done":
        task["completed_at"] = now()
        task["status"] = "done"
        save_data(data)
        print(f"Task {id_}. {task["description"]} is now completed.")
        return
    elif task["status"] == "done":
        raise Exception(f"Task {id_}. {task["description"]} is already completed.")

def update_task(id_: int, description=None, due=None, priority=None):
    data = load_data()
    tasks = data["tasks"]
    task = get_task_by_id(tasks, id_)
    if not task or task["status"] == "deleted":
        raise IndexError(f"No task with id {id_}")
    if description is None and due is None and priority is None:
        raise ValueError("Nothing to update")
    changes = []
    if description is not None:
        task["description"] = description
        changes.append(f"Description: {description}")
    if due is not None:
        task["due"] = parse_due_date(due).strftime("%Y-%m-%d %H:%M")
        changes.append(f"Due: {due}")
    if priority is not None:
        task["priority"] = priority
        changes.append(f"Priority: {priority}")
    print(f"Successfully updated Task {id_}: \n{', '.join(changes)}")
    save_data(data)

def delete_task(id_: int):
    data = load_data()
    tasks = data["tasks"]
    task = get_task_by_id(tasks, id_)
    if not task:
        raise IndexError(f"No task with id {id_}")
    confirm = input(f"Delete Task {id_}? [y/N]: ")
    if confirm.lower() != "y":
        print("Cancelled")
        return
    if task["status"] == "deleted":
        raise ValueError(f"Task {id_}. {task["description"]} already deleted.")
    else:
        task["deleted_at"] = now()
        task["status"] = "deleted"
        save_data(data)
        print(f"Task {id_}. {task["description"]} is now deleted.")
        return

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

def sort_key(task):
    status_values = {
        "in_progress": 1,
        "todo": 2,
        "done": 3,
        "deleted": 4
    }
    status = status_values[task["status"]]
    due = (datetime.strptime(task["due"], "%Y-%m-%d %H:%M") if task["due"] else datetime.max)
    priority = task["priority"]
    return (status, priority, due)

def display_tasks(tasks, view="default"):
    columns = COLUMNS[view]

    headers = [label_title for label_title, label in columns]
    rows = []

    for task in tasks:
        row = []
        for _, key in columns:
            value = task.get(key)
            row.append(value if value is not None else "-")
        rows.append(row)
    print(
        tabulate(
            rows,
            headers=headers,
            tablefmt="pretty"
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
        "due": due_date.strftime("%Y-%m-%d %H:%M") if due_date else None,
        "deleted_at": None
    }
    saved = add_task(task)
    print(f"Task added with ID {saved['id']}")

def list_tasks():
    data = load_data()
    tasks = data["tasks"]
    current_tasks = [task for task in tasks if task["status"] in ("todo", "in_progress")]
    current_tasks.sort(key=sort_key)
    display_tasks(current_tasks)

def list_all_tasks():
    data = load_data()
    tasks = data["tasks"]
    all_tasks = [task for task in tasks if task["status"] != "deleted"]
    all_tasks.sort(key=sort_key)
    display_tasks(all_tasks, view="all")

def list_todo_tasks():
    data = load_data()
    tasks = data["tasks"]
    todo_tasks = [task for task in tasks if task["status"] == "todo"]
    todo_tasks.sort(key=sort_key)
    display_tasks(todo_tasks)

def list_active_tasks():
    data = load_data()
    tasks = data["tasks"]
    active_tasks = [task for task in tasks if task["status"] == "in_progress"]
    active_tasks.sort(key=sort_key)
    display_tasks(active_tasks, view="active")

def list_done_tasks():
    data = load_data()
    tasks = data["tasks"]
    done_tasks = [task for task in tasks if task["status"] == "done"]
    done_tasks.sort(key=sort_key)
    display_tasks(done_tasks, view="all")

def list_deleted_tasks():
    data = load_data()
    tasks = data["tasks"]
    deleted_tasks = [task for task in tasks if task["status"] == "deleted"]
    deleted_tasks.sort(key=sort_key)
    display_tasks(deleted_tasks, view="del")

def sort_key_by_priority(task):
    priority = task["priority"]
    return (priority)

def list_task_by_priority():
    data = load_data()
    tasks = data["tasks"]
    tasks_by_priority = [task for task in tasks if task["status"] in ("todo", "in_progress")]
    tasks_by_priority.sort(key=sort_key_by_priority)
    display_tasks(tasks_by_priority)



parser = argparse.ArgumentParser("tTaskly")
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

update = subparser.add_parser("update", help="Update task fields")
update.add_argument("id", type=int, help="Id of task to be updated")
update.add_argument("--description", help="Task description")
update.add_argument("--due", help="Setup a due date for the task")
update.add_argument(
    "--priority",
    choices=range(1,5),
    default=None,
    type=int,
    help="Task priority (1=Critical, 2=High, 3=Normal, 4=Low)"
    )

delete = subparser.add_parser("delete", help="delete task")
delete.add_argument("id", type=int, help="Id of task to be deleted")

list_ = subparser.add_parser("list", help="list current to-do and in-progress.")
list_.add_argument("-p", "--priority", action="store_true", help="list in order of priority")
list_.add_argument("-a", "--all", action="store_true", help="list all tasks")
list_.add_argument("-d", "--done", action="store_true", help="list completed tasks")
list_.add_argument("-c", "--active", action="store_true", help="list active tasks")
list_.add_argument("-t", "--todo", action="store_true", help="list remaing todo's")
list_.add_argument("-q", "--deleted", action="store_true", help="list deleted tasks")


start = subparser.add_parser("start", help="changes status from todo to in_progress")
start.add_argument("id", help="mention id of task to start", type=int)

done = subparser.add_parser("done", help="changes status to done")
done.add_argument("id", help="mention id of task to mark done", type=int)

args = parser.parse_args()

if args.command is None:
    list_tasks()

if args.command == "add":
    try:
        handle_add(args)
    except ValueError as e:
        parser.error(str(e))
elif args.command == "list":
    if args.priority:
        list_task_by_priority()
    elif args.all:
        list_all_tasks()
    elif args.done:
        list_done_tasks()
    elif args.active:
        list_active_tasks()
    elif args.todo:
        list_todo_tasks()
    elif args.deleted:
        list_deleted_tasks()
    else:
        list_tasks()
elif args.command == "start":
    try:
        start_task(args.id)
    except Exception as e:
        parser.error(str(e))
elif args.command == "done":
    try:
        done_task(args.id)
    except Exception as e:
        parser.error(str(e))
elif args.command == "update":
    try:
        update_task(id_=args.id, description=args.description, due=args.due, priority=args.priority)
    except Exception as e:
        parser.error(str(e))
elif args.command == "delete":
    try:
        delete_task(id_=args.id)
    except Exception as e:
        parser.error(str(e))