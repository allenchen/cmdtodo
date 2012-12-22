"""Client for the TODO service.  A lot of client functions are borrowed from
@amatsukawa from his version of this app at github.com/amatsukawa/todo_cli"""

from datetime import datetime, date
from subprocess import call
from client_base import Task, TaskSet, ClientTaskStore

import argparse
import xmlrpclib
import os
import sys
import client_formatting
import pickle

EDITOR = os.environ.get("EDITOR", "emacs")

CACHED_STORE_PATH = "/tmp/cmdtodo.store"

SERVER_PATH = "http://localhost:8889"

cached_store = ClientTaskStore(None)

# if EDITOR == "vim":
#     raise IllegalEditorException

def resolve_task_id(task_id):
    pass

def load_cached_tasks():
    cached_store = pickle.load(CACHED_STORE_PATH)

def dump_cached_tasks():
    cached_store_fh = open(CACHED_STORE_PATH, "w")
    tmp_stub = cached_store.stub
    cached_store.stub = None
    pickle.dump(cached_store, cached_store_fh)
    cached_store_fh.close()
    cached_store.stub = tmp_stub

def synchronize_cached_store():
    if cached_store.synchronize_all():
        dump_cached_tasks()

def add_task(task):
    val = cached_store.stub.add_task(task)
    synchronize_cached_store()
    return Task(snapshot=val)

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


def delay_priority_upgrade(params):
    # at some later date, you want to upgrade the priority of a task
    pass

def make_argparser():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("action")
    argument_parser.add_argument("query", nargs='*')
    return argument_parser.parse_args()

def main():
    args = make_argparser()
    stub = xmlrpclib.ServerProxy(SERVER_PATH)
    cached_store.stub = stub
    synchronize_cached_store()

    if args.action == "add":
        query = " ".join(args.query)
        result = add_task(client_formatting.parse_new_task(query))
        print result

if __name__ == "__main__":
    main()
