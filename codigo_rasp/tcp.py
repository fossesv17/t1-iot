from server import *

if __name__ == "__main__":
    server_tcp = ServerTCP(HOST, PORT_TCP)
    signal.signal(signal.SIGINT, server_tcp.handle_sigint)
    server_tcp.start()
    # register server.handle_sigint as the handler function for SIGINT