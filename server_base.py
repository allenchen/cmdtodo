from common_base import Task, TaskSet, DuplicateIdException, NotImplementedException

import common_utils
import datetime

class DelayedUpdate():
    def __init__(self, task, new_priority, date):
        self.task = task
        self.new_priority = new_priority
        self.date = date

    def expire(self):
        return self.date < datetime.datetime.now()

class ServerTaskStore():
    def __init__(self):
        self.pending_tasks = TaskSet()
        self.active_tasks = TaskSet()
        self.completed_tasks = TaskSet()
        self.delayed_updates = []

    def complete_task(self, task):
        self.completed_tasks.add_task(task)
        self.active_tasks.remove_task(task)
        self.pending_tasks.remove_task(task)

    def activate_task(self, task):
        self.active_tasks.add_task(task)
        self.pending_tasks.remove_task(task)

    def add_task(self, task):
        bucket_tag = common_utils.determine_bucket(task)
        if bucket_tag == "ACTIVE":
            self.active_tasks.add_task(task)
        elif bucket_tag == "COMPLETED":
            self.completed_tasks.add_task(task)
        else:
            self.pending_tasks.add_task(task)

    def delete_task(self, task):
        self.pending_tasks.remove_task(task)
        self.active_tasks.remove_task(task)
        self.completed_tasks.remove_task(task)

    def add_delay_update(self, task, new_priority, date):
        self.delayed_updates += [DelayedUpdate(task, new_priority, date)]

    def edit_task(self, task):
        bucket_tag = common_utils.determine_bucket(task)

        if bucket_tag == "ACTIVE":
            bucket = self.active_tasks
        elif bucket_tag == "COMPLETED":
            bucket = self.completed_tasks
        else:
            bucket = self.pending_tasks

        replaced_task = bucket.get_by_id(task.id)
        bucket.remove_task(replaced_task)
        bucket.add_task(task)
        return task

    def flush_delayed_updates(self):
        self.expire_set = [
            upd for udp in self.delayed_updates if not upd.expire()]
        for updated_task in self.expire_set:
            updated_task.active = True
            self.edit_task(updated_task)
