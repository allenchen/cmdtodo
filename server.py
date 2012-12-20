from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

class TodoRequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/todo', '')


def main(unused_argv):
    server = SimpleXMLRPCServer(("localhost", 8000),
                                requestHandler=RequestHandler)
    server.register_introspection_functions()
