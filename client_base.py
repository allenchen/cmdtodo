class NotImplementedException(Exception):
    pass

class DuplicateIdException(Exception):
    pass

class Task():
    def __init__(self, snapshot=None):
        if not snapshot:
            self.id = -1
        else:
            self.__dict__ = snapshot

    def __eq__(self, other):
        if self.id is -1:
            return False
        return other.id == self.id


class ClientTaskSet():
    def __init__(self, stub, snapshot=None):
        if not snapshot:
            self.tasks = []
        else:
            self.tasks = [Task(snapshot=ts) for ts in snapshot.tasks]

        self.stub = stub

    def __contains__(self, task):
        return task in self.tasks

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

    def get_by_id(self, task_id):
        candidates = [t for t in self.tasks if t.id == task_id]
        if len(candidates) < 1:
            return None
        return candidates[0]
        

class ClientTaskStore():
    def __init__(self, stub):
        self.pending_tasks = TaskSet()
        self.active_tasks = TaskSet()
        self.completed_tasks = TaskSet()
        self.stub = stub
        self.version = -1

    def complete_task(self, task):
        self.completed_tasks.add_task(task)
        self.active_tasks.remove_task(task)
        self.pending_tasks.remove_task(task)

    def activate_task(self, task):
        self.active_tasks.add_task(task)
        self.pending_tasks.remove_task(task)

    def add_pending_task(self, task):
        self.pending_tasks.add_task(task)

    def delete_task(self, task):
        self.pending_tasks.remove_task(task)
        self.active_tasks.remove_task(task)
        self.completed_task.remove_task(task)

    def is_synchronized(self):
        return self.version == stub.get_snapshot_version()

    def synchronize_active(self):
        self.active_tasks = TaskSet(stub,
                                    snapshot=stub.get_active_snapshot())

    def synchronize_pending(self):
        self.pending_tasks = TaskSet(stub,
                                     snapshot=stub.get_pending_snapshot())

    def synchronize_completed(self):
        self.completed_tasks = TaskSet(stub,
                                       snapshot=stub.get_completed_snapshot())
