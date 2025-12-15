# import argparse


# def main(command_line=None):
#     parser = argparse.ArgumentParser('Blame Praise app')
#     parser.add_argument(
#         '--debug',
#         action='store_true',
#         help='Print debug info'
#     )
#     subparsers = parser.add_subparsers(dest='command')
#     blame = subparsers.add_parser('blame', help='blame people')
#     blame.add_argument(
#         '--dry-run',
#         help='do not blame, just pretend',
#         action='store_true'
#     )
#     blame.add_argument('name', nargs='+', help='name(s) to blame')
#     praise = subparsers.add_parser('praise', help='praise someone')
#     praise.add_argument('name', help='name of person to praise')
#     praise.add_argument(
#         'reason',
#         help='what to praise for (optional)',
#         default="no reason",
#         nargs='?'
#     )
#     args = parser.parse_args(command_line)
#     if args.debug:
#         print("debug: " + str(args))
#     if args.command == 'blame':
#         if args.dry_run:
#             print("Not for real")
#         print("blaming " + ", ".join(args.name))
#     elif args.command == 'praise':
#         print('praising ' + args.name + ' for ' + args.reason)


# if __name__ == '__main__':
#     main()


import argparse
from datetime import datetime


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
