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

    def __str__(self):
        s = (
            """[
Task #{0}:
  Text: {1}
  Labels: {2}
  Priority: {3}
  Contact: {4}
  Notes: {5}
  Active? {6}
  Done? {7}
]""".format(
                self.id,
                self.text,
                self.labels,
                self.priority,
                self.contact,
                self.notes,
                self.active,
                self.done))
        return s

    def formatted_print(self):
        return "[{0}] ${1} @{2} {3}".format(
            self.id, self.priority, self.contact, self.text)


class TaskSet():
    def __init__(self, snapshot=None):
        if not snapshot:
            self.tasks = []
            self.version = -1
        else:
            self.tasks = [Task(snapshot=ts) for ts in snapshot["tasks"]]
            self.version = snapshot["version"]

    def __contains__(self, task):
        return task in self.tasks

    def add_task(self, task):
        if task in self:
            raise (DuplicateIdException, 
                   "Duplicate ID insertion attempted: " + str(task))

        self.tasks += [task]
        self.increment_version()
        return True

    def remove_task(self, task):
        if task not in self:
            return False

        self.tasks.remove(task)
        self.increment_version()
        return True

    def edit_task(self, old_task, new_task):
        # we do this because, technically, you might change the ID.
        self.remove_task(old_task)
        self.add_task(new_task)
        self.increment_version()

    def get_by_id(self, task_id):
        candidates = [t for t in self.tasks if t.id == task_id]
        if len(candidates) < 1:
            return None
        return candidates[0]

    def increment_version(self):
        self.version += 1

    def __str__(self):
        s = """[\nTaskSet version """ + str(self.version) + "\n"
        for t in self.tasks:
            s += t.__str__()
        s += "\n]"
        return s

    def formatted_print(self):
        statements = []
        for t in sorted(self.tasks, lambda x: x.priority):
            statements += [t.formatted_print()]
        return "\n".join(statements)
