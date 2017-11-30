import socket
MAX_RECV = 1024 * 1024 * 512


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverSocket = socket.socket()
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(5)

    def send(self, text):
        self.serverSocket.send(bytes(str(text), 'UTF-8'))

