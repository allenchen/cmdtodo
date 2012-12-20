import xmlrpclib
import client_base
from client_base import TaskSet

stub = xmlrpclib.ServerProxy("http://localhost:8889")

print stub.get_snapshot_version()
print stub.increment_snapshot_version()
print stub.get_snapshot_version()

print stub.get_pending_snapshot()
