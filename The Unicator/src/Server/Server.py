import pprint as pp
import threading

from Client_thread import ClientThread


class Server(threading.Thread):
    MAX_RECV = 10*1024*1024

    def __init__(self, threadName, connection, protocol):
        threading.Thread.__init__(self, name = threadName)
        self.nb_clients = 0
        self.connection = connection
        self.protocol = protocol

        # Sockets from which we expect to read
        self.clients = []

    def run(self):
        while True:
            print("waiting for clients")
            connection, client_address = self.connection.serverSocket.accept()
            print('new connection from', client_address)

            connection.setblocking(True)
            cli = ClientThread("Client " + str(self.nb_clients), connection, self.protocol)
            cli.start()
            self.clients.append(cli)
            pp.pprint(self.clients)
            self.nb_clients += 1

    def on_next(self, value):
        print("Received {0}".format(value))

    def on_completed(self):
        print("Done!")


