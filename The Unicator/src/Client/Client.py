import os

class Client:
    """
    Classe représentant le client
    """
    error_message = "Le chemin d'acces ne peut pas être vide."

    def __init__(self, protocol , connexion):
        self.protocol = protocol
        self.connexion = connexion
        self.connexion.connect()

    def ask_server(self, text):
        server_answer = self.exchange_data(text)
        return self.protocol.process_answer(server_answer)

    def verify_path(self,path):
        if path == '':
           return False

        return True

    def verify_connexion(self):
        request = self.protocol.verify_connexion("bonjourServeur")
        return self.ask_server(request)

    def know_server_name(self):
        request = self.protocol.know_server_name("questionNomServeur")
        return self.ask_server(request)

    def exchange_data(self,text):
        self.connexion.send(text)
        return self.connexion.receive()

    def close_connexion(self):
        text = self.protocol.close_connexion("quitter")
        server_answer = self.exchange_data(text)
        return self.protocol.process_answer(server_answer)
