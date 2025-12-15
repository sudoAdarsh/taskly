import json
import argparse
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("task.json")
def load_data():
    if not DATA_FILE.exists():
        return {} 

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")

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
    print(task)

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
args = parser.parse_args()

if args.command == "add":
    try:
        handle_add(args)
    except ValueError as e:
        parser.error(str(e))
