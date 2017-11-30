from ProtocolJson import ProtocolJson
from Server import Server
from Connection import Connection

if __name__ == '__main__':

    port = int(50010)
    Connection = Connection('localhost', port)
    protocol = ProtocolJson()
    server = Server("Server-Robot", Connection, protocol)
    server.start()    # run forever....

