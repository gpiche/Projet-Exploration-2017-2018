import sys
from Protocol_json import Protocol_json
from Server import Server
from Connection import Connection

if __name__ == '__main__':

    port = int(50010)

    Connection = Connection('', port)


    protocol = Protocol_json()


    server = Server("Server-Unicator", Connection, protocol)
    server.start()    # run forever....

