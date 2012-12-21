from client_base import Task, TaskSet, ClientTaskStore

def parse_new_task(task_str, active=False):
    """
    Given a string that denotes a user supplied string that describes a task,
    returns a task object.
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

    task = Task()
    task.text = text.strip()
    task.labels = labels
    task.priority = priority
    task.contact = contact
    task.notes = notes
    task.active = active
    task.done = False

    return task

def list_tasks(stub, task_store):
    

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
