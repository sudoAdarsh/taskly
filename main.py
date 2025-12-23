# TODO get supporing fucntion for parsing date and sorting task

# TODO get sqlite to handle storing data

# TODO add class to manage CRUD operation (ADD, DELETE, EDIT, START, DONE)

# TODO manage displaying , listing task

import argparse
from list_tasks import List
from data import Data

li = List()
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
group = list_.add_mutually_exclusive_group()
group.add_argument("-p", "--priority", action="store_true", help="list in order of priority")
group.add_argument("-u", "--due", action="store_true", help="list in order of due nearing")
group.add_argument("-a", "--all", action="store_true", help="list all tasks")
group.add_argument("-d", "--done", action="store_true", help="list completed tasks")
group.add_argument("-c", "--active", action="store_true", help="list active tasks")
group.add_argument("-t", "--todo", action="store_true", help="list remaing todo's")
group.add_argument("-q", "--deleted", action="store_true", help="list deleted tasks")


args = parser.parse_args()

if args.command is None:
    li.list_task()

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
elif args.command == "update":
    try:
        dt.update_task(id_=args.id, desc=args.description, priority=args.priority, due=args.due)
    except Exception as e:
        parser.error(str(e))
elif args.command == "delete":
    try:
        dt.delete_task(id_=args.id)
    except Exception as e:
        parser.error(str(e))
elif args.command == "list":
    if args.priority:
        li.list_task(tasks_to_display="priority") # list deafualt task but based on priority ; default
    elif args.due:
        li.list_task(tasks_to_display="due") # list deafualt task but based on due ; default
    elif args.all:
        li.list_task(tasks_to_display="all", view="all") # list todo, in-progress, done 
    elif args.done:
        li.list_task(tasks_to_display="done", view="all") # list done 
    elif args.active:
        li.list_task(tasks_to_display="active", view="active") # list in-progress 
    elif args.todo:
        li.list_task(tasks_to_display="todo") # list todos
    elif args.deleted:
        li.list_task(tasks_to_display="deleted", view="del") # list only deleted task 
    else:
        li.list_task() # list tasks which are in-progress or todo 