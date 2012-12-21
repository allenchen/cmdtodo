"""Client for the TODO service.  Most of this is borrowed from @amatsukawa from
his version of this app at github.com/amatsukawa/todo_cli"""

from datetime import datetime, date
from subprocess import call
from client_base import Task, TaskSet, ClientTaskStore

import argparse
import xmlrpclib
import os
import sys
import client_formatting

EDITOR = os.environ.get("EDITOR", "emacs")

cached_tasks = []

# if EDITOR == "vim":
#     raise IllegalEditorException

def resolve_task_id(task_id):
    pass

def load_cached_tasks(cache_file):
    f = open("/tmp/cmdtodo_cached", "r")

# Utility functions

def assign_task_id(task, stub):
    task.id = stub.get_unique_id()

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

if __name__ == "__main__":
    main()
