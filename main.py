# TODO get supporing fucntion for parsing date and sorting task

# TODO get sqlite to handle storing data

# TODO add class to manage CRUD operation (ADD, DELETE, EDIT, START, DONE)

# TODO manage displaying , listing task


import argparse
from data import Data
dt = Data()
parser = argparse.ArgumentParser("Taskly")
subparser = parser.add_subparsers(dest="command")

add = subparser.add_parser("add", help="Add's a new task")
add.add_argument("description", help="Task description")
add.add_argument(
    "--due",
    help=(
        "Due date: "
        "N (days), Nd/Nw, YYYY-MM-DD"
        "(default: +1 day)"
    )
)
add.add_argument(
    "--priority",
    choices=range(1,5),
    default=3,
    type=int,
    help="Task priority (1=Critical, 2=High, 3=Normal, 4=Low)")
start = subparser.add_parser("start", help="changes status from todo to in_progress")
start.add_argument("id", help="mention id of task to start", type=int)

done = subparser.add_parser("done", help="changes status to done")
done.add_argument("id", help="mention id of task to mark done", type=int)

args = parser.parse_args()

if args.command == "add":
    try:
        dt.add_task(args)
    except Exception as e:
        parser.error(str(e))
elif args.command == "start":
    try:
        dt.start_task(args.id)
    except Exception as e:
        parser.error(str(e))
elif args.command == "done":
    try:
        dt.done_task(args.id)
    except Exception as e:
        parser.error(str(e))