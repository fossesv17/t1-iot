from server import *

if __name__ == "__main__":
    server_udp = ServerUDP(HOST, PORT_UDP)
    signal.signal(signal.SIGINT, server_udp.handle_sigint)
    server_udp.start()
    # register server.handle_sigint as the handler function for SIGINT