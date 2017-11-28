
class Prompt:
    def __init__(self,client, prompt_pattern='Client: '):
        """Constructeur de l'interpréteur"""
        self.prompt_pattern = prompt_pattern
        self.command = ''
        self.client = client
        self.run()



    def process(self, input):
     """Interpréteur des commandes."""

     self.command = input
     return self.command


    def invite(self, prompt):
     """ Interaction avec l'utilisateur """
     answer = input(prompt)
     return answer

    def run(self):
        while True:
            answer = self.invite(self.prompt_pattern)
            processed_answer = self.process(answer)

            try:
             if processed_answer == 'Je veux une pizza et un café svp!':
                response = self.client.verify_connexion()

             elif processed_answer == 'Whoami?':
                response = self.client.know_server_name()

             else:
                response = "Commande invalide"

             print('Serveur: ' + str(response))

            except IOError as e:
                print(e)

