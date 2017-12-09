import socket
MAX_RECV = 1024 * 1024 * 512


class Connexion:
    def __init__(self):
        self.host = '192.168.1.103'
        self.port = 50010
        self.clientSocket = socket.socket()
        self.connect()

    def connect(self):
        self.clientSocket.connect((self.host, self.port))

    def send(self, text):
        self.clientSocket.send(bytes(str(text), 'UTF-8'))

    def receive(self):
        answer = self.clientSocket.recv(MAX_RECV).decode('UTF-8')
        return answer

    def close(self):
        self.clientSocket.close()