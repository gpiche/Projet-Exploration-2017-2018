import sys
from Connexion import Connexion
from Protocol_json import Protocol_json
from Client import Client
from Prompt import Prompt


host = 'localhost'

if __name__ == '__main__':
    port = 50010

    connexion = Connexion(host, port)

    protocol = Protocol_json()

    client = Client(protocol, connexion)


    prompt = Prompt(client)



