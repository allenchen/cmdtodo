from server_base import ServerTaskStore, TaskSet, Task

"""Todo service, defining the RPC functions."""

class TodoService():
    def __init__(self):
        # TODO(allench): these are temporary, they obviously need to be 
        # persisted somewhere, and loaded in every time we start up the
        # todo service.
        self.snapshot_version = 0
        self.id_counter = 0
        self.task_store = ServerTaskStore()

    def pre_cleanup(self):
        # do stuff like delay_priority_upgrade checks
        pass

    def get_unique_id(self):
        self.id_counter += 1
        return self.id_counter

    def increment_snapshot_version(self):
        self.snapshot_version += 1

    def get_snapshot_version(self):
        return self.snapshot_version

    def get_active_snapshot(self):
        return self.task_store.active_tasks

    def get_pending_snapshot(self):
        return self.task_store.pending_tasks

    def get_completed_snapshot(self):
        return self.task_store.completed_tasks
