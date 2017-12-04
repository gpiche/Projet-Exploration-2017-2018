import threading


class ClientThread(threading.Thread):
    """Thread to process each client request"""

    MAX_RECV = 10*1024*1024

    def __init__(self, name, connect, protocol):
        threading.Thread.__init__(self, name=name)
        self.connection = connect
        self.name = name
        self.protocol = protocol

    def run(self):
        while True:
            try:
                data = self.connection.recv(self.MAX_RECV).decode(encoding='UTF-8')
                print('Client "%s" received "%s" from %s' % (self.name, data, self.connection.getpeername()))
                reply = str(self.protocol.process_query(data))
                print('Client "%s" reply is "%s"' % (self.name, reply))
                self.connection.send(bytes(reply, 'UTF8'))

            except (InterruptedError, ConnectionResetError) as e:
                msg = 'Client "%s" error: %s' % (self.name, e)
                self.connection.send(bytes(msg, 'UTF8'))


            #except ConnectionResetError as e:
            #    pass

            #except InterruptedError as e:
            #    msg = 'Client "%s" error: %s' % (self.name, e)
            #    self.connection.send(bytes(msg, 'UTF8'))


