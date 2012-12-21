from common_base import Task, TaskSet, DuplicateIdException, NotImplementedException

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
        versions = self.stub.get_all_versions()
        return (
            self.pending_tasks.version == versions["pending_tasks"] and
            self.active_tasks.version == versions["active_tasks"] and
            self.completed_tasks.version == versions["completed_tasks"])

    def synchronize_all(self):
        versions = self.stub.get_all_versions()
        s_active = self.synchronize_active(versions=versions)
        s_pending = self.synchronize_pending(versions=versions)
        s_completed = self.synchronize_completed(versions=versions)
        return s_active or s_pending or s_completed

    def synchronize_active(self,versions=None):
        if not versions:
            versions = self.stub.get_all_versions()
        if self.active_tasks.version != versions["active_tasks"]:
            self.active_tasks = TaskSet(
                snapshot=self.stub.get_active_snapshot())
            return True
        return False

    def synchronize_pending(self,versions=None):
        if not versions:
            versions = self.stub.get_all_versions()
        if self.pending_tasks.version != versions["pending_tasks"]:
            self.pending_tasks = TaskSet(
                snapshot=self.stub.get_pending_snapshot())
            return True
        return False

    def synchronize_completed(self,versions=None):
        if not versions:
            versions = self.stub.get_all_versions()
        if self.completed_tasks.version != versions["completed_tasks"]:        
            self.completed_tasks = TaskSet(
                snapshot=self.stub.get_completed_snapshot())
            return True
        return False
