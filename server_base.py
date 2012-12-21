from common_base import Task, TaskSet, DuplicateIdException, NotImplementedException

class ServerTaskStore():
    def __init__(self):
        self.pending_tasks = TaskSet()
        self.active_tasks = TaskSet()
        self.completed_tasks = TaskSet()

    def complete_task(self, task):
        self.completed_tasks.add_task(task)
        self.active_tasks.remove_task(task)
        self.pending_tasks.remove_task(task)

    def activate_task(self, task):
        self.active_tasks.add_task(task)
        self.pending_tasks.remove_task(task)

    def add_task(self, task):
        if task.active:
            self.active_tasks.add_task(task)
        elif task.done:
            self.completed_tasks.add_task(task)
        else:
            self.pending_tasks.add_task(task)

    def delete_task(self, task):
        self.pending_tasks.remove_task(task)
        self.active_tasks.remove_task(task)
        self.completed_tasks.remove_task(task)
