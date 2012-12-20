"""Client for the TODO service.  Most of this is borrowed from @amatsukawa from
his version of this app at github.com/amatsukawa/todo_cli"""

from datetime import datetime, date
from subprocess import call

import xmlrpclib
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc


date_consts = pdc.Constants()
date_parser = pdt.Calendar(date_consts)

EDITOR = os.environ.get("EDITOR", "emacs")

cached_tasks = []

# if EDITOR == "vim":
#     raise IllegalEditorException, "Please specify a usable editor."
#     sys.exit(0)

def resolve_task_id(task_id):
    pass

def load_cached_tasks(cache_file):
    f = open("/tmp/todo_pickle", "r")

def parse_new_task(task_str, active=False):
    """
    @ for estimated priority
    # for label
    """
    priority = 5
    labels = []
    text = ''
    notes = ''
    contact = ''

    for word in task_str.split():
        if word.startswith("$"):
            priority = int(word[1:])
        elif word.startswith("@"):
            contact = word[1:]
        elif word.startswith("#"):
            labels.append(word[1:])
            text += word + " "
        else:
            text += word + " "

    return {'text': text.strip(),
            'labels': labels,
            'priority': priority,
            'count': 0,
            'contact': contact,
            'due': str(due),
            'notes': notes,
            'active': active,
            'done': False}

def edit_notes(params, view=True):
    task_num = params[0]
    task_id = task_tmp[task_num]
    task = task_store.get_task_by_id(task_id)
    content = task['notes']
    if not view:
        with tempfile.NamedTemporaryFile(suffix=".tmp") as temp:
          temp.write(content)
          temp.flush()
          call([EDITOR, temp.name])
          content = temp.read()
          temp.seek(0)
          content = temp.read()
          task_store.set_task_by_id(task_id, {"notes": content})
        list_tasks([])
    else:
        print content

def list_tasks(params):
    print
    mapper = {}
    incomplete = task_store.get_incomplete_tasks()
    today = []
    rest = []
    for task in incomplete:
        if task['today']:
            today.append(task)
        else:
            rest.append(task)
    today = sorted(today, key=lambda x: (parse_date(x['due']), x['text'].lower()))
    rest = sorted(rest, key=lambda x: (parse_date(x['due']), x['text'].lower()))
    i = 0
    for task in today:
        mapper[str(i)] = task["_id"]
        print format_task(i, task)
        i += 1
    print "\n---\n"
    for task in rest:
        mapper[str(i)] = task["_id"]
        print format_task(i, task)
        i += 1
    f = open("/tmp/todo_pickle", "w")
    pickle.dump(mapper, f)
    f.close()
    print

def format_task(index, task):
    print_str = "[{0}]    ".format(index)
    now = datetime.now().date()
    due = parse_date(task['due'])
    if now > due:
        print_str += colored("{due}    ".format(**task), "red")
    elif now < due:
        print_str += colored("{due}    ".format(**task), "blue")
    else:
        print_str += colored("{due}    ".format(**task), "yellow")
    print_str += colored("{0}/{1}    ".format(task['count'], task['est_count']), "cyan")
    print_str += "{text}    ".format(**task)
    for label in task['labels']:
        print_str += colored("#{0} ".format(label), "green")
    return print_str

def delay_priority_upgrade(
