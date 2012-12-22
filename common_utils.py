from common_base import Task, TaskSet

def determine_bucket(task):
    if task.active:
        return "ACTIVE"
    elif task.done:
        return "COMPLETED"
    else:
        return "PENDING"
