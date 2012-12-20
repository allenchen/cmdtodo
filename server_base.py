class NotImplementedException(Exception):
    pass

class DuplicateIdException(Exception):
    pass

class Task():
    def __init__(self, snapshot=None):
        if not snapshot:
            self.id = -1
            self.text = ''
            self.labels = []
            self.priority = 5
            self.contact = ''
            self.notes = ''
            self.active = False
            self.done = False

        else:
            self.__dict__ = snapshot

    def __eq__(self, other):
        return other.id == self.id


# TODO(allench): there's duplicate code here; only the task store differs between
# client and server base.
class TaskSet():
    def __init__(self, snapshot=None):
        if not snapshot:
            self.tasks = []
        else:
            self.tasks = [Task(snapshot=ts) for ts in snapshot.tasks]

    def add_task(self, task):
        if task in self:
            raise (DuplicateIdException, 
                   "Duplicate ID insertion attempted: " + str(task))

        self.tasks += [task]
        return True

    def remove_task(self, task):
        if task not in self:
            return False

        self.tasks.remove(task)

    def edit_task(self, old_task, new_task):
        # we do this because, technically, you might change the ID.
        self.remove_task(old_task)
        self.add_task(new_task)

    def __contains__(self, task):
        return task in self.tasks

    def get_by_id(self, task_id):
        candidates = [t for t in self.tasks if t.id == task_id]
        if len(candidates) < 1:
            return None
        return candidates[0]
        

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

    def add_pending_task(self, task):
        # TODO(allench): This should just be "add_task", so we can just add
        # a task of any status.  We should look at the status of it (pending,
        # active, or completed) and place it into the appropriate bin, instead
        # of just having added tasks always in the pending state.
        self.pending_tasks.add_task(task)

    def delete_task(self, task):
        self.pending_tasks.remove_task(task)
        self.active_tasks.remove_task(task)
        self.completed_task.remove_task(task)
