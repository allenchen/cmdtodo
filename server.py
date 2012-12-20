from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from todo_service import TodoService

class TodoRequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2', '')


def main():
    server = SimpleXMLRPCServer(("localhost", 8889),
                                requestHandler=TodoRequestHandler,
                                allow_none=True)
    server.register_introspection_functions()
    server.register_instance(TodoService())

    server.serve_forever()


if __name__ == "__main__":
    main()
