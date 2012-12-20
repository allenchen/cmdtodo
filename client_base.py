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
        if self.id is -1:
            return False
        return other.id == self.id

# TODO(allench): there's duplicate code here; only the task store differs between
# client and server base.
class TaskSet():
    def __init__(self, snapshot=None):
        if not snapshot:
            self.tasks = []
        else:
            self.tasks = [Task(snapshot=ts) for ts in snapshot.tasks]

        self.version = -1

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
    """Represents the task storage and main methods to interact with the
    RPC service.  This is really inefficient right now because of how
    many RPC calls we use, and how much data we're transferring with every
    one of these calls."""

    def __init__(self, stub):
        self.pending_tasks = TaskSet()
        self.active_tasks = TaskSet()
        self.completed_tasks = TaskSet()
        self.stub = stub
        # each one of these TaskSets should have a version, but right now
        # we only have a global version lock (which isn't efficient, but, eh)
        self.version = -1

    def complete_task(self, task):
        self.stub.complete_task(task)
        self.synchronize_active()
        self.synchronize_pending()
        self.synchronize_completed()

    def activate_task(self, task):
        self.stub.activate_task(task)
        self.synchronize_pending()
        self.synchronize_active()

    def add_pending_task(self, task):
        self.stub.add_pending_task(task)
        self.synchronize_pending()

    def delete_task(self, task):
        self.stub.remove_task(task)
        self.synchronize_pending()
        self.synchronize_active()
        self.synchronize_completed()

    def is_synchronized(self):
        return self.version == stub.get_snapshot_version()

    def synchronize_all(self):
        if not self.is_synchronized():
            self.synchronize_active()
            self.synchronize_pending()
            self.synchronize_completed()

    def synchronize_active(self):        
        self.active_tasks = TaskSet(stub,
                                    snapshot=stub.get_active_snapshot())

    def synchronize_pending(self):
        self.pending_tasks = TaskSet(stub,
                                     snapshot=stub.get_pending_snapshot())

    def synchronize_completed(self):
        self.completed_tasks = TaskSet(stub,
                                       snapshot=stub.get_completed_snapshot())
