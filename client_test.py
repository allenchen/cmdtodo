import xmlrpclib
import client_base
import client_formatting

stub = xmlrpclib.ServerProxy("http://localhost:8889")
"""
print stub.get_snapshot_version()
print stub.increment_snapshot_version()
print stub.get_snapshot_version()

print stub.get_pending_snapshot()
"""

task = client_formatting.parse_new_task("finish the todoservice #personal @allench $2")
client_formatting.assign_task_id(task, stub)
print task.__dict__
